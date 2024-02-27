from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumDingtalkK12FamilyRelationshipCode(Enum):
    """
    学生家长关系
    """

    FATHER = "爸爸"
    MOTHER = "妈妈"
    GRANDFATHER = "爷爷"
    GRANDMOTHER = "奶奶"
    MATERNAL_GRANDMOTHER = "外公"
    MATERNAL_GRANDFATHER = "外婆"
    ELDER_BROTHER = "哥哥"
    YOUNGER_BROTHER = "弟弟"
    ELDER_SISTER = "姐姐"
    YOUNGER_SISTER = "妹妹"


class DingtalkK12FamilyRelationshipModel(VersionedModel):
    """
    学生家长关系
    """

    dingtalk_k12_student_id: str
    dingtalk_k12_parent_id: str
    relationship_code: str
    relationship_name: str
    parent_remote_user_id: Optional[str]
