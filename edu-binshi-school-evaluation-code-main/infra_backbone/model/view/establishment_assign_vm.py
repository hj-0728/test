from datetime import datetime
from typing import Optional

from infra_basic.basic_model import BasicModel


class EstablishmentAssignVm(BasicModel):
    establishment_id: str
    people_id: str
    comments: Optional[str]
    seq: int = 1
    start_at: Optional[datetime]
    finish_at: Optional[datetime]
    dimension_category: str
