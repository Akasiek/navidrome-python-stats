from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import httpx

from .auth import build_auth_params
from .config import NavidromeConfig
from .exceptions import NavidromeError


class NavidromeClient:
    def __init__(self, config: NavidromeConfig) -> None:
        self.config = config
        self.http: httpx.AsyncClient | None = None

    async def open(self) -> None:
        self.http = httpx.AsyncClient(
            base_url=self.config.url,
            timeout=httpx.Timeout(10.0),
        )

    async def close(self) -> None:
        if self.http is not None:
            await self.http.aclose()
            self.http = None

    async def __aenter__(self) -> "NavidromeClient":
        await self.open()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()

    def build_navidrome_url(self, endpoint: str, is_rest: bool = True, extra_params: dict[str, Any] | None = None) -> str:
        if is_rest:
            params = build_auth_params(self.config)
        else:
            params = {}
        if extra_params:
            params.update(extra_params)
        url = self.config.url.rstrip("/") + ("/rest" if is_rest else "/app/#")
        url = f"{url}/{endpoint}"
        if extra_params:
            url += f"?{urlencode(extra_params)}"
        return url

    async def request(
        self,
        method_name: str,
        extra_params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if self.http is None:
            raise RuntimeError("NavidromeClient is not open")

        params = build_auth_params(self.config)
        if extra_params:
            params.update(extra_params)

        response = await self.http.get(f"/rest/{method_name}", params=params)
        response.raise_for_status()

        body: dict[str, Any] = response.json()
        # TODO
        # TODO check what we got
        # TODO
        subsonic = body.get("subsonic-response", {})

        if subsonic.get("status") != "ok":
            error = subsonic.get("error", {})
            raise NavidromeError(
                code=error.get("code", -1),
                message=error.get("message", "Unknown error"),
            )

        return subsonic
