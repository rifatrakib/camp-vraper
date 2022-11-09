from typing import List, Union
from urllib.parse import urlparse

from pydantic import BaseModel, HttpUrl, validator


def resolve_relative_url(url):
    if not bool(urlparse(url).netloc):
        return None
    return url


class Instructor(BaseModel):
    id: int
    name: str
    url: Union[HttpUrl, str, None] = None
    biography: Union[str, None] = None
    imageUrl: Union[HttpUrl, str, None] = None
    marketingBiography: Union[str, None] = None

    @validator("url")
    def validate_url(cls, value):
        return resolve_relative_url(value)

    @validator("imageUrl")
    def validate_image_url(cls, value):
        return resolve_relative_url(value)


class Category(BaseModel):
    id: int
    name: str


class Course(BaseModel):
    id: int
    instructors: List[Instructor]
    link: HttpUrl
    shortDescription: Union[str, None] = None
    slug: Union[str, None] = None
    technologies: List[Category]
    timeNeededInHours: Union[int, None] = None
    title: str
