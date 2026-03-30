import type { Album } from './album'
import type { Artist } from './artist'
import type { Song } from './song'

export interface AlbumsResponse {
  albums: Album[]
}

export interface SongsResponse {
  songs: Song[]
}

export interface ArtistsResponse {
  artists: Artist[]
}

export interface PingResponse {
  status: string
}

