from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumContextPeopleUserMapResCategory(Enum):
    """
    上下文人用户关联类型
    """

    DINGTALK_K12_STUDENT = "钉钉k12学生"
    DINGTALK_K12_PARENT = "钉钉k12家长"
    DINGTALK_USER = "钉钉用户"


class ContextPeopleUserMapModel(VersionedModel):
    """
    上下文人用户关联
    """

    people_id: str
    res_category: str
    res_id: str
