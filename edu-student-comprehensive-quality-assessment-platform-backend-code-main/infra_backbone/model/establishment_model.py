from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EstablishmentModel(VersionedModel):
    dimension_dept_tree_id: str
    capacity_id: str
    seq: Optional[int]
    comments: Optional[str]
    started_on: Optional[datetime]
    ended_on: Optional[datetime]
