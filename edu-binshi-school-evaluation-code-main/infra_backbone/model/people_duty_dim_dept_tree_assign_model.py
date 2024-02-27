from datetime import datetime
from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class PeopleDutyDimDeptTreeAssignModel(VersionedModel):
    dimension_dept_tree_id: str
    duty_id: str
    seq: int = 1
    comments: Optional[str]
    people_id: str
    start_at: Optional[datetime]
    finish_at: Optional[datetime]

    duty_code: Optional[str]
    duty_name: Optional[str]
