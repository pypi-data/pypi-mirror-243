from typing import Optional

from pydantic import BaseModel


class Size(BaseModel):
    height: Optional[int] = None
    type: Optional[str] = None
    width: Optional[int] = None
    url: Optional[str] = None


class Photo(BaseModel):
    album_id: int
    date: int
    id: int
    owner_id: int
    access_key: Optional[str] = ""
    sizes: list[Size]


class Image(BaseModel):
    url: str
    width: int
    height: int
    with_padding: Optional[int] = None
