from datetime import datetime
from typing import Optional

from infra_utility.base_plus_model import BasePlusModel
from infra_utility.datetime_helper import local_now


class TeamGoalEditModel(BasePlusModel):
    team_id: Optional[str]
    goal_id: str
    goal_category: str
    activity: str
    start_at: datetime = local_now()
    finish_at: Optional[datetime]
