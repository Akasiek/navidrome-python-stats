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
