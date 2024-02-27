from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel


class DimensionDeptTreeModel(VersionedModel):
    dimension_id: Optional[str]
    dept_id: str
    parent_dept_id: Optional[str]
    seq: Optional[str]
    start_at: Optional[datetime]
    finish_at: Optional[datetime]
