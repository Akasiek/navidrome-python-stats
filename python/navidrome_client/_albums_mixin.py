from __future__ import annotations

from typing import Literal

from web_server.models.album import Album

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


class AlbumsMixin:
    async def _get_albums(
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
        return await self._get_albums("newest", size=size, offset=offset)

    async def get_frequent_albums(self, size: int = 20, offset: int = 0) -> list[Album]:
        return await self._get_albums("frequent", size=size, offset=offset)

    async def get_starred_albums(self, size: int = 20, offset: int = 0) -> list[Album]:
        return await self._get_albums("starred", size=size, offset=offset)

    async def get_recent_albums(self, size: int = 20, offset: int = 0) -> list[Album]:
        return await self._get_albums("recent", size=size, offset=offset)

    async def _get_random_albums(self, size: int = 20) -> list[Album]:
        return await self._get_albums("random", size=size)

    async def get_top_rated_albums(self, size: int = 20, offset: int = 0) -> list[Album]:
        return await self._get_albums("highest", size=size, offset=offset)

    async def _scan_all_albums_raw(self) -> list[dict]:
        albums = []
        offset = 0
        page_size = 500
        while True:
            result = await self.client.request_api("album", {"_start": offset, "_end": offset + page_size})
            batch: list[dict] = result["body"]
            albums.extend(batch)
            if len(batch) < page_size:
                break
            offset += page_size
        return albums