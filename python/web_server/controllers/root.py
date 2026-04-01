from fastapi import APIRouter

from web_server.dependencies import NavidromeDep

router = APIRouter(tags=["root"])

@router.get("/ping")
async def ping(service: NavidromeDep):
    ok = await service.ping()
    return {"status": "ok" if ok else "unreachable"}
