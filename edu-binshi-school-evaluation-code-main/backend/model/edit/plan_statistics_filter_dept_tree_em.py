from datetime import datetime
from typing import Optional

from infra_basic.basic_model import BasePlusModel


class PlanStatisticsFilterDeptTreeEditModel(BasePlusModel):
    evaluation_criteria_plan_id: str
    search_text: Optional[str]
    dimension_dept_tree_id: Optional[str]

    compared_time: Optional[datetime]
