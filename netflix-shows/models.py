from pydantic import BaseModel
from datetime import date
from typing import List


class Shows(BaseModel):
    show_id: int
    type: str
    title: str
    director: str
    cast: str
    country: str
    date_added: date
    release_year: int
    rating: str
    duration: str
    listed_in: str
    description: str


class ShowModify(BaseModel):
    type: str
    title: str
    director: str
    cast: str
    country: str
    date_added: date
    release_year: int
    rating: str
    duration: str
    listed_in: str
    description: str


class ShowsSearch(BaseModel):
    length: int
    data: List[Shows]

