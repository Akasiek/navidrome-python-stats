from __future__ import annotations
from typing import Annotated, TYPE_CHECKING
from fastapi import Depends, Request
from navidrome_client.service import NavidromeService


def get_navidrome(request: Request) -> NavidromeService:
    return request.app.state.navidrome


NavidromeDep = Annotated[NavidromeService, Depends(get_navidrome)]
