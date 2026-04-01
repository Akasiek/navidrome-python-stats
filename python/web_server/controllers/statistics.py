from fastapi import APIRouter

from web_server.dependencies import NavidromeDep
from web_server.models.statistics import (
    ChartData,
    DecadeStat,
    GenreStat,
    LibraryDurationData,
    LibraryStats,
    NeverPlayedData,
)

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("", response_model=LibraryStats,
            summary="Library primary statistics",
            description="Get primary statistics about the library, such as total songs, albums, artists, and total duration.")
async def get_library_stats(service: NavidromeDep):
    return await service.get_library_stats()


@router.get("/insights/top-genres", response_model=list[GenreStat],
            summary="Top genres by song count")
async def get_top_genres(service: NavidromeDep):
    return await service.get_top_genres()


@router.get("/insights/albums-by-decade", response_model=list[DecadeStat],
            summary="Album count grouped by decade")
async def get_albums_by_decade(service: NavidromeDep):
    return await service.get_albums_by_decade()


@router.get("/insights/format-counts", response_model=dict[str, int],
            summary="Song count by audio format")
async def get_format_counts(service: NavidromeDep):
    return await service.get_format_counts()


@router.get("/insights/most-prolific-artists", response_model=ChartData,
            summary="Most prolific artists by album count")
async def get_most_prolific_artists(service: NavidromeDep):
    return await service.get_most_prolific_artists()


@router.get("/insights/longest-albums", response_model=ChartData,
            summary="Top longest albums by duration")
async def get_longest_albums(service: NavidromeDep):
    return await service.get_longest_albums()


@router.get("/insights/most-played-artists", response_model=ChartData,
            summary="Most played artists by total play count")
async def get_most_played_artists(service: NavidromeDep):
    return await service.get_most_played_artists()


@router.get("/insights/library-duration", response_model=LibraryDurationData,
            summary="Total and average library duration")
async def get_library_duration(service: NavidromeDep):
    return await service.get_library_duration()


@router.get("/insights/never-played", response_model=NeverPlayedData,
            summary="Count of never played albums and songs")
async def get_never_played(service: NavidromeDep):
    return await service.get_never_played()


@router.get("/insights/top-played-songs", response_model=ChartData,
            summary="Top played songs by play count")
async def get_top_played_songs(service: NavidromeDep):
    return await service.get_top_played_songs()


@router.get("/insights/artist-dominance", response_model=ChartData,
            summary="Library share of top artists by album count")
async def get_artist_dominance(service: NavidromeDep):
    return await service.get_artist_dominance()