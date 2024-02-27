import datetime
from typing import List

from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now

from backend.model.edit.save_evaluation_criteria_plan_scope_em import (
    SaveEvaluationCriteriaPlanScopeEm,
)
from backend.service.app_evaluation_assignment_service import AppEvaluationAssignmentService
from domain_evaluation.model.evaluation_criteria_plan_model import (
    EvaluationCriteriaPlanModel,
)
from domain_evaluation.model.evaluation_criteria_plan_scope_model import (
    EnumGroupCategory,
    EvaluationCriteriaPlanScopeModel,
)
from domain_evaluation.repository.evaluation_criteria_plan_repository import (
    EvaluationCriteriaPlanRepository,
)
from domain_evaluation.repository.evaluation_criteria_plan_scope_repository import (
    EvaluationCriteriaPlanScopeRepository,
)
from domain_evaluation.service.evaluation_criteria_plan_scope_service import (
    EvaluationCriteriaPlanScopeService,
)
from infra_backbone.repository.dept_repository import DeptRepository
from infra_backbone.repository.establishment_assign_repository import \
    EstablishmentAssignRepository


class AppEvaluationCriteriaPlanScopeService:
    """
    评价标准计划适用的集合 service
    """

    def __init__(
        self,
        evaluation_criteria_plan_scope_repository: EvaluationCriteriaPlanScopeRepository,
        evaluation_criteria_plan_repository: EvaluationCriteriaPlanRepository,
        app_evaluation_assignment_service: AppEvaluationAssignmentService,
        evaluation_criteria_plan_scope_service: EvaluationCriteriaPlanScopeService,
        dept_repository: DeptRepository,
        establishment_assign_repository: EstablishmentAssignRepository,
    ):
        self.__evaluation_criteria_plan_scope_repository = evaluation_criteria_plan_scope_repository
        self.__evaluation_criteria_plan_repository = evaluation_criteria_plan_repository
        self.__app_evaluation_assignment_service = app_evaluation_assignment_service
        self.__evaluation_criteria_plan_scope_service = evaluation_criteria_plan_scope_service
        self.__dept_repository = dept_repository
        self.__establishment_assign_repository = establishment_assign_repository

    def save_evaluation_criteria_plan_scope(
        self,
        data: SaveEvaluationCriteriaPlanScopeEm,
        transaction: Transaction,
        evaluation_criteria_plan: EvaluationCriteriaPlanModel = None,
    ):
        """
        保存评价标准计划适用集合
        :param data:
        :param evaluation_criteria_plan:
        :param transaction:
        """
        evaluation_criteria_plan_vm = (
            self.__evaluation_criteria_plan_repository.fetch_evaluation_criteria_plan_by_id(
                evaluation_criteria_plan_id=data.evaluation_criteria_plan_id
            )
        )

        if evaluation_criteria_plan_vm is None:
            evaluation_criteria_plan_vm = evaluation_criteria_plan

        # 用字典存储不同scope_category对应的ids
        scope_ids = {
            EnumGroupCategory.PERSONAL.name: data.people_id_list,
            EnumGroupCategory.DEPT.name: data.dept_id_list,
        }

        evaluation_criteria_plan_scope_list = []

        for category in [EnumGroupCategory.PERSONAL.name, EnumGroupCategory.DEPT.name]:
            if category in data.scope_category:
                # 如果传入的scope_category中包含PERSONAL或DEPT则进行更新
                evaluation_criteria_plan_scope_list += self.update_evaluation_criteria_plan_scope(
                    evaluation_criteria_plan_id=evaluation_criteria_plan_vm.id,
                    scope_category=category,
                    scope_ids=scope_ids[category],
                    transaction=transaction,
                )

            else:
                # 若不包含则删除
                self.end_evaluation_criteria_plan_scope(
                    evaluation_criteria_plan_id=evaluation_criteria_plan_vm.id,
                    scope_category=category,
                    transaction=transaction,
                )
        return evaluation_criteria_plan_vm, evaluation_criteria_plan_scope_list

    def update_evaluation_criteria_plan_scope(
        self,
        evaluation_criteria_plan_id: str,
        scope_category: str,
        scope_ids: List[str],
        transaction: Transaction,
    ) -> List[EvaluationCriteriaPlanScopeModel]:

        scope_list = self.__evaluation_criteria_plan_scope_repository.get_plan_scope_by_plan_id_and_scope(
            evaluation_criteria_plan_id=evaluation_criteria_plan_id,
            scope_category=scope_category,
        )

        db_scope_id_set = set(
            [obj.scope_id for obj in scope_list]
        )

        scope_id_list = []

        # 只保存未被删除的 scope
        if scope_category == EnumGroupCategory.DEPT.name:
            dept_list = self.__dept_repository.get_current_dept_by_ids(
                dept_ids=scope_ids
            )
            scope_id_list = [x.id for x in dept_list]

        if scope_category == EnumGroupCategory.PERSONAL.name:
            establishment_assign_list = (
                self.__establishment_assign_repository.get_current_people_establishment_assign_by_establishment_assign_ids(
                    establishment_assign_ids=scope_ids
                )
            )
            scope_id_list = [x.id for x in establishment_assign_list]

        scope_id_set = set(scope_id_list)
        need_add_scope = scope_id_set - db_scope_id_set
        evaluation_criteria_plan_scope_list = [x for x in scope_list if x.scope_id in scope_id_list]

        for scope_id in need_add_scope:
            data = EvaluationCriteriaPlanScopeModel(
                evaluation_criteria_plan_id=evaluation_criteria_plan_id,
                scope_category=scope_category,
                scope_id=scope_id,
                start_at=local_now(),
            )

            self.__evaluation_criteria_plan_scope_repository.insert_evaluation_criteria_plan_scope(
                data=data, transaction=transaction
            )

            evaluation_criteria_plan_scope_list.append(data)

        # 删除（更改finish_at）
        items_in_scope_not_in_establishment = db_scope_id_set - scope_id_set
        if items_in_scope_not_in_establishment:
            scope_dict = {x.scope_id: x for x in scope_list}
            for scope_id in items_in_scope_not_in_establishment:
                db_scope = scope_dict.get(scope_id)
                if db_scope:
                    db_scope.finish_at = local_now()
                    self.__evaluation_criteria_plan_scope_repository.update_evaluation_criteria_plan_scope(
                        data=db_scope,
                        transaction=transaction,
                        limited_col_list=["finish_at"],
                    )
        return evaluation_criteria_plan_scope_list

    def end_evaluation_criteria_plan_scope(
        self, evaluation_criteria_plan_id: str, scope_category: str, transaction: Transaction
    ):
        evaluation_criteria_plan_scope_id_list = self.__evaluation_criteria_plan_scope_service.get_evaluation_criteria_plan_scope_list_by_plan_id(
            evaluation_criteria_plan_id=evaluation_criteria_plan_id, scope_category=scope_category
        )
        for scope_info in evaluation_criteria_plan_scope_id_list:
            scope_info.finish_at = local_now()
            self.__evaluation_criteria_plan_scope_repository.update_evaluation_criteria_plan_scope(
                data=scope_info,
                transaction=transaction,
                limited_col_list=["finish_at"],
            )
