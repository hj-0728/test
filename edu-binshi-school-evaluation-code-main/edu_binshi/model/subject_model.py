"""
科目模型类
"""
from infra_basic.basic_model import VersionedModel


class SubjectModel(VersionedModel):
    """
    科目
    """

    name: str
    is_activated: bool
