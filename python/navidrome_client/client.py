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
        self.api_token: str | None = None

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
        params = build_auth_params(self.config) if is_rest else {}
        if extra_params:
            params.update(extra_params)

        base = (self.config.external_url or self.config.url).rstrip("/")
        url = base + ("/rest" if is_rest else "/app/#")
        url = f"{url}/{endpoint}"
        if params:
            url += "?" + urlencode(params)
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
        subsonic = body.get("subsonic-response", {})

        if subsonic.get("status") != "ok":
            error = subsonic.get("error", {})
            raise NavidromeError(
                code=error.get("code", -1),
                message=error.get("message", "Unknown error"),
            )

        return subsonic

    async def fetch_cover_art(self, cover_id: str) -> tuple[bytes, str]:
        if self.http is None:
            raise RuntimeError("NavidromeClient is not open")
        params = build_auth_params(self.config)
        params["id"] = cover_id
        response = await self.http.get("/rest/getCoverArt", params=params)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "image/jpeg")
        return response.content, content_type

    async def request_api(
        self,
        method_name: str,
        extra_params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if self.http is None:
            raise RuntimeError("NavidromeClient is not open")

        headers = {"X-ND-Authorization": f"Bearer {self.get_api_token()}"}
        params = {}
        if extra_params:
            params.update(extra_params)

        response = await self.http.get(f"/api/{method_name}", headers=headers, params=params)
        response.raise_for_status()

        body = response.json()
        headers = response.headers

        return {
            "body": body,
            "headers": headers,
        }

    def get_api_token(self) -> str:
        if self.api_token is not None:
            return self.api_token
        payload = {
            "username": self.config.user,
            "password": self.config.password,
        }
        response = httpx.post(f"{self.config.url}/auth/login", json=payload, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        token = data.get("token")
        if not token:
            raise NavidromeError(code=-1, message="Failed to retrieve API token")
        self.api_token = token
        return token

    def refresh_api_token(self) -> str:
        self.api_token = None
        return self.get_api_token()
