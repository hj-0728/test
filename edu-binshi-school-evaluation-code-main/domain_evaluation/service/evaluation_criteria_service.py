from typing import List

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.enum_helper import enum_to_dict_list, get_enum_value_by_name

from domain_evaluation.data.query_params.evaluation_criteria_page_query_params import (
    EvaluationCriteriaPageQueryParams, EvaluationCriteriaListQueryParams,
)
from domain_evaluation.model.evaluation_criteria_model import (
    EnumEvaluationCriteriaStatus,
    EnumEvaluationObjectCategory,
    EvaluationCriteriaModel,
    SaveEvaluationCriteriaModel,
)
from domain_evaluation.model.evaluation_criteria_plan_model import EnumEvaluationCriteriaPlanStatus
from domain_evaluation.repository.evaluation_criteria_plan_repository import (
    EvaluationCriteriaPlanRepository,
)
from domain_evaluation.repository.evaluation_criteria_repository import EvaluationCriteriaRepository


class EvaluationCriteriaService:
    """
    评价标准 service
    """

    def __init__(
        self,
        evaluation_criteria_repository: EvaluationCriteriaRepository,
        evaluation_criteria_plan_repository: EvaluationCriteriaPlanRepository,
    ):
        self.__evaluation_criteria_repository = evaluation_criteria_repository
        self.__evaluation_criteria_plan_repository = evaluation_criteria_plan_repository

    def save_evaluation_criteria(
        self,
        evaluation_criteria: SaveEvaluationCriteriaModel,
        transaction: Transaction,
    ):
        # 保存评价标准
        exist_evaluation_criteria_info = (
            self.__evaluation_criteria_repository.get_evaluation_criteria_by_name(
                name=evaluation_criteria.name,
                evaluation_object_category=evaluation_criteria.evaluation_object_category,
                evaluation_criteria_id=evaluation_criteria.id,
            )
        )
        if exist_evaluation_criteria_info:
            raise BusinessError("此评价标准名称已被使用")
        if evaluation_criteria.id:
            self.__evaluation_criteria_repository.update_evaluation_criteria(
                evaluation_criteria=evaluation_criteria.to_evaluation_criteria_model(),
                transaction=transaction,
                limited_col_list=["name", "comments", "status"],
            )
        else:
            evaluation_criteria.id = (
                self.__evaluation_criteria_repository.insert_evaluation_criteria(
                    evaluation_criteria=evaluation_criteria.to_evaluation_criteria_model(),
                    transaction=transaction,
                )
            )

    def get_evaluation_criteria_page(self, params: EvaluationCriteriaPageQueryParams):
        """
        获取评价标准
        :param params:
        """
        evaluation_criteria_page = (
            self.__evaluation_criteria_repository.get_evaluation_criteria_page(params=params)
        )
        for evaluation_criteria in evaluation_criteria_page.data:
            evaluation_criteria.status_display = get_enum_value_by_name(
                enum_class=EnumEvaluationCriteriaStatus,
                enum_name=evaluation_criteria.status,
            )
            evaluation_criteria.evaluation_object_category_display = get_enum_value_by_name(
                enum_class=EnumEvaluationObjectCategory,
                enum_name=evaluation_criteria.evaluation_object_category,
            )
        return evaluation_criteria_page

    def get_evaluation_criteria_detail(
        self,
        evaluation_criteria_id: str,
    ):
        """
        获取评价标准详情
        :param evaluation_criteria_id:
        """

        evaluation_criteria_detail = (
            self.__evaluation_criteria_repository.get_evaluation_criteria_detail(
                evaluation_criteria_id=evaluation_criteria_id
            )
        )
        evaluation_criteria_detail.status_display = get_enum_value_by_name(
            enum_class=EnumEvaluationCriteriaStatus,
            enum_name=evaluation_criteria_detail.status,
        )
        evaluation_criteria_detail.evaluation_object_category_display = get_enum_value_by_name(
            enum_class=EnumEvaluationObjectCategory,
            enum_name=evaluation_criteria_detail.evaluation_object_category,
        )
        return evaluation_criteria_detail

    def update_evaluation_criteria_status(
        self,
        evaluation_criteria: EvaluationCriteriaModel,
        transaction: Transaction,
    ):
        """
        更新评价标准状态
        :param evaluation_criteria:
        :param transaction:
        :return:
        """
        if evaluation_criteria.status == EnumEvaluationCriteriaStatus.ABOLISHED.name:
            evaluation_criteria_plan_list = self.__evaluation_criteria_repository.get_evaluation_criteria_plan_by_evaluation_criteria_id(
                evaluation_criteria_id=evaluation_criteria.id
            )

            for evaluation_criteria_plan in evaluation_criteria_plan_list:
                evaluation_criteria_plan.status = EnumEvaluationCriteriaPlanStatus.ABOLISHED.name
                self.__evaluation_criteria_plan_repository.update_evaluation_criteria_plan(
                    evaluation_criteria_plan=evaluation_criteria_plan,
                    transaction=transaction,
                    limited_col_list=["status"],
                )

        self.__evaluation_criteria_repository.update_evaluation_criteria(
            evaluation_criteria=evaluation_criteria,
            transaction=transaction,
            limited_col_list=["status"],
        )

    def delete_evaluation_criteria(
        self,
        evaluation_criteria_id: str,
        transaction: Transaction,
    ):
        """
        删除评价标准
        :param evaluation_criteria_id:
        :param transaction:
        :return:
        """

        # 删除评价标准
        self.__evaluation_criteria_repository.delete_evaluation_criteria(
            evaluation_criteria_id=evaluation_criteria_id,
            transaction=transaction,
        )

    @staticmethod
    def get_enum_evaluation_object_category():
        """
        获取EnumEvaluationObjectCategory
        :return:
        """
        return enum_to_dict_list(
            enum_class=EnumEvaluationObjectCategory,
            name_col="value",
            value_col="text",
        )

    @staticmethod
    def get_enum_evaluation_criteria_status():
        """
        获取EnumEvaluationCriteriaStatus
        :return:
        """
        return enum_to_dict_list(
            enum_class=EnumEvaluationCriteriaStatus,
            name_col="value",
            value_col="text",
        )

    def get_evaluation_criteria_plan_by_evaluation_criteria_id(self, evaluation_criteria_id: str):
        """
        获取应用评价标准的评价标准计划
        :param evaluation_criteria_id:
        :return:
        """
        evaluation_criteria_plan_list = self.__evaluation_criteria_repository.get_evaluation_criteria_plan_by_evaluation_criteria_id(
            evaluation_criteria_id=evaluation_criteria_id
        )

        return evaluation_criteria_plan_list

    def get_evaluation_criteria_list(self, params: EvaluationCriteriaListQueryParams) -> List[EvaluationCriteriaModel]:
        """
        获取评价标准列表
        :param params:
        """
        evaluation_criteria_list = (
            self.__evaluation_criteria_repository.get_evaluation_criteria_list(params=params)
        )
        for evaluation_criteria in evaluation_criteria_list:
            evaluation_criteria.status_display = get_enum_value_by_name(
                enum_class=EnumEvaluationCriteriaStatus,
                enum_name=evaluation_criteria.status,
            )
            evaluation_criteria.evaluation_object_category_display = get_enum_value_by_name(
                enum_class=EnumEvaluationObjectCategory,
                enum_name=evaluation_criteria.evaluation_object_category,
            )
        return evaluation_criteria_list

    def judge_evaluation_criteria_can_update(
        self, evaluation_criteria_id: str
    ) -> bool:
        """
        判断评价标准内容是否可以修改，即状态是否为已作废
        :param evaluation_criteria_id:
        :return:
        """

        evaluation_criteria = self.__evaluation_criteria_repository.get_evaluation_criteria_detail(
            evaluation_criteria_id=evaluation_criteria_id
        )

        if evaluation_criteria.status == EnumEvaluationCriteriaStatus.ABOLISHED.name:
            raise BusinessError("评价标准已作废，无法修改")

        return True

