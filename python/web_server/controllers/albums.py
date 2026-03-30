from fastapi import APIRouter, Query

from web_server.dependencies import NavidromeDep

router = APIRouter(prefix="/albums", tags=["albums"])

_SIZE = Query(20, ge=1, le=100, description="Number of albums to return")
_OFFSET = Query(0, ge=0, description="Offset (pagination)")


@router.get("/newest", summary="Newest albums")
async def get_newest_albums(
    service: NavidromeDep,
    size: int = _SIZE,
    offset: int = _OFFSET,
):
    albums = await service.get_newest_albums(size=size, offset=offset)
    return {"albums": [a.model_dump() for a in albums]}


@router.get("/frequent", summary="Most frequently listened albums")
async def get_frequent_albums(
    service: NavidromeDep,
    size: int = _SIZE,
    offset: int = _OFFSET,
):
    albums = await service.get_frequent_albums(size=size, offset=offset)
    return {"albums": [a.model_dump() for a in albums]}


@router.get("/starred", summary="User's favorite albums")
async def get_starred_albums(
    service: NavidromeDep,
    size: int = _SIZE,
    offset: int = _OFFSET,
):
    albums = await service.get_starred_albums(size=size, offset=offset)
    return {"albums": [a.model_dump() for a in albums]}


@router.get("/recent", summary="Recently listened albums")
async def get_recent_albums(
    service: NavidromeDep,
    size: int = _SIZE,
    offset: int = _OFFSET,
):
    albums = await service.get_recent_albums(size=size, offset=offset)
    return {"albums": [a.model_dump() for a in albums]}


@router.get("/top-rated", summary="Highest rated albums")
async def get_top_rated_albums(
    service: NavidromeDep,
    size: int = _SIZE,
    offset: int = _OFFSET,
):
    albums = await service.get_top_rated_albums(size=size, offset=offset)
    return {"albums": [a.model_dump() for a in albums]}


@router.get("/{album_id}/songs", summary="Album songs")
async def get_album_songs(album_id: str, service: NavidromeDep):
    songs = await service.get_songs(album_id)
    return {"songs": [s.model_dump() for s in songs]}

