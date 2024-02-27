from datetime import datetime
from typing import Optional

from infra_basic.basic_model import BasicModel


class TeamGoalViewModel(BasicModel):
    id: str
    version: int
    goal_name: Optional[str]
    team_name: Optional[str]
    team_id: str
    goal_id: str
    goal_category: str
    activity: str
    start_at: datetime
    finish_at: Optional[datetime]
