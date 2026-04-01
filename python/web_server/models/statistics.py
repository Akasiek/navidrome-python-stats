from __future__ import annotations

from pydantic import BaseModel


class LibraryStats(BaseModel):
    artist_count: int
    album_count: int
    song_count: int
    starred_album_count: int
    starred_song_count: int
    starred_artist_count: int
    playlist_count: int
    user_count: int
    genre_count: int
    radio_station_count: int
    format_counts: dict[str, int]


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