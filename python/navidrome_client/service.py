from __future__ import annotations

import asyncio
import json
from typing import Literal

from web_server.models.stats import LibraryStats
from .client import NavidromeClient
from .config import NavidromeConfig
from web_server.models.album import Album
from web_server.models.artist import Artist
from web_server.models.song import Song

AlbumListType = Literal[
    "random",
    "newest",
    "highest",
    "frequent",
    "recent",
    "alphabeticalByName",
    "alphabeticalByArtist",
    "starred",
    "byYear",
    "byGenre",
]


class NavidromeService:
    def __init__(self, config: NavidromeConfig) -> None:
        self.client = NavidromeClient(config)

    async def open(self) -> None:
        await self.client.open()

    async def close(self) -> None:
        await self.client.close()

    async def __aenter__(self) -> "NavidromeService":
        await self.open()
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def ping(self) -> bool:
        try:
            await self.client.request("ping")
            return True
        except Exception:
            return False

    async def get_artists(self) -> list[Artist]:
        data = await self.client.request("getArtists")
        raw_index: list[dict] = (
            data.get("artists", {}).get("index", [])
        )
        artists: list[Artist] = []
        for index_entry in raw_index:
            for raw_artist in index_entry.get("artist", []):
                artists.append(Artist.model_validate(raw_artist))
        return artists

    async def get_albums(
        self,
        list_type: AlbumListType = "alphabeticalByName",
        size: int = 50,
        offset: int = 0,
    ) -> list[Album]:
        data = await self.client.request(
            "getAlbumList2",
            extra_params={"type": list_type, "size": size, "offset": offset},
        )
        raw_albums: list[dict] = data.get("albumList2", {}).get("album", [])
        return [Album.model_validate(a) for a in raw_albums]

    async def get_newest_albums(self, size: int = 20, offset: int = 0) -> list[Album]:
        return await self.get_albums("newest", size=size, offset=offset)

    async def get_frequent_albums(self, size: int = 20, offset: int = 0) -> list[Album]:
        return await self.get_albums("frequent", size=size, offset=offset)

    async def get_starred_albums(self, size: int = 20, offset: int = 0) -> list[Album]:
        return await self.get_albums("starred", size=size, offset=offset)

    async def get_recent_albums(self, size: int = 20, offset: int = 0) -> list[Album]:
        return await self.get_albums("recent", size=size, offset=offset)

    async def get_random_albums(self, size: int = 20) -> list[Album]:
        return await self.get_albums("random", size=size)

    async def get_top_rated_albums(self, size: int = 20, offset: int = 0) -> list[Album]:
        return await self.get_albums("highest", size=size, offset=offset)

    _AUDIO_FORMATS = ["flac", "opus", "mp3", "ogg", "m4a", "aac", "wav", "aiff", "wv", "ape"]

    async def _get_total_count(self, resource: str, filter: dict | None = None) -> int:
        params: dict = {"_start": 1, "_end": 2}
        if filter:
            params.update(filter)
        result = await self.client.request_api(resource, params)
        return int(result['headers']['x-total-count'])

    async def get_library_stats(self) -> "LibraryStats":
        from web_server.models.stats import LibraryStats

        artist_count = await self._get_total_count("artist")
        album_count = await self._get_total_count("album")
        song_count = await self._get_total_count("song")
        playlist_count = await self._get_total_count("playlist")

        genres_data, radio_data, users_data = await asyncio.gather(
            self.client.request("getGenres"),
            self.client.request("getInternetRadioStations"),
            self.client.request("getUsers"),
        )
        genre_count = len(genres_data.get("genres", {}).get("genre", []))
        radio_station_count = len(radio_data.get("internetRadioStations", {}).get("internetRadioStation", []))
        user_count = len(users_data.get("users", {}).get("user", []))

        starred_data = await self.client.request("getStarred2")
        starred = starred_data.get("starred2", {})
        starred_artist_count = len(starred.get("artist", []))
        starred_album_count = len(starred.get("album", []))
        starred_song_count = len(starred.get("song", []))

        format_counts_raw = await asyncio.gather(
            *[self._get_total_count("song", {"suffix": fmt}) for fmt in self._AUDIO_FORMATS]
        )
        format_counts = {
            fmt: count
            for fmt, count in zip(self._AUDIO_FORMATS, format_counts_raw)
            if count > 0
        }

        return LibraryStats(
            artist_count=artist_count,
            album_count=album_count,
            song_count=song_count,
            starred_album_count=starred_album_count,
            starred_song_count=starred_song_count,
            starred_artist_count=starred_artist_count,
            playlist_count=playlist_count,
            user_count=user_count,
            genre_count=genre_count,
            radio_station_count=radio_station_count,
            format_counts=format_counts,
        )

    async def _get_top_genres(self, limit: int = 15) -> list["GenreStat"]:
        from web_server.models.insights import GenreStat

        data = await self.client.request("getGenres")
        raw_genres = data.get("genres", {}).get("genre", [])
        genres = [
            GenreStat(name=g["value"], song_count=g.get("songCount", 0), album_count=g.get("albumCount", 0))
            for g in raw_genres
        ]
        return sorted(genres, key=lambda g: g.song_count, reverse=True)[:limit]

    _DECADES = [
        ("1960s", 1960, 1969), ("1970s", 1970, 1979), ("1980s", 1980, 1989),
        ("1990s", 1990, 1999), ("2000s", 2000, 2009), ("2010s", 2010, 2019),
        ("2020s", 2020, 2029),
    ]

    async def _get_albums_by_decade(self) -> list["DecadeStat"]:
        from web_server.models.insights import DecadeStat

        decade_counts: dict[int, int] = {}
        offset = 0
        page_size = 500

        while True:
            result = await self.client.request_api("album", {"_start": offset, "_end": offset + page_size})
            batch: list[dict] = result["body"]
            for album in batch:
                year = album.get("maxYear") or album.get("year") or 0
                if year > 0:
                    decade_start = (year // 10) * 10
                    decade_counts[decade_start] = decade_counts.get(decade_start, 0) + 1
            if len(batch) < page_size:
                break
            offset += page_size

        return [
            DecadeStat(decade=label, album_count=decade_counts.get(decade_start, 0))
            for label, decade_start, _ in self._DECADES
            if decade_counts.get(decade_start, 0) > 0
        ]

    async def _get_format_counts(self) -> dict[str, int]:
        counts = await asyncio.gather(
            *[self._get_total_count("song", {"suffix": fmt}) for fmt in self._AUDIO_FORMATS]
        )
        return {fmt: count for fmt, count in zip(self._AUDIO_FORMATS, counts) if count > 0}

    async def get_insights(self) -> "InsightsData":
        from web_server.models.insights import InsightsData

        top_genres, albums_by_decade, format_counts = await asyncio.gather(
            self._get_top_genres(),
            self._get_albums_by_decade(),
            self._get_format_counts(),
        )

        return InsightsData(top_genres=top_genres, albums_by_decade=albums_by_decade, format_counts=format_counts)

    async def get_songs(self, album_id: str) -> list[Song]:
        data = await self.client.request(
            "getAlbum",
            extra_params={"id": album_id},
        )
        raw_songs: list[dict] = data.get("album", {}).get("song", [])
        return [Song.model_validate(s) for s in raw_songs]
