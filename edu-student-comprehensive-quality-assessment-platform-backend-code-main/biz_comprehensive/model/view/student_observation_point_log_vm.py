from datetime import datetime
from typing import Optional

from infra_basic.basic_model import BasePlusModel


class StudentObservationPointLogViewModel(BasePlusModel):
    id: str
    observation_action_performer_name: str
    observation_on: datetime
    comment: Optional[str]
    observation_point_name: str
    observation_point_icon: str
