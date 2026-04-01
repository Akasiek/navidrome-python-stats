from __future__ import annotations

import asyncio


class LibraryMixin:
    _AUDIO_FORMATS = ["flac", "opus", "mp3", "ogg", "m4a", "aac", "wav", "aiff", "wv", "ape"]

    async def _get_total_count(self, resource: str, filter: dict | None = None) -> int:
        params: dict = {"_start": 1, "_end": 2}
        if filter:
            params.update(filter)
        result = await self.client.request_api(resource, params)
        return int(result['headers']['x-total-count'])

    async def get_library_stats(self) -> "LibraryStats":
        from web_server.models.statistics import LibraryStats

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

    async def get_format_counts(self) -> dict[str, int]:
        counts = await asyncio.gather(
            *[self._get_total_count("song", {"suffix": fmt}) for fmt in self._AUDIO_FORMATS]
        )
        return {fmt: count for fmt, count in zip(self._AUDIO_FORMATS, counts) if count > 0}
