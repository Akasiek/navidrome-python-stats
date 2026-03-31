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

export interface GenreStat {
  name: string
  song_count: number
  album_count: number
}

export interface DecadeStat {
  decade: string
  album_count: number
}

export interface InsightsData {
  top_genres: GenreStat[]
  albums_by_decade: DecadeStat[]
  format_counts: Record<string, number>
}

export interface LibraryStats {
  artist_count: number
  album_count: number
  song_count: number
  starred_album_count: number
  starred_song_count: number
  starred_artist_count: number
  playlist_count: number
  user_count: number
  genre_count: number
  radio_station_count: number
  format_counts: Record<string, number>
}
