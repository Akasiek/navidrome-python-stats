from __future__ import annotations
from typing import TYPE_CHECKING
from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel

if TYPE_CHECKING:
    from web_server.dependencies import NavidromeDep


class Album(BaseModel):
    id: str
    name: str
    artist: str | None = None
    artist_id: str | None = Field(None)
    artist_url: str | None = None
    year: int | None = None
    song_count: int = Field(0)
    duration: int | None = None
    cover_art: str | None = Field(None)
    cover_art_url: str | None = None
    play_count: int = Field(0)
    starred: str | None = None  # ISO-8601 timestamp, present when album is starred
    genre: str | None = None
    rating: int | None = Field(None, alias="userRating")

    model_config = {"populate_by_name": True, "alias_generator": to_camel}


class AlbumResponse(BaseModel):
    name: str
    url: str | None = None
    artist: str | None = None
    artist_url: str | None = None
    year: int | None = None
    duration: int | None = None
    cover_art_url: str | None = Field(None)
    play_count: int = Field(0)
    starred: str | None = None
    genre: str | None = None
    rating: int | None = None

    @classmethod
    def get_album_url(cls, album: Album, service: NavidromeDep) -> str | None:
        if album.id:
            return service.client.build_navidrome_url(f"album/{album.id}/show", False)
        return None

    @classmethod
    def get_artist_url(cls, album: Album, service: NavidromeDep) -> str | None:
        if album.artist_id:
            return service.client.build_navidrome_url(f"artist/{album.artist_id}/show", False)
        return None

    @classmethod
    def get_cover_art_url(cls, album: Album, service: NavidromeDep) -> str | None:
        if album.cover_art:
            return f"/api/albums/cover/{album.cover_art}"
        return None

    @classmethod
    def from_album(cls, album: Album, service: NavidromeDep) -> AlbumResponse:
        return cls(
            name=album.name,
            url=cls.get_album_url(album, service),
            artist=album.artist,
            artist_url=cls.get_artist_url(album, service),
            year=album.year,
            duration=album.duration,
            cover_art_url=cls.get_cover_art_url(album, service),
            play_count=album.play_count,
            starred=album.starred,
            genre=album.genre,
            rating=album.rating,
        )


class AlbumListResponse(BaseModel):
    albums: list[AlbumResponse]
