from fastapi import APIRouter

from navidrome_client.service import AlbumListType
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


@router.get("/albums")
async def get_albums(
    service: NavidromeDep,
    list_type: AlbumListType = "alphabeticalByName",
    size: int = 50,
    offset: int = 0,
):
    albums = await service.get_albums(list_type=list_type, size=size, offset=offset)  # type: ignore[arg-type]
    return {"albums": [a.model_dump() for a in albums]}


@router.get("/albums/{album_id}/songs")
async def get_songs(album_id: str, service: NavidromeDep):
    songs = await service.get_songs(album_id)
    return {"songs": [s.model_dump() for s in songs]}
