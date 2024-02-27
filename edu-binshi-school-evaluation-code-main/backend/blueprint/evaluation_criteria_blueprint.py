import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler
from backend.data.constant import FlaskConfigConst
from domain_evaluation.data.query_params.evaluation_criteria_page_query_params import (
    EvaluationCriteriaPageQueryParams, EvaluationCriteriaListQueryParams,
)
from domain_evaluation.model.evaluation_criteria_model import (
    EvaluationCriteriaModel,
    SaveEvaluationCriteriaModel,
)
from domain_evaluation.service.evaluation_criteria_service import EvaluationCriteriaService

blueprint_evaluation_criteria = Blueprint(
    name="evaluation-criteria",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/evaluation-criteria"


@blueprint_evaluation_criteria.route(f"{WEB_PREFIX}/save", methods=["POST"])
@inject
def route_save_evaluation_criteria(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    evaluation_criteria_service: EvaluationCriteriaService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_service
    ],
):
    """
    保存评价标准
    :param uow:
    :param evaluation_criteria_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="save_evaluation_criteria",
                action_params={"data": data},
            )
            result = evaluation_criteria_service.save_evaluation_criteria(
                evaluation_criteria=SaveEvaluationCriteriaModel(**data),
                transaction=transaction,
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria.route(f"{WEB_PREFIX}/get-page", methods=["POST"])
@inject
def route_get_evaluation_criteria_page(
    evaluation_criteria_service: EvaluationCriteriaService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_service
    ],
):
    """
    获取评价标准
    :param evaluation_criteria_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)

        result = evaluation_criteria_service.get_evaluation_criteria_page(
            params=EvaluationCriteriaPageQueryParams(**data),
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria.route(
    f"{WEB_PREFIX}/detail/<string:evaluation_criteria_id>", methods=["GET"]
)
@inject
def route_get_evaluation_criteria_detail(
    evaluation_criteria_id: str,
    evaluation_criteria_service: EvaluationCriteriaService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_service
    ],
):
    """
    获取评价标准详情
    :param evaluation_criteria_id:
    :param evaluation_criteria_service:
    """
    carrier = MessageCarrier()
    try:
        result = evaluation_criteria_service.get_evaluation_criteria_detail(
            evaluation_criteria_id=evaluation_criteria_id,
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria.route(f"{WEB_PREFIX}/update-status", methods=["POST"])
@inject
def route_update_evaluation_criteria_status(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    evaluation_criteria_service: EvaluationCriteriaService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_service
    ],
):
    """
    更新评价标准状态
    :param uow:
    :param evaluation_criteria_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="update_evaluation_criteria_status",
                action_params={"data": data},
            )
            result = evaluation_criteria_service.update_evaluation_criteria_status(
                evaluation_criteria=EvaluationCriteriaModel(**data),
                transaction=transaction,
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria.route(f"{WEB_PREFIX}/delete", methods=["POST"])
@inject
def route_delete_evaluation_criteria(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    evaluation_criteria_service: EvaluationCriteriaService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_service
    ],
):
    """
    删除评价标准
    :param uow:
    :param evaluation_criteria_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="delete_evaluation_criteria",
                action_params={"data": data},
            )
            result = evaluation_criteria_service.delete_evaluation_criteria(
                evaluation_criteria_id=data.get("evaluationCriteriaId"),
                transaction=transaction,
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria.route(
    f"{WEB_PREFIX}/get-enum-evaluation-object-category", methods=["GET"]
)
@inject
def route_get_enum_evaluation_object_category(
    evaluation_criteria_service: EvaluationCriteriaService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_service
    ],
):
    """
    获取EnumEvaluationObjectCategory
    :param evaluation_criteria_service:
    """
    carrier = MessageCarrier()
    try:
        result = evaluation_criteria_service.get_enum_evaluation_object_category()
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria.route(
    f"{WEB_PREFIX}/get-enum-evaluation-criteria-status", methods=["GET"]
)
@inject
def route_get_enum_evaluation_criteria_status(
    evaluation_criteria_service: EvaluationCriteriaService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_service
    ],
):
    """
    获取EnumEvaluationCriteriaStatus
    :param evaluation_criteria_service:
    """
    carrier = MessageCarrier()
    try:
        result = evaluation_criteria_service.get_enum_evaluation_criteria_status()
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria.route(
    f"{WEB_PREFIX}/get-evaluation-criteria-plan-by-evaluation-criteria-id", methods=["GET"]
)
@inject
def route_get_evaluation_criteria_plan_by_evaluation_criteria_id(
    evaluation_criteria_service: EvaluationCriteriaService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_service
    ],
):
    """
    获取应用评价标准的评价标准计划
    :param evaluation_criteria_service:
    """
    carrier = MessageCarrier()
    try:
        evaluation_criteria_id = request.args.get("evaluation_criteria_id")
        result = evaluation_criteria_service.get_evaluation_criteria_plan_by_evaluation_criteria_id(
            evaluation_criteria_id=evaluation_criteria_id
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria.route(f"{WEB_PREFIX}/get-list", methods=["POST"])
@inject
def route_get_evaluation_criteria_list(
    evaluation_criteria_service: EvaluationCriteriaService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_service
    ],
):
    """
    获取评价标准列表
    :param evaluation_criteria_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)

        result = evaluation_criteria_service.get_evaluation_criteria_list(
            params=EvaluationCriteriaListQueryParams(**data),
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
