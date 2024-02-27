from typing import List, Optional

from infra_basic.basic_model import BasicModel

from infra_backbone.model.view.team_goal_vm import TeamGoalViewModel


class TeamViewModel(BasicModel):
    """
    小组
    """

    id: str
    version: int = 1
    name: str
    create_people_name: Optional[str]
    team_category_id: Optional[str]
    team_goal: Optional[str]
    is_self_create: bool = False
    member_list: List[str] = []

    team_goal_list: List[TeamGoalViewModel] = []
