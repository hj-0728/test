from typing import List

from infra_basic.pagination_carrier import PaginationCarrier
from infra_utility.algorithm.tree import list_to_tree

from backend.data.query_params.evaluation_report_assignment_query_params import (
    EvaluationReportAssignmentQueryParams,
)
from backend.model.view.evaluation_report_assignment_vm import EvaluationReportAssignmentViewModel
from domain_evaluation.service.evaluation_criteria_plan_service import EvaluationCriteriaPlanService
from edu_binshi.model.edit.evaluation_report_dept_tree_em import EvaluationReportDeptTreeEditModel
from edu_binshi.model.view.dept_tree_vm import DeptTreeViewModel
from edu_binshi.repository.report_repository import ReportRepository
from infra_backbone.data.constant import OrganizationCodeConst
from infra_backbone.service.organization_service import OrganizationService


class EvaluationReportService:
    def __init__(
        self,
        evaluation_criteria_plan_service: EvaluationCriteriaPlanService,
        report_repository: ReportRepository,
        organization_service: OrganizationService,
    ):
        self._evaluation_criteria_plan_service = evaluation_criteria_plan_service
        self.__report_repository = report_repository
        self._organization_service = organization_service

    def get_evaluation_report_tree(
        self, params: EvaluationReportDeptTreeEditModel
    ) -> List[DeptTreeViewModel]:
        """
        获取评价报告查看页需要展示的部门
        """
        plan = self._evaluation_criteria_plan_service.get_evaluation_criteria_plan(
            plan_id=params.evaluation_criteria_plan_id
        )
        params.compared_time = min(plan.executed_finish_at, plan.handled_at)
        tree = self.__report_repository.get_evaluation_report_dept(params=params)
        if not tree:
            return []

        organization = self._organization_service.get_organization_by_code(
            code=OrganizationCodeConst.BJSYXX
        )
        tree_list = list_to_tree(
            original_list=tree,
            tree_node_type=DeptTreeViewModel,
            id_attr="dept_id",
            parent_id_attr="parent_dept_id",
        )
        full_tree = [
            DeptTreeViewModel(
                id=organization.id,
                name=organization.name,
                seq=1,
                dept_category_code="ORGANIZATION",
                children=tree_list,
            )
        ]
        return full_tree

    def get_evaluation_report_assignment(
        self, params: EvaluationReportAssignmentQueryParams
    ) -> PaginationCarrier[EvaluationReportAssignmentViewModel]:
        """
        获取评价报告页的分配列表
        """
        plan = self._evaluation_criteria_plan_service.get_evaluation_criteria_plan(
            plan_id=params.evaluation_criteria_plan_id
        )
        params.compared_time = min(plan.executed_finish_at, plan.handled_at)
        return self.__report_repository.fetch_evaluation_report_assignment(params=params)
