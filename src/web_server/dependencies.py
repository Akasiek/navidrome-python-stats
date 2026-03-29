from typing import Annotated

from fastapi import Depends, Request

from navidrome_client import NavidromeService


def get_navidrome(request: Request) -> NavidromeService:
    return request.app.state.navidrome


NavidromeDep = Annotated[NavidromeService, Depends(get_navidrome)]

