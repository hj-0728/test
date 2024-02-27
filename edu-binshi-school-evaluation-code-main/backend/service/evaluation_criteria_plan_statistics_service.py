import json
from typing import List, Dict

from infra_basic.errors import BusinessError
from infra_basic.pagination_carrier import PaginationCarrier
from infra_object_storage.service.object_storage_service import ObjectStorageService
from infra_utility.algorithm.tree import list_to_tree
from infra_utility.enum_helper import get_enum_value_by_name

from backend.data.query_params.plan_progress_detail_query_params import \
    PlanProgressDetailQueryParams
from backend.data.query_params.plan_ranking_query_params import PlanRankingQueryParams
from backend.model.edit.plan_benchmark_statistics_em import PlanBenchmarkStatisticsEm, \
    EnumStatisticsObjectType
from backend.model.edit.plan_statistics_filter_dept_tree_em import \
    PlanStatisticsFilterDeptTreeEditModel
from backend.model.view.benchmark_vm import BenchmarkVm
from backend.model.view.dimension_dept_tree_info_vm import DimensionDeptTreeInfoVm
from backend.model.view.indicator_tree_vm import IndicatorTreeVm
from backend.model.view.plan_benchmark_statistics_vm import \
    PlanBenchmarkStatisticsVm, PlanRankingBenchmarkStatisticsVm, PlanProgressDetailVm
from backend.repository.evaluation_criteria_plan_statistics_repository import \
    EvaluationCriteriaPlanStatisticsRepository
from domain_evaluation.model.evaluation_criteria_plan_model import \
    EnumEvaluationCriteriaPlanStatus
from domain_evaluation.repository.benchmark_repository import BenchmarkRepository
from domain_evaluation.service.evaluation_criteria_plan_service import \
    EvaluationCriteriaPlanService
from edu_binshi.model.view.dept_tree_vm import DeptTreeViewModel
from infra_backbone.data.constant import DimensionCodeConst, OrganizationCodeConst
from infra_backbone.model.dimension_model import EnumDimensionCategory
from infra_backbone.model.people_model import PeopleModel
from infra_backbone.service.dimension_service import DimensionService
from infra_backbone.service.organization_service import OrganizationService


