from fastapi import APIRouter

from web_server.dependencies import NavidromeDep

router = APIRouter(prefix="/navidrome", tags=["navidrome"])


@router.get("/ping")
async def ping(service: NavidromeDep):
    ok = await service.ping()
    return {"status": "ok" if ok else "unreachable"}


@router.get("/artists")
async def get_artists(service: NavidromeDep):
    artists = await service.get_artists()
    return {"artists": [a.model_dump() for a in artists]}

