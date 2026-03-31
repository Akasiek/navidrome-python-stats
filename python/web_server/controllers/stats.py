from fastapi import APIRouter

from web_server.dependencies import NavidromeDep
from web_server.models.stats import LibraryStats

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("", summary="Library statistics", response_model=LibraryStats)
async def get_library_stats(service: NavidromeDep):
    return await service.get_library_stats()
