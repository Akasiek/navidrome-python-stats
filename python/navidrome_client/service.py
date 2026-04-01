from __future__ import annotations

from .client import NavidromeClient
from .config import NavidromeConfig
from ._artists_mixin import ArtistsMixin
from ._albums_mixin import AlbumsMixin
from ._songs_mixin import SongsMixin
from ._library_mixin import LibraryMixin
from ._insights_mixin import InsightsMixin


class NavidromeService(ArtistsMixin, AlbumsMixin, SongsMixin, LibraryMixin, InsightsMixin):
    def __init__(self, config: NavidromeConfig) -> None:
        self.client = NavidromeClient(config)

    async def open(self) -> None:
        await self.client.open()

    async def close(self) -> None:
        await self.client.close()

    async def __aenter__(self) -> NavidromeService:
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