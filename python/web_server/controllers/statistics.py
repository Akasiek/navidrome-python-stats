from fastapi import APIRouter

from web_server.dependencies import NavidromeDep
from web_server.models.statistics import InsightsData, LibraryStats

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("", response_model=LibraryStats,
            summary="Library primary statistics",
            description="Get primary statistics about the library, such as total songs, albums, artists, and total duration.")
async def get_library_stats(service: NavidromeDep):
    return await service.get_library_stats()


@router.get("/insights", summary="Insights data", response_model=InsightsData)
async def get_insights(service: NavidromeDep):
    return await service.get_insights()