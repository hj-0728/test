from typing import Optional, List

from infra_utility.base_plus_model import BasePlusModel


class K12TeacherVm(BasePlusModel):
    """
    教师 vm
    """

    people_name: str
    dept_name: str
    people_id: str
    dimension_dept_tree_id: str
    capacity_name: str
    subject_name: Optional[str]
    dept_name_list: List[str] = []
