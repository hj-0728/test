from datetime import datetime
from typing import Optional

from infra_basic.basic_model import BasePlusModel


class ObservationLogViewModel(BasePlusModel):
    observation_action_id: str
    observee_name: str
    observation_on: datetime
    comment: Optional[str]
    observation_point_name: str
    observation_point_icon: str
    is_self: bool = False
