import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_period_id
from backend.data.constant import FlaskConfigConst
from backend.data.query_params.plan_progress_detail_query_params import \
    PlanProgressDetailQueryParams
from backend.data.query_params.plan_ranking_query_params import PlanRankingQueryParams
from backend.model.edit.plan_benchmark_statistics_em import PlanBenchmarkStatisticsEm
from backend.model.edit.plan_statistics_filter_dept_tree_em import \
    PlanStatisticsFilterDeptTreeEditModel
from backend.service.evaluation_criteria_plan_statistics_service import \
    EvaluationCriteriaPlanStatisticsService

blueprint_evaluation_criteria_plan_statistics = Blueprint(
    name="evaluation-criteria-plan-statistics",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/evaluation-criteria-plan-statistics"


@blueprint_evaluation_criteria_plan_statistics.route(
    f"{WEB_PREFIX}/indicator-tree/<string:plan_id>", methods=["GET"]
)
@inject
def route_get_evaluation_criteria_plan_indicator_tree(
    plan_id: str,
    plan_statistics_service: EvaluationCriteriaPlanStatisticsService = Provide[
        BackendContainer.evaluation_criteria_plan_statistics_service
    ],
):
    """
    获取评价计划指标树
    :param plan_id:
    :param plan_statistics_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        result = plan_statistics_service.get_evaluation_criteria_plan_indicator_tree(
            evaluation_criteria_plan_id=plan_id,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan_statistics.route(
    f"{WEB_PREFIX}/get-plan-indicator-benchmark/<string:plan_id>/<string:indicator_id>",
    methods=["GET"]
)
@inject
def route_get_plan_indicator_benchmark(
    plan_id: str,
    indicator_id: str,
    plan_statistics_service: EvaluationCriteriaPlanStatisticsService = Provide[
        BackendContainer.evaluation_criteria_plan_statistics_service
    ],
):
    """
    获取评价计划指标 基准值
    :param plan_id:
    :param indicator_id:
    :param plan_statistics_service:
    :return:
    """

    carrier = MessageCarrier()
    try:
        result = plan_statistics_service.get_evaluation_criteria_plan_indicator_benchmark(
            evaluation_criteria_plan_id=plan_id,
            indicator_id=indicator_id,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan_statistics.route(
    f"{WEB_PREFIX}/get-plan-dept-grade-scope/<string:plan_id>",
    methods=["GET"]
)
@inject
def route_get_plan_dept_grade_scope(
    plan_id: str,
    plan_statistics_service: EvaluationCriteriaPlanStatisticsService = Provide[
        BackendContainer.evaluation_criteria_plan_statistics_service
    ],
):
    """
    获取评价计划部门年级范围
    :param plan_id:
    :param plan_statistics_service:
    :return:
    """

    carrier = MessageCarrier()
    try:
        result = plan_statistics_service.get_evaluation_criteria_plan_dept_grade_scope(
            evaluation_criteria_plan_id=plan_id,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan_statistics.route(
    f"{WEB_PREFIX}/get-plan-grade-class-scope/<string:plan_id>/<string:grade_id>",
    methods=["GET"]
)
@inject
def route_get_plan_grade_class_scope(
    plan_id: str,
    grade_id: str,
    plan_statistics_service: EvaluationCriteriaPlanStatisticsService = Provide[
        BackendContainer.evaluation_criteria_plan_statistics_service
    ],
):
    """
    获取评价计划部门年级下的班级范围
    :param plan_id:
    :param plan_statistics_service:
    :param grade_id:
    :return:
    """

    carrier = MessageCarrier()
    try:
        result = plan_statistics_service.get_evaluation_criteria_plan_grade_class_scope(
            evaluation_criteria_plan_id=plan_id,
            grade_dept_id=grade_id,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan_statistics.route(
    f"{WEB_PREFIX}/get-plan-class-student-scope/<string:plan_id>/<string:class_id>",
    methods=["GET"]
)
@inject
def route_get_plan_class_student_scope(
    plan_id: str,
    class_id: str,
    plan_statistics_service: EvaluationCriteriaPlanStatisticsService = Provide[
        BackendContainer.evaluation_criteria_plan_statistics_service
    ],
):
    """
    获取评价计划班级下的学生范围
    :param plan_id:
    :param plan_statistics_service:
    :param class_id:
    :return:
    """

    carrier = MessageCarrier()
    try:
        result = plan_statistics_service.get_evaluation_criteria_plan_class_student_scope(
            evaluation_criteria_plan_id=plan_id,
            class_dept_id=class_id,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan_statistics.route(
    f"{WEB_PREFIX}/get-plan-benchmark-statistics",
    methods=["POST"]
)
@inject
def route_get_plan_benchmark_statistics(
    plan_statistics_service: EvaluationCriteriaPlanStatisticsService = Provide[
        BackendContainer.evaluation_criteria_plan_statistics_service
    ],
):
    """
    获取评价计划benchmark统计数据
    :param plan_statistics_service:
    :return:
    """

    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = plan_statistics_service.get_plan_benchmark_statistics(
            params=PlanBenchmarkStatisticsEm(**data),
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan_statistics.route(
    f"{WEB_PREFIX}/get-plan-benchmark-ranking",
    methods=["POST"]
)
@inject
def route_get_plan_benchmark_ranking(
    plan_statistics_service: EvaluationCriteriaPlanStatisticsService = Provide[
        BackendContainer.evaluation_criteria_plan_statistics_service
    ],
):
    """
    获取评价计划benchmark排行数据
    :param plan_statistics_service:
    :return:
    """

    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = plan_statistics_service.get_plan_benchmark_ranking(
            params=PlanRankingQueryParams(**data),
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan_statistics.route(
    f"{WEB_PREFIX}/progress-detail",
    methods=["POST"]
)
@inject
def route_get_evaluation_criteria_plan_progress_detail(
    plan_statistics_service: EvaluationCriteriaPlanStatisticsService = Provide[
        BackendContainer.evaluation_criteria_plan_statistics_service
    ],
):
    """
    获取评价计划进展详情
    :param plan_statistics_service:
    :return:
    """

    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        params = PlanProgressDetailQueryParams(**data)
        params.period_id = get_current_period_id()
        result = plan_statistics_service.get_plan_progress_detail(
            params=params,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan_statistics.route(
    f"{WEB_PREFIX}/status-count", methods=["GET"]
)
@inject
def route_get_evaluation_criteria_plan_status_count(
    plan_statistics_service: EvaluationCriteriaPlanStatisticsService = Provide[
        BackendContainer.evaluation_criteria_plan_statistics_service
    ],
):
    """
    获取评价计划状态个数 已发布、已归档
    :param plan_statistics_service:
    :return:
    """

    carrier = MessageCarrier()
    try:
        period_id = get_current_period_id()
        result = plan_statistics_service.get_plan_status_count(
            period_id=period_id,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan_statistics.route(
    f"{WEB_PREFIX}/filter-dept-tree", methods=["POST"]
)
@inject
def route_get_plan_ranking_filter_dept_tree(
    plan_statistics_service: EvaluationCriteriaPlanStatisticsService = Provide[
        BackendContainer.evaluation_criteria_plan_statistics_service
    ],
):
    """
    获取计划排行部门筛选
    :param plan_statistics_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        params = PlanStatisticsFilterDeptTreeEditModel(**data)
        result = plan_statistics_service.get_plan_ranking_filter_dept_tree(
            params=params
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


