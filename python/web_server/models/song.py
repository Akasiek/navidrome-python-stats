from __future__ import annotations
from pydantic import BaseModel, Field


class Song(BaseModel):
    id: str
    title: str
    album: str | None = None
    album_id: str | None = Field(None)
    artist: str | None = None
    artist_id: str | None = Field(None)
    track: int | None = None
    duration: int | None = None

    model_config = {"populate_by_name": True}
