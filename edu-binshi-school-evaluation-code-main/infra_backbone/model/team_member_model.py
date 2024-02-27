from datetime import datetime
from typing import Optional

from infra_basic.basic_model import VersionedModel


class TeamMemberModel(VersionedModel):
    """
    小组成员
    """

    team_id: str
    people_id: str
    capacity_id: str
    seq: int
    start_at: datetime
    finish_at: Optional[datetime]
