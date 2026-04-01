from __future__ import annotations

import asyncio


class InsightsMixin:
    _DECADES = [
        ("1960s", 1960, 1969), ("1970s", 1970, 1979), ("1980s", 1980, 1989),
        ("1990s", 1990, 1999), ("2000s", 2000, 2009), ("2010s", 2010, 2019),
        ("2020s", 2020, 2029),
    ]

    async def get_top_genres(self, limit: int = 15) -> "list[GenreStat]":
        from web_server.models.statistics import GenreStat

        data = await self.client.request("getGenres")
        raw_genres = data.get("genres", {}).get("genre", [])
        genres = [
            GenreStat(name=g["value"], song_count=g.get("songCount", 0), album_count=g.get("albumCount", 0))
            for g in raw_genres
        ]
        return sorted(genres, key=lambda g: g.song_count, reverse=True)[:limit]

    async def get_albums_by_decade(self) -> "list[DecadeStat]":
        from web_server.models.statistics import DecadeStat

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

    async def get_most_prolific_artists(self, limit: int = 15) -> "ChartData":
        from web_server.models.statistics import ChartData

        result = await self.client.request_api("artist", {
            "_sort": "albumCount", "_order": "DESC", "_start": 0, "_end": limit,
        })
        artists: list[dict] = result["body"]
        return ChartData(
            labels=[a.get("name", "Unknown") for a in artists],
            values=[a.get("albumCount", 0) for a in artists],
        )

    async def get_longest_albums(self, limit: int = 10) -> "ChartData":
        from web_server.models.statistics import ChartData

        result = await self.client.request_api("album", {
            "_sort": "duration", "_order": "DESC", "_start": 0, "_end": limit,
        })
        albums: list[dict] = result["body"]
        return ChartData(
            labels=[f"{a.get('name', '?')} — {a.get('artist', 'Unknown')}" for a in albums],
            values=[a.get("duration", 0) for a in albums],
        )

    async def get_most_played_artists(self, limit: int = 15) -> "ChartData":
        from web_server.models.statistics import ChartData

        all_albums = await self._scan_all_albums_raw()
        play_counts: dict[str, int] = {}
        for album in all_albums:
            artist = album.get("albumArtist") or album.get("artist") or album.get("artistName") or "Unknown"
            play_counts[artist] = play_counts.get(artist, 0) + album.get("playCount", 0)

        top = sorted(
            ((name, count) for name, count in play_counts.items() if count > 0),
            key=lambda x: x[1],
            reverse=True,
        )[:limit]
        return ChartData(
            labels=[name for name, _ in top],
            values=[count for _, count in top],
        )

    async def get_library_duration(self) -> "LibraryDurationData":
        from web_server.models.statistics import LibraryDurationData

        all_albums = await self._scan_all_albums_raw()
        total_seconds = int(sum(a.get("duration", 0) for a in all_albums))
        avg = total_seconds // len(all_albums) if all_albums else 0
        return LibraryDurationData(total_seconds=total_seconds, avg_album_seconds=avg)

    async def get_never_played(self) -> "NeverPlayedData":
        from web_server.models.statistics import NeverPlayedData

        all_albums, all_songs = await asyncio.gather(
            self._scan_all_albums_raw(),
            self._scan_all_songs_raw(),
        )
        never_albums = sum(1 for a in all_albums if a.get("playCount", 0) == 0)
        never_songs = sum(1 for s in all_songs if s.get("playCount", 0) == 0)
        return NeverPlayedData(
            albums_played=len(all_albums) - never_albums,
            albums_never_played=never_albums,
            songs_played=len(all_songs) - never_songs,
            songs_never_played=never_songs,
        )

    async def get_top_played_songs(self, limit: int = 15) -> "ChartData":
        from web_server.models.statistics import ChartData

        result = await self.client.request_api("song", {
            "_sort": "playCount", "_order": "DESC", "_start": 0, "_end": limit,
        })
        songs: list[dict] = result["body"]
        played = [s for s in songs if s.get("playCount", 0) > 0]
        return ChartData(
            labels=[f"{s.get('title', '?')} — {s.get('artist', 'Unknown')}" for s in played],
            values=[s.get("playCount", 0) for s in played],
        )

    async def get_artist_dominance(self, limit: int = 10) -> "ChartData":
        from web_server.models.statistics import ChartData

        all_albums = await self._scan_all_albums_raw()
        album_counts: dict[str, int] = {}
        for album in all_albums:
            artist = album.get("albumArtist") or album.get("artist") or album.get("artistName") or "Unknown"
            album_counts[artist] = album_counts.get(artist, 0) + 1

        top = sorted(album_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
        others = sum(count for _, count in sorted(album_counts.items(), key=lambda x: x[1], reverse=True)[limit:])

        labels = [name for name, _ in top]
        values = [count for _, count in top]
        if others > 0:
            labels.append("Others")
            values.append(others)
        return ChartData(labels=labels, values=values)