from typing import Optional, List

from domain_evaluation.model.evaluation_criteria_plan_scope_model import EvaluationCriteriaPlanScopeCategoryModal, \
    EvaluationCriteriaPlanScopeModel
from domain_evaluation.repository.evaluation_criteria_plan_repository import (
    EvaluationCriteriaPlanRepository,
)
from domain_evaluation.repository.evaluation_criteria_plan_scope_repository import (
    EvaluationCriteriaPlanScopeRepository,
)


class EvaluationCriteriaPlanScopeService:
    """
    评价标准计划适用的集合 service
    """

    def __init__(
        self,
        evaluation_criteria_plan_scope_repository: EvaluationCriteriaPlanScopeRepository,
        evaluation_criteria_plan_repository: EvaluationCriteriaPlanRepository,
    ):
        self.__evaluation_criteria_plan_scope_repository = evaluation_criteria_plan_scope_repository
        self.__evaluation_criteria_plan_repository = evaluation_criteria_plan_repository

    def get_plan_scope_by_plan_id(self, plan_id: str) -> List[EvaluationCriteriaPlanScopeCategoryModal]:
        """
        根据plan_id获取评价计划适用的集合
        :param plan_id:
        :return:
        """
        return self.__evaluation_criteria_plan_scope_repository.get_plan_scope_by_plan_id(
            plan_id=plan_id
        )

    def get_evaluation_criteria_plan_scope_list_by_plan_id(
        self, evaluation_criteria_plan_id: str, scope_category: Optional[str]
    ) -> List[EvaluationCriteriaPlanScopeModel]:
        """
        根据plan_id获取评价计划适用集合列表
        :param evaluation_criteria_plan_id:
        :param scope_category:
        """
        return self.__evaluation_criteria_plan_scope_repository.get_evaluation_criteria_plan_scope_list_by_plan_id(
            evaluation_criteria_plan_id=evaluation_criteria_plan_id, scope_category=scope_category
        )
