from __future__ import annotations
from pydantic import BaseModel, Field


class Artist(BaseModel):
    id: str
    name: str
    album_count: int = Field(0)

    model_config = {"populate_by_name": True}
