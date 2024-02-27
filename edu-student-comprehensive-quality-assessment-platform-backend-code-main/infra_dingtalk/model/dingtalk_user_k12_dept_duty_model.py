from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumDingtalkUserK12DeptDutyMap(Enum):
    """
    1表示校区负责人，2表示年级负责人，3表示班主任，4表示任课老师，5表示学段负责人
    """

    SECTION_LEADER = 5
    TEACHER = 4
    HEAD_TEACHER = 3
    GRADE_PRINCIPAL = 2
    HEAD_OF_CAMPUS = 1


class DingtalkUserK12DeptDutyModel(VersionedModel):
    """
    钉钉用户在k12部门中的职责
    """

    dingtalk_user_id: str
    remote_user_id: Optional[str]
    dingtalk_k12_dept_id: str
    duty: str
    subject: Optional[str]