class EvaluationCriteriaPlanStatisticsService:
    """
    评价标准计划统计 service
    """

    def __init__(
        self,
        evaluation_criteria_plan_statistics_repository: EvaluationCriteriaPlanStatisticsRepository,
        dimension_service: DimensionService,
        benchmark_repository: BenchmarkRepository,
        object_storage_service: ObjectStorageService,
        evaluation_criteria_plan_service: EvaluationCriteriaPlanService,
        organization_service: OrganizationService,
    ):
        self.__plan_stats_repository = evaluation_criteria_plan_statistics_repository
        self.__dimension_service = dimension_service
        self.__benchmark_repository = benchmark_repository
        self.__object_storage_service = object_storage_service
        self.__plan_service = evaluation_criteria_plan_service
        self.__organization_service = organization_service

    def get_evaluation_criteria_plan_indicator_tree(
        self, evaluation_criteria_plan_id: str
    ) -> List[IndicatorTreeVm]:
        """
        获取评价标准计划指标树
        :param evaluation_criteria_plan_id:
        :return:
        """

        indicator_list = self.__plan_stats_repository.get_evaluation_criteria_plan_indicator_by_plan_id(
            evaluation_criteria_plan_id=evaluation_criteria_plan_id
        )

        # 2. 生成树
        indicator_tree = list_to_tree(
            original_list=indicator_list,
            tree_node_type=IndicatorTreeVm,
            parent_id_attr="parent_indicator_id",
        )

        return indicator_tree

    def get_evaluation_criteria_plan_indicator_benchmark(
        self, evaluation_criteria_plan_id: str, indicator_id: str
    ) -> List[BenchmarkVm]:
        """
        获取评价标准计划指标基准
        :param evaluation_criteria_plan_id:
        :param indicator_id:
        :return:
        """

        return self.__plan_stats_repository.get_evaluation_criteria_plan_indicator_benchmark(
            evaluation_criteria_plan_id=evaluation_criteria_plan_id,
            indicator_id=indicator_id,
        )

    def get_evaluation_criteria_plan_dept_grade_scope(
        self, evaluation_criteria_plan_id: str
    ) -> List[DimensionDeptTreeInfoVm]:
        """
        获取评价标准计划部门年级范围
        :param evaluation_criteria_plan_id:
        :return:
        """

        dimension = self.__dimension_service.get_dimension_by_organization_code_and_category_code(
            dimension_code=DimensionCodeConst.DINGTALK_EDU,
            dimension_category=EnumDimensionCategory.EDU.name,
            organization_code=OrganizationCodeConst.BJSYXX,
        )

        return self.__plan_stats_repository.get_evaluation_criteria_plan_dept_grade_scope(
            evaluation_criteria_plan_id=evaluation_criteria_plan_id,
            dimension_id=dimension.id,
        )

    def get_evaluation_criteria_plan_grade_class_scope(
        self, evaluation_criteria_plan_id: str, grade_dept_id: str
    ) -> List[DimensionDeptTreeInfoVm]:
        """
        获取评价计划部门年级下的班级范围
        :param evaluation_criteria_plan_id:
        :param grade_dept_id:
        :return:
        """

        dimension = self.__dimension_service.get_dimension_by_organization_code_and_category_code(
            dimension_code=DimensionCodeConst.DINGTALK_EDU,
            dimension_category=EnumDimensionCategory.EDU.name,
            organization_code=OrganizationCodeConst.BJSYXX,
        )

        return self.__plan_stats_repository.get_evaluation_criteria_plan_grade_class_scope(
            evaluation_criteria_plan_id=evaluation_criteria_plan_id,
            grade_dept_id=grade_dept_id,
            dimension_id=dimension.id,
        )

    def get_evaluation_criteria_plan_class_student_scope(
        self, evaluation_criteria_plan_id: str, class_dept_id: str
    ) -> List[PeopleModel]:
        """
        获取评价计划班级下的学生范围
        :param evaluation_criteria_plan_id:
        :param class_dept_id:
        :return:
        """

        return self.__plan_stats_repository.get_evaluation_criteria_plan_class_student_scope(
            evaluation_criteria_plan_id=evaluation_criteria_plan_id,
            class_dept_id=class_dept_id,
        )

    def get_plan_benchmark_statistics(
        self, params: PlanBenchmarkStatisticsEm
    ) -> PlanBenchmarkStatisticsVm:
        """
        获取评价计划基准统计
        :param params:
        :return:
        """

        score_symbol_info = self.__benchmark_repository.get_benchmark_score_symbol(
            benchmark_id=params.benchmark_id
        )

        if score_symbol_info.limited_string_options_str:
            score_symbol_info.limited_string_options = json.loads(score_symbol_info.limited_string_options_str)

        if params.statistics_object_type == EnumStatisticsObjectType.CLASS.name:

            dimension = self.__dimension_service.get_dimension_by_organization_code_and_category_code(
                dimension_code=DimensionCodeConst.DINGTALK_EDU,
                dimension_category=EnumDimensionCategory.EDU.name,
                organization_code=OrganizationCodeConst.BJSYXX,
            )
            statistics_info = self.__plan_stats_repository.get_plan_class_benchmark_statistics(
                evaluation_criteria_plan_id=params.evaluation_criteria_plan_id,
                dimension_dept_tree_id_list=params.dimension_dept_tree_id_list,
                benchmark_id=params.benchmark_id,
                dimension_id=dimension.id
            )

        elif params.statistics_object_type == EnumStatisticsObjectType.STUDENT.name:

            statistics_info = self.__plan_stats_repository.get_plan_student_benchmark_statistics(
                evaluation_criteria_plan_id=params.evaluation_criteria_plan_id,
                benchmark_id=params.benchmark_id,
            )

        else:
            raise BusinessError("参数错误")

        return PlanBenchmarkStatisticsVm(
            statistics_info=statistics_info,
            score_symbol_info=score_symbol_info
        )

    def get_plan_benchmark_ranking(
        self, params: PlanRankingQueryParams
    ) -> PaginationCarrier[PlanRankingBenchmarkStatisticsVm]:
        """
        计划基准排行
        :param params:
        :return:
        """

        score_symbol_info = self.__benchmark_repository.get_benchmark_score_symbol(
            benchmark_id=params.benchmark_id
        )

        if score_symbol_info.limited_string_options_str:
            score_symbol_info.limited_string_options = json.loads(score_symbol_info.limited_string_options_str)

        string_options = score_symbol_info.limited_string_options \
            if score_symbol_info.limited_string_options \
            else score_symbol_info.string_options

        ranking = self.__plan_stats_repository.get_plan_ranking_benchmark_statistics(
            params=params,
            string_options=string_options,
        )

        for ranking_data in ranking.data:
            ranking_data.file_url = self.__object_storage_service.get_file_url(
                file_id=ranking_data.file_id
            )

        return ranking

    def get_plan_progress_detail(
        self, params: PlanProgressDetailQueryParams
    ) -> PaginationCarrier[PlanProgressDetailVm]:
        """
        获取计划进展详情
        :param params:
        :return:
        """

        if params.is_in_progress:
            plan_progress = self.__plan_stats_repository.get_in_progress_plan_progress_detail(
                params=params
            )
        else:
            plan_progress = self.__plan_stats_repository.get_to_be_started_plan_progress_detail(
                params=params
            )

        for plan_progress_data in plan_progress.data:
            plan_progress_data.status_name = get_enum_value_by_name(
                enum_class=EnumEvaluationCriteriaPlanStatus,
                enum_name=plan_progress_data.status
            )

        return plan_progress

    def get_plan_status_count(self, period_id: str) -> Dict[str, int]:
        """
        获取周期计划状态个数
        :param period_id:
        :return: {status: count}
        """

        status_count_list = self.__plan_stats_repository.get_plan_status_count(
            period_id=period_id
        )
        status_count_dict = {}
        for status_count in status_count_list:
            status_count_dict[status_count.status] = status_count.count
        return status_count_dict

    def get_plan_ranking_filter_dept_tree(
        self, params: PlanStatisticsFilterDeptTreeEditModel
    ) -> List[DeptTreeViewModel]:
        """
        获取计划排序部门过滤
        :param params:
        :return:
        """
        plan = self.__plan_service.get_evaluation_criteria_plan(
            plan_id=params.evaluation_criteria_plan_id
        )
        params.compared_time = min(plan.executed_finish_at, plan.handled_at)
        tree = self.__plan_stats_repository.get_plan_ranking_filter_dept(params=params)

        if not tree:
            return []

        organization = self.__organization_service.get_organization_by_code(
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

