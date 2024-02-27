from datetime import datetime
from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumSearchScene(Enum):
    MOBILE_STUDENT = "手机端搜索学生"


class SearchHistoryModel(VersionedModel):
    """
    搜索历史
    """

    owner_people_id: str
    search_content: str
    search_on: datetime
    search_scene: str
