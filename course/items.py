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


class Subtitle(BaseModel):
    language: str
    link: HttpUrl


class VideoAdditives(BaseModel):
    page_url: HttpUrl
    video_mp4_link: HttpUrl
    video_hls_link: Union[bool, None] = None
    audio_link: Union[HttpUrl, str, None] = None
    subtitle_vtt_link: Union[HttpUrl, str, None] = None
    thumbnail_link: Union[HttpUrl, str, None] = None
    is_projector_video: Union[bool, None] = None
    subtitles: List[Subtitle] = []


class VideoInformation(BaseModel):
    name: str
    course_name: str
    chapter_name: str
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
    details: Union[VideoAdditives, None] = None
    visited: bool = False


class Script(BaseModel):
    citations: List[HttpUrl] = []
    number: int
    script: str
    title: str


class Transcript(BaseModel):
    slides: List[Script] = []
    url: HttpUrl
