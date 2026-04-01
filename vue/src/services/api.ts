// API service for communicating with FastAPI backend

import type {
  AlbumsResponse,
  SongsResponse,
  ArtistsResponse,
  PingResponse,
  LibraryStats,
  GenreStat,
  DecadeStat,
  ChartData,
  NeverPlayedData,
  LibraryDurationData,
} from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

async function request<T>(endpoint: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`)

  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`)
  }

  return response.json()
}

export const api = {
  // Navidrome endpoints
  ping: () => request<PingResponse>('/navidrome/ping'),
  getArtists: () => request<ArtistsResponse>('/navidrome/artists'),

  // Album endpoints
  getNewestAlbums: (size = 20, offset = 0) =>
    request<AlbumsResponse>(`/albums/newest?size=${size}&offset=${offset}`),

  getFrequentAlbums: (size = 20, offset = 0) =>
    request<AlbumsResponse>(`/albums/frequent?size=${size}&offset=${offset}`),

  getStarredAlbums: (size = 20, offset = 0) =>
    request<AlbumsResponse>(`/albums/starred?size=${size}&offset=${offset}`),

  getRecentAlbums: (size = 20, offset = 0) =>
    request<AlbumsResponse>(`/albums/recent?size=${size}&offset=${offset}`),

  getTopRatedAlbums: (size = 20, offset = 0) =>
    request<AlbumsResponse>(`/albums/top-rated?size=${size}&offset=${offset}`),

  getAlbumSongs: (albumId: string) => request<SongsResponse>(`/albums/${albumId}/songs`),

  getStats: () => request<LibraryStats>('/statistics'),
  getTopGenres: () => request<GenreStat[]>('/statistics/insights/top-genres'),
  getAlbumsByDecade: () => request<DecadeStat[]>('/statistics/insights/albums-by-decade'),
  getFormatCounts: () => request<Record<string, number>>('/statistics/insights/format-counts'),
  getMostProlificArtists: () => request<ChartData>('/statistics/insights/most-prolific-artists'),
  getArtistDominance: () => request<ChartData>('/statistics/insights/artist-dominance'),
  getLongestAlbums: () => request<ChartData>('/statistics/insights/longest-albums'),
  getMostPlayedArtists: () => request<ChartData>('/statistics/insights/most-played-artists'),
  getLibraryDuration: () => request<LibraryDurationData>('/statistics/insights/library-duration'),
  getNeverPlayed: () => request<NeverPlayedData>('/statistics/insights/never-played'),
  getTopPlayedSongs: () => request<ChartData>('/statistics/insights/top-played-songs'),
}
