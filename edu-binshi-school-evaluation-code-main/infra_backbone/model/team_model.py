from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel
from infra_utility.datetime_helper import local_now


class TeamModel(VersionedModel):
    """
    小组
    """

    team_category_id: Optional[str]
    name: str
    start_at: datetime = local_now()
    finish_at: Optional[datetime]
