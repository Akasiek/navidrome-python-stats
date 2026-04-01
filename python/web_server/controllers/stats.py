from fastapi import APIRouter

from web_server.dependencies import NavidromeDep
from web_server.models.stats import LibraryStats

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("", response_model=LibraryStats,
            summary="Library primary statistics",
            description="Get primary statistics about the library, such as total songs, albums, artists, and total duration.")
async def get_library_stats(service: NavidromeDep):
    return await service.get_library_stats()
