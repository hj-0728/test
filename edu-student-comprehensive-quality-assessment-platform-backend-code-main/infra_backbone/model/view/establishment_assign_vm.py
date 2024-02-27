from datetime import datetime
from typing import Optional

from infra_basic.basic_model import BasicModel


class EstablishmentAssignVm(BasicModel):
    establishment_id: str
    people_id: str
    comments: Optional[str]
    seq: int = 1
    started_on: Optional[datetime]
    ended_on: Optional[datetime]
    dimension_category: str
