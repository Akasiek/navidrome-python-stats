from fastapi import FastAPI

from web_server.controllers.albums import router as albums_router
from web_server.controllers.root import router as root_router
from web_server.controllers.statistics import router as statistics_router


def register_routers(app: FastAPI) -> None:
    app.include_router(root_router)
    app.include_router(albums_router)
    app.include_router(statistics_router)

