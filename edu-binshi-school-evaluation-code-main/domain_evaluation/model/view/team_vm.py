from infra_basic.basic_model import BasePlusModel


class TeamViewModel(BasePlusModel):
    team_id: str
    team_name: str
    goal_category: str
    goal_id: str
    activity: str
    team_category_id: str
    team_category_name: str
