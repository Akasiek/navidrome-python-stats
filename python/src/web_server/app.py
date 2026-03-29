from fastapi import FastAPI

from web_server.lifespan import lifespan
from web_server.router import register_routers


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    register_routers(app)
    return app

