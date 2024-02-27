import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler
from backend.data.constant import FlaskConfigConst
from backend.model.edit.save_evaluation_criteria_plan_scope_em import (
    SaveEvaluationCriteriaPlanScopeEm,
)
from backend.service.app_evaluation_criteria_plan_scope_service import (
    AppEvaluationCriteriaPlanScopeService,
)
from domain_evaluation.service.evaluation_criteria_plan_scope_service import (
    EvaluationCriteriaPlanScopeService,
)

blueprint_evaluation_criteria_plan_scope = Blueprint(
    name="evaluation-criteria-plan-scope",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/evaluation-criteria-plan-scope"


@blueprint_evaluation_criteria_plan_scope.route(f"{WEB_PREFIX}/save", methods=["POST"])
@inject
def route_save_evaluation_criteria_plan_scope(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    app_evaluation_criteria_plan_scope_service: AppEvaluationCriteriaPlanScopeService = Provide[
        BackendContainer.app_evaluation_criteria_plan_scope_service
    ],
):
    """
    保存评价标准计划适用的集合
    :param uow:
    :param app_evaluation_criteria_plan_scope_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="save_evaluation_criteria_plan_scope",
                action_params={"data": data},
            )
            result = app_evaluation_criteria_plan_scope_service.save_evaluation_criteria_plan_scope(
                data=SaveEvaluationCriteriaPlanScopeEm(**data),
                transaction=transaction,
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_plan_scope.route(
    f"{WEB_PREFIX}/get-plan-scope-by-plan-id/<string:plan_id>", methods=["GET"]
)
@inject
def route_get_plan_scope_by_plan_id(
    plan_id: str,
    evaluation_criteria_plan_scope_service: EvaluationCriteriaPlanScopeService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_plan_scope_service
    ],
):
    """
    根据plan_id获取评价标准计划适用的集合
    :param plan_id:
    :param evaluation_criteria_plan_scope_service:
    """
    carrier = MessageCarrier()
    try:
        result = evaluation_criteria_plan_scope_service.get_plan_scope_by_plan_id(plan_id=plan_id)
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
