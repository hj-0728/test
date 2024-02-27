from datetime import datetime
from typing import Optional, List

from infra_utility.base_plus_model import BasePlusModel


class K12TeacherSubjectVm(BasePlusModel):
    """
    教师 vm
    """

    id: str
    version: int
    people_id: str
    dimension_dept_tree_id: str
    subject_id: str
    start_at: Optional[datetime]
    finish_at: Optional[datetime]
    subject_name: Optional[str]

    people_name: Optional[str]


class FiltersVm(BasePlusModel):
    """
    过滤 vm
    """
    text: str
    value: str


class K12TeacherSubjectFiltersVm(BasePlusModel):
    """
    教师科目过滤 vm
    """
    subject_filters: List[FiltersVm] = []
    capacity_filters: List[FiltersVm] = []
