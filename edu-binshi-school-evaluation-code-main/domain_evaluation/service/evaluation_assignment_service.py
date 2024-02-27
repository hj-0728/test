from infra_basic.transaction import Transaction
from infra_object_storage.service.object_storage_service import ObjectStorageService
from infra_utility.datetime_helper import local_now
from infra_utility.enum_helper import get_enum_value_by_name

from domain_evaluation.data.query_params.evaluation_assignment_query_params import (
    EvaluationAssignmentQueryParams,
)
from domain_evaluation.model.evaluation_assignment_model import (
    EnumEvaluationAssignmentEffectedCategory,
    EvaluationAssignmentModel,
)
from domain_evaluation.model.evaluation_criteria_model import EnumEvaluationObjectCategory
from domain_evaluation.model.evaluation_criteria_plan_model import EnumEvaluationCriteriaPlanStatus
from domain_evaluation.repository.evaluation_assignment_repository import (
    EvaluationAssignmentRepository,
)
from infra_backbone.model.role_model import EnumRoleCode


class EvaluationAssignmentService:
    """
    评价分配 service
    """

    def __init__(
        self,
        evaluation_assignment_repository: EvaluationAssignmentRepository,
        object_storage_service: ObjectStorageService,
    ):
        self.__evaluation_assignment_repository = evaluation_assignment_repository
        self.__object_storage_service = object_storage_service

    def save_evaluation_assignment(
        self,
        evaluation_criteria_plan_id: str,
        establishment_assignment_id: str,
        transaction: Transaction,
    ) -> EvaluationAssignmentModel:
        """
        保存评价分配--学生
        :param evaluation_criteria_plan_id:
        :param establishment_assignment_id:
        :param transaction:
        :return:
        """
        evaluation_assignment = EvaluationAssignmentModel(
            evaluation_criteria_plan_id=evaluation_criteria_plan_id,
            effected_category=EnumEvaluationAssignmentEffectedCategory.ESTABLISHMENT_ASSIGN.name,
            effected_id=establishment_assignment_id,
            start_at=local_now(),
        )
        evaluation_assignment.id = (
            self.__evaluation_assignment_repository.insert_evaluation_assignment(
                data=evaluation_assignment, transaction=transaction
            )
        )
        return evaluation_assignment

    def get_evaluation_assignment_todo_list(self, params: EvaluationAssignmentQueryParams):
        """
        获取评价分配需要做的列表
        :param params:
        :return:
        """
        result = self.__evaluation_assignment_repository.get_evaluation_assignment_todo_list(
            params=params
        )
        for data in result.data:
            if data.avatar_bucket_name and data.avatar_object_name:
                data.avatar_url = self.__object_storage_service.build_url(
                    bucket_name=data.avatar_bucket_name,
                    object_name=data.avatar_object_name
                )
        return result

    def get_evaluation_assignment_about_me_list(
        self,
        params: EvaluationAssignmentQueryParams,
        current_role_code: str,
    ):
        """
        获取自评的评价分配列表
        :param params:
        :param current_role_code:
        :return:
        """
        result = self.__evaluation_assignment_repository.get_evaluation_assignment_about_me_list(
            params=params
        )

        show_report_status = [
            EnumEvaluationCriteriaPlanStatus.IN_PROGRESS.name,
            EnumEvaluationCriteriaPlanStatus.ARCHIVED.name,
        ]

        for data in result.data:
            data.evaluation_object_category_name = get_enum_value_by_name(
                enum_class=EnumEvaluationObjectCategory,
                enum_name=data.evaluation_object_category,
                fallback="未知",
            )
            data.plan_status_name = get_enum_value_by_name(
                enum_class=EnumEvaluationCriteriaPlanStatus,
                enum_name=data.plan_status,
                fallback="未知",
            )
            if data.plan_status in show_report_status and current_role_code != EnumRoleCode.STUDENT.name:
                data.show_report = True
        return result
