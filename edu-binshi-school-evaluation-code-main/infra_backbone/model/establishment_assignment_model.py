from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EstablishmentAssignmentModel(VersionedModel):
    establishment_id: str
    people_id: str
    comments: Optional[str]
    start_at: datetime
    finish_at: datetime
