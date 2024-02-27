from typing import Optional

from infra_basic.basic_model import VersionedModel


class TeamCategoryModel(VersionedModel):
    """
    小组分类
    """

    name: str
    code: Optional[str]
    is_activated: bool = True
