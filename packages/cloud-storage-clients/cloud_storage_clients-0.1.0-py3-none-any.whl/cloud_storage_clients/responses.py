from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class GetResponse:
    content: bytes


@dataclass
class HeadResponse:
    file_size: int
    content_type: Optional[str]


@dataclass
class PutResponse:
    info: Optional[dict]


@dataclass
class DeleteResponse:
    info: Optional[dict]


@dataclass
class CopyResponse:
    info: Optional[dict]


@dataclass
class BucketFolder:
    name: str


@dataclass
class BucketFile:
    name: str
    last_modified: datetime
    size: int


@dataclass
class BucketObjects:
    folders: list[BucketFolder]
    files: list[BucketFile]


@dataclass
class ListResponse:
    bucket_objects: BucketObjects


@dataclass
class GetDownloadUrlResponse:
    url: str


@dataclass
class GetUploadUrlResponse:
    url: str
    fields: dict


@dataclass
class CreateMultipartUploadResponse:
    upload_id: str


@dataclass
class GetPartUploadUrlResponse:
    url: str


@dataclass
class CompleteMultipartUploadResponse:
    info: Optional[dict]
