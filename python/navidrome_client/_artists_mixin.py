from __future__ import annotations

from typing import TYPE_CHECKING

from web_server.models.artist import Artist

if TYPE_CHECKING:
    from .client import NavidromeClient


class ArtistsMixin:
    client: NavidromeClient
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