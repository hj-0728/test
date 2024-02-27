from datetime import datetime
from typing import List, Optional

from infra_utility.base_plus_model import BasePlusModel
from infra_utility.datetime_helper import local_now

from infra_backbone.model.edit.team_goal_em import TeamGoalEditModel


class TeamEditModal(BasePlusModel):
    """
    小组编辑模型
    """

    id: Optional[str]
    version: int = 1
    name: str
    team_category_id: str
    start_at: datetime = local_now()
    finish_at: Optional[datetime]
    team_goal_list: List[TeamGoalEditModel] = []
