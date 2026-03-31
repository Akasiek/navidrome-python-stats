from fastapi import APIRouter

from web_server.dependencies import NavidromeDep
from web_server.models.insights import InsightsData

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("", summary="Insights data", response_model=InsightsData)
async def get_insights(service: NavidromeDep):
    return await service.get_insights()
