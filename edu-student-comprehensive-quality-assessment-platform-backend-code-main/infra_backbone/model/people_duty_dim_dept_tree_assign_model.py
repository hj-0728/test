from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel


class PeopleDutyDimDeptTreeAssignModel(VersionedModel):
    dimension_dept_tree_id: str
    duty_id: str
    seq: int = 1
    comments: Optional[str]
    people_id: str
    started_on: Optional[datetime]
    ended_on: Optional[datetime]

    duty_code: Optional[str]
    duty_name: Optional[str]
