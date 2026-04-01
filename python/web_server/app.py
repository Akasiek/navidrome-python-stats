from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx

from web_server.lifespan import lifespan
from web_server.router import register_routers


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    register_routers(app)

    @app.exception_handler(httpx.ConnectError)
    async def connect_error_handler(request: Request, exc: httpx.ConnectError):
        return JSONResponse(
            status_code=503,
            content={"detail": "Cannot connect to Navidrome server", "error": str(exc)},
        )

    return app

