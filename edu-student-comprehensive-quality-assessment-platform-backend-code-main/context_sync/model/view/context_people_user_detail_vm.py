from typing import List, Optional

from infra_basic.basic_model import BasePlusModel


class ContextPeopleUserDetailViewModel(BasePlusModel):
    """
    上下文人和家长详情
    """

    id: str
    people_id: str
    res_id: str
    people_version: int
    name: str
    is_activated: bool
    second_user_id: Optional[str]


class StudentFamilyRelationshipViewModel(BasePlusModel):
    parent_id: Optional[str]
    relationship: Optional[str]


class ContextPeopleStudentDetailViewModel(ContextPeopleUserDetailViewModel):
    """
    上下文人和学生详情
    """

    dept_id_list: List[str]
    family_relationship: List[StudentFamilyRelationshipViewModel]
