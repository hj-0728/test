"""
command
"""
from typing import List, Optional

from infra_basic.basic_model import BasePlusModel


class SaveEvaluationCriteriaPlanScopeEm(BasePlusModel):
    """
    保存评价标准计划使用范围
    """

    evaluation_criteria_plan_id: Optional[str]
    scope_category: List[str]
    dept_id_list: Optional[List[str]]
    people_id_list: Optional[List[str]]
