from typing import Optional

from infra_utility.base_plus_model import BasePlusModel


class EvaluationRecordEditModel(BasePlusModel):
    """
    评价记录
    """

    evaluation_criteria_id: str
    evaluation_assignment_id: str
    evaluation_criteria_plan_id: str
    people_id: Optional[str]
