from typing import Optional

from infra_basic.basic_model import BasePlusModel


class PeopleDutyDimDeptTreeAssignViewModel(BasePlusModel):
    id: str
    dimension_dept_tree_id: str
    duty_id: str
    seq: int = 1
    comments: Optional[str]
    people_id: str
    dimension_category: str
