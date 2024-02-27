from datetime import datetime
from os import path
from typing import Dict, Optional

from infra_basic.basic_model import BasicModel
from pydantic import root_validator


class FileViewModel(BasicModel):
    id: Optional[str]
    file_name: Optional[str]
    download_url: Optional[str]
    is_image: bool = False

    @root_validator
    def check_is_image(cls, value: Dict) -> Dict:
        # pylint: disable=C0103, E0213
        if not value["file_name"]:
            return value
        image_suffix = (
            ".jpg",
            ".png",
            ".gif",
            ".bmp",
            ".jpeg",
            ".jfif",
            ".tif",
            ".pcx",
            ".tga",
            ".exif",
            ".fpx",
            ".svg",
            ".psd",
            ".cdr",
            ".pcd",
            ".dxf",
            ".ufo",
            ".eps",
            ".ai",
            ".raw",
            ".wmf",
            ".webp",
            ".avif",
            ".tiff",
            ".pjp",
            ".pjpeg",
            ".svgz",
            ".ico",
            ".xbm",
            ".dib",
        )
        file_ext = path.splitext(value["file_name"])[1]
        value["is_image"] = file_ext.lower() in image_suffix
        return value


class FileVm(BasicModel):
    file_name: Optional[str]
    relationship_handled_at: Optional[datetime]
    object_name: str
    bucket_name: str
