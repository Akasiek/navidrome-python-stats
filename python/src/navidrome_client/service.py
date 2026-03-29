from __future__ import annotations

from typing import Literal

from .client import NavidromeClient
from .config import NavidromeConfig
from .models import Album, Artist, Song

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

    async def get_songs(self, album_id: str) -> list[Song]:
        data = await self.client.request(
            "getAlbum",
            extra_params={"id": album_id},
        )
        raw_songs: list[dict] = data.get("album", {}).get("song", [])
        return [Song.model_validate(s) for s in raw_songs]
