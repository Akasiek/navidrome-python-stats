from __future__ import annotations

from pydantic import BaseModel, Field

class Artist(BaseModel):
    id: str
    name: str
    album_count: int = Field(0, alias="albumCount")

    model_config = {"populate_by_name": True}

class Album(BaseModel):
    id: str
    name: str
    artist: str | None = None
    artist_id: str | None = Field(None, alias="artistId")
    year: int | None = None
    song_count: int = Field(0, alias="songCount")
    duration: int | None = None
    cover_art: str | None = Field(None, alias="coverArt")
    play_count: int = Field(0, alias="playCount")
    starred: str | None = None   # ISO-8601 timestamp, present when album is starred
    genre: str | None = None
    rating: int | None = None    # 1-5 user rating

    model_config = {"populate_by_name": True}

class Song(BaseModel):
    id: str
    title: str
    album: str | None = None
    album_id: str | None = Field(None, alias="albumId")
    artist: str | None = None
    artist_id: str | None = Field(None, alias="artistId")
    track: int | None = None
    duration: int | None = None
    cover_art: str | None = Field(None, alias="coverArt")

    model_config = {"populate_by_name": True}

