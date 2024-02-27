from datetime import datetime
from typing import Optional

from infra_basic.basic_model import BasicModel
from infra_utility.base_plus_model import BasePlusModel


class FileVm(BasicModel):
    file_name: Optional[str]
    relationship_handled_at: Optional[datetime]
    object_name: str
    bucket_name: str


class FileNameViewModel(BasePlusModel):
    id: str
    original_name: str
    display_name: Optional[str]


class FileBytesVm(BasePlusModel):
    """
    待压缩文件
    """

    file_name: str
    file_bytes: bytes
