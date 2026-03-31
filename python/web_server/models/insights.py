from __future__ import annotations

from pydantic import BaseModel


class GenreStat(BaseModel):
    name: str
    song_count: int
    album_count: int


class DecadeStat(BaseModel):
    decade: str
    album_count: int


class InsightsData(BaseModel):
    top_genres: list[GenreStat]
    albums_by_decade: list[DecadeStat]
    format_counts: dict[str, int]
