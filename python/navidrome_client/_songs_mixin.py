from __future__ import annotations

from web_server.models.song import Song


class SongsMixin:
    async def get_songs(self, album_id: str) -> list[Song]:
        data = await self.client.request(
            "getAlbum",
            extra_params={"id": album_id},
        )
        raw_songs: list[dict] = data.get("album", {}).get("song", [])
        return [Song.model_validate(s) for s in raw_songs]

    async def _scan_all_songs_raw(self) -> list[dict]:
        songs = []
        offset = 0
        page_size = 500
        while True:
            result = await self.client.request_api("song", {"_start": offset, "_end": offset + page_size})
            batch: list[dict] = result["body"]
            songs.extend(batch)
            if len(batch) < page_size:
                break
            offset += page_size
        return songs