from datetime import datetime
from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumPerformerResCategory(str, Enum):
    PEOPLE = "人员"


class ObservationActionModel(VersionedModel):
    observation_require_id: Optional[str]
    performer_res_category: str
    performer_res_id: str
    performed_started_on: Optional[datetime]
    performed_ended_on: Optional[datetime]
