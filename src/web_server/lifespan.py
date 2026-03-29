from contextlib import asynccontextmanager

from fastapi import FastAPI

from navidrome_client import NavidromeService, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    service = NavidromeService(get_settings())
    await service.open()
    app.state.navidrome = service
    yield
    await service.close()

