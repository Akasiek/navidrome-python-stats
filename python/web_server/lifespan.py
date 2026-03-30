from contextlib import asynccontextmanager
from fastapi import FastAPI
from navidrome_client.config import get_settings
from navidrome_client.service import NavidromeService


@asynccontextmanager
async def lifespan(app: FastAPI):
    service = NavidromeService(get_settings())
    await service.open()
    app.state.navidrome = service
    yield
    await service.close()

