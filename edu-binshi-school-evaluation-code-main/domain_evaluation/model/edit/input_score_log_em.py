from typing import Optional

from infra_utility.base_plus_model import BasePlusModel


class InputScoreLogEditModel(BasePlusModel):
    id: str
    version: int
    people_id: Optional[str]
    numeric_score: Optional[float]
    string_score: Optional[str]
    evaluation_criteria_plan_id: str
