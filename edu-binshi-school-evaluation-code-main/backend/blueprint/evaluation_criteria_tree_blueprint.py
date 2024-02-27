import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler
from backend.data.constant import FlaskConfigConst
from domain_evaluation.data.query_params.evaluation_criteria_tree_item_query_params import (
    EvaluationCriteriaBoundTagItemQueryParams,
    EvaluationCriteriaNotBoundTagItemQueryParams,
)
from domain_evaluation.model.edit.evaluation_criteria_tree_bind_tag_em import (
    EvaluationCriteriaTreeBindTagEditModel,
)
from domain_evaluation.model.evaluation_criteria_tree_model import SaveEvaluationCriteriaTreeModel
from domain_evaluation.service.evaluation_criteria_tree_service import EvaluationCriteriaTreeService

blueprint_evaluation_criteria_tree = Blueprint(
    name="evaluation-criteria-tree",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/evaluation-criteria-tree"


@blueprint_evaluation_criteria_tree.route(f"{WEB_PREFIX}/save", methods=["POST"])
@inject
def route_save_evaluation_criteria_tree(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    evaluation_criteria_tree_service: EvaluationCriteriaTreeService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_tree_service
    ],
):
    """
    保存评价标准的树
    :param uow:
    :param evaluation_criteria_tree_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="save_evaluation_criteria_tree",
                action_params={"data": data},
            )
            result = evaluation_criteria_tree_service.save_evaluation_criteria_tree(
                evaluation_criteria_tree=SaveEvaluationCriteriaTreeModel(**data),
                transaction=transaction,
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_tree.route(f"{WEB_PREFIX}/delete", methods=["POST"])
@inject
def route_delete_evaluation_criteria_service_tree(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    evaluation_criteria_tree_service: EvaluationCriteriaTreeService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_tree_service
    ],
):
    """
    删除评价标准的树
    :param uow:
    :param evaluation_criteria_tree_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="delete_evaluation_criteria_tree",
                action_params={"data": data},
            )
            delete_list = data.get("deleteList")
            if not delete_list:
                raise BusinessError("未获取到参数")
            evaluation_criteria_tree_service.delete_evaluation_criteria_tree(
                evaluation_criteria_tree_list=[
                    SaveEvaluationCriteriaTreeModel(**x) for x in delete_list
                ],
                indicator_id=data.get("indicatorId"),
                transaction=transaction,
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_tree.route(f"{WEB_PREFIX}/update-seq", methods=["POST"])
@inject
def route_update_evaluation_criteria_service_tree_seq(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    evaluation_criteria_tree_service: EvaluationCriteriaTreeService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_tree_service
    ],
):
    """
    删除评价标准的树
    :param uow:
    :param evaluation_criteria_tree_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="delete_evaluation_criteria_tree",
                action_params={"data": data},
            )
            update_seq_list = data.get("updateSeqList")
            if not update_seq_list:
                raise BusinessError("未获取到参数")
            result = evaluation_criteria_tree_service.update_evaluation_criteria_tree_seq(
                evaluation_criteria_tree_list=[
                    SaveEvaluationCriteriaTreeModel(**x) for x in update_seq_list
                ],
                transaction=transaction,
                parent_indicator_id=data.get("parentIndicatorId"),
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_tree.route(
    f"{WEB_PREFIX}/get-tree/<string:evaluation_criteria_id>", methods=["GET"]
)
@inject
def route_get_evaluation_criteria_tree(
    evaluation_criteria_id: str,
    evaluation_criteria_tree_service: EvaluationCriteriaTreeService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_tree_service
    ],
):
    """
    获取评价标准的树
    :param evaluation_criteria_id:
    :param evaluation_criteria_tree_service:
    """
    carrier = MessageCarrier()
    try:
        result = evaluation_criteria_tree_service.get_evaluation_criteria_tree(
            evaluation_criteria_id=evaluation_criteria_id,
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_tree.route(
    f"{WEB_PREFIX}/detail/<string:evaluation_criteria_tree_id>", methods=["GET"]
)
@inject
def route_get_evaluation_criteria_tree_detail(
    evaluation_criteria_tree_id: str,
    evaluation_criteria_tree_service: EvaluationCriteriaTreeService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_tree_service
    ],
):
    """
    获取评价标准树详情
    :param evaluation_criteria_tree_id:
    :param evaluation_criteria_tree_service:
    """
    carrier = MessageCarrier()
    try:
        result = evaluation_criteria_tree_service.get_evaluation_criteria_tree_detail(
            evaluation_criteria_tree_id=evaluation_criteria_tree_id,
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_tree.route(f"{WEB_PREFIX}/bind-tag", methods=["POST"])
@inject
def route_bind_evaluation_criteria_tree_tag(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    evaluation_criteria_tree_service: EvaluationCriteriaTreeService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_tree_service
    ],
):
    """
    绑定评价标准树的tag
    """
    carrier = MessageCarrier()
    try:
        with uow:
            data = request.get_json(silent=True)
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="evaluation_criteria_tree_bind_tag",
                action_params=data,
            )
            evaluation_criteria_tree_service.evaluation_criteria_tree_bind_tag(
                evaluation_criteria_tree_bind_tag_em=EvaluationCriteriaTreeBindTagEditModel(**data),
                transaction=transaction,
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_tree.route(f"{WEB_PREFIX}/bound-tag-item-list", methods=["POST"])
@inject
def route_get_evaluation_criteria_tree_bound_tag_item_list(
    evaluation_criteria_tree_service: EvaluationCriteriaTreeService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_tree_service
    ],
):
    """
    获取评价标准树绑定tag的item列表
    :param evaluation_criteria_tree_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = evaluation_criteria_tree_service.get_evaluation_criteria_tree_bound_tag_item_list(
            query_params=EvaluationCriteriaBoundTagItemQueryParams(**data),
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_tree.route(
    f"{WEB_PREFIX}/bound-tag-detail/<string:evaluation_criteria_id>", methods=["GET"]
)
@inject
def route_get_evaluation_criteria_tree_bound_tag_detail(
    evaluation_criteria_id: str,
    evaluation_criteria_tree_service: EvaluationCriteriaTreeService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_tree_service
    ],
):
    """
    获取评价标准树标签绑定详情
    :param evaluation_criteria_id:
    :param evaluation_criteria_tree_service:
    """
    carrier = MessageCarrier()
    try:
        result = evaluation_criteria_tree_service.get_evaluation_criteria_tree_bound_tag_detail(
            evaluation_criteria_id=evaluation_criteria_id,
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_tree.route(f"{WEB_PREFIX}/not-bound-tag-item-list", methods=["POST"])
@inject
def route_get_evaluation_criteria_tree_not_bound_tag_item_list(
    evaluation_criteria_tree_service: EvaluationCriteriaTreeService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_tree_service
    ],
):
    """
    获取评价标准树未绑定tag的item列表
    :param evaluation_criteria_tree_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = (
            evaluation_criteria_tree_service.get_evaluation_criteria_tree_not_bound_tag_item_list(
                query_params=EvaluationCriteriaNotBoundTagItemQueryParams(**data),
            )
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_evaluation_criteria_tree.route(
    f"{WEB_PREFIX}/unbound-tag", methods=["POST"]
)
@inject
def route_delete_tag_ownership_relationship(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    evaluation_criteria_tree_service: EvaluationCriteriaTreeService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_criteria_tree_service
    ],
) -> jsonify:
    """
    删除绑定标签
    :return:
    """
    carrier = MessageCarrier()
    try:
        with uow:
            data = request.get_json(silent=True)
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="evaluation_criteria_tree_unbound_tag",
                action_params=data,
            )
            evaluation_criteria_tree_service.evaluation_criteria_tree_unbound_tag(
                evaluation_criteria_tree_bind_tag_em=EvaluationCriteriaTreeBindTagEditModel(**data),
                transaction=transaction,
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
