from datetime import datetime
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


class Resource(BaseModel):
    link: HttpUrl
    title: str


class CourseOutline(BaseModel):
    slug: str
    chapters: List[Resource]
    materials: List[Resource]
    number_of_chapters: int
    number_of_materials: int


class VideoInformation(BaseModel):
    name: str
    page_url: HttpUrl
    context: Union[HttpUrl, str, None] = None
    type: Union[str, None] = None
    description: Union[str, None] = None
    thumbnailUrl: List[Union[HttpUrl, str, None]] = list()
    uploadDate: Union[datetime, None] = None
    embedUrl: HttpUrl
    projector_key: str
    video_url: HttpUrl
    transcript_url: HttpUrl
