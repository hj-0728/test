from datetime import datetime
from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel
from infra_utility.datetime_helper import local_now


class EnumTeamGoalCategory(Enum):
    """
    小组目标分类
    """

    DIMENSION_DEPT_TREE = "DIMENSION_DEPT_TREE"


class EnumTeamGoalActivity(Enum):
    """
    小组目标活动
    """

    EVALUATION = "评价"


class EnumTeamCategory(Enum):
    """
    名称、目标
    """

    NAME = "名称"
    GOAL = "目标"


class TeamGoalModel(VersionedModel):
    team_id: str
    goal_category: str
    goal_id: str
    activity: str = EnumTeamGoalActivity.EVALUATION.name
    start_at: datetime = local_now()
    finish_at: Optional[datetime]
