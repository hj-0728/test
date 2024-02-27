from datetime import datetime

from infra_basic.basic_model import BasicModel


class TeamMemberViewModel(BasicModel):
    id: str
    version: int
    team_id: str
    people_id: str
    people_name: str
    capacity_id: str
    capacity_name: str
    start_at: datetime
    finish_at: datetime
    seq: int
