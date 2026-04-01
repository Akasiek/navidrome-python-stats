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
    total_seconds: int
    avg_album_seconds: int


class GenreStat(BaseModel):
    name: str
    song_count: int
    album_count: int


class DecadeStat(BaseModel):
    decade: str
    album_count: int


class ChartData(BaseModel):
    labels: list[str]
    values: list[int]


class NeverPlayedData(BaseModel):
    albums_played: int
    albums_never_played: int
    songs_played: int
    songs_never_played: int

