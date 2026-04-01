from fastapi import FastAPI

from web_server.controllers.albums import router as albums_router
from web_server.controllers.insights import router as insights_router
from web_server.controllers.root import router as root_router
from web_server.controllers.stats import router as stats_router


def register_routers(app: FastAPI) -> None:
    app.include_router(root_router)
    app.include_router(albums_router)
    app.include_router(stats_router)
    app.include_router(insights_router)

