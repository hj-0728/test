from datetime import datetime
from typing import List, Optional

from infra_basic.basic_model import BasePlusModel
from infra_utility.datetime_helper import local_now


class PeopleRelationshipViewModel(BasePlusModel):
    subject_people_id: str
    object_people_id: str
    relationship: str
    start_at: datetime = local_now()
    finish_at: Optional[datetime]


class DeptDutyViewModel(BasePlusModel):
    """ """

    dimension_dept_tree_id: Optional[str]
    dimension_category: Optional[str]
    dept_id: Optional[str]
    duty_id: Optional[str]
    duty_code: Optional[str]
    duty_name: Optional[str]
    organization_id: Optional[str]
    comments: Optional[str]


class EstablishmentAssignViewModel(BasePlusModel):
    """
    人员职责维度部门树关系
    """

    establishment_id: Optional[str]
    dimension_dept_tree_id: Optional[str]
    dimension_category: Optional[str]
    dept_id: Optional[str]
    capacity_id: Optional[str]
    capacity_code: Optional[str]
    capacity_name: Optional[str]
    organization_id: Optional[str]
    comments: Optional[str]


class AddPeopleViewModel(BasePlusModel):
    id: Optional[str]
    remote_user_id: str
    name: str
    gender: Optional[str]
    mobile: Optional[str]
    gender_display: Optional[str]
    born_at: Optional[datetime]
    born_at_precision: Optional[str]
    died_at: Optional[datetime]
    died_at_precision: Optional[str]
    is_verified: bool = False
    people_relationship_list: Optional[List[PeopleRelationshipViewModel]]
    establishment_assign_list: Optional[List[EstablishmentAssignViewModel]]
