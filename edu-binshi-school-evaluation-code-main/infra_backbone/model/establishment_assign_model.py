from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EstablishmentAssignModel(VersionedModel):
    establishment_id: str
    people_id: str
    comments: Optional[str]
    seq: int = 1
    start_at: Optional[datetime]
    finish_at: Optional[datetime]
