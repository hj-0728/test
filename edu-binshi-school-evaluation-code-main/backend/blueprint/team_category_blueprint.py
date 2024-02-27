import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.query_params import PageFilterParams
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler
from backend.data.constant import FlaskConfigConst
from infra_backbone.model.team_category_model import TeamCategoryModel
from infra_backbone.service.team_category_service import TeamCategoryService
from infra_backbone.model.params.team_category_query_params import TeamCategoryQueryParams

blueprint_team_category = Blueprint(
    name="team-category",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/team-category"


@blueprint_team_category.route(f"{WEB_PREFIX}/list", methods=["POST"])
@inject
def route_get_team_category_list(
    team_category_service: TeamCategoryService = Provide[
        BackendContainer.backbone_container.team_category_service
    ],
):
    """
    获取小组类型列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = team_category_service.get_team_category_list_page(
            query_params=TeamCategoryQueryParams(**data),
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_team_category.route(
    f"{WEB_PREFIX}/get-team-category-detail/<string:team_category_id>", methods=["GET"]
)
@inject
def route_get_evaluation_criteria_detail(
    team_category_id: str,
    team_category_service: TeamCategoryService = Provide[
        BackendContainer.backbone_container.team_category_service
    ],
):
    """
    获取小组类型详情
    :param team_category_id:
    :param team_category_service:
    """
    carrier = MessageCarrier()
    try:
        result = team_category_service.get_team_category_detail(
            team_category_id=team_category_id,
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_team_category.route(f"{WEB_PREFIX}/save-team-category", methods=["POST"])
@inject
def route_save_team_category(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    team_category_service: TeamCategoryService = Provide[
        BackendContainer.backbone_container.team_category_service
    ],
):
    """
    保存小组类型
    :param uow:
    :param team_category_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="save_team_category",
                action_params=data,
            )
            result = team_category_service.save_team_category(
                team_category=TeamCategoryModel(**data), transaction=transaction
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_team_category.route(f"{WEB_PREFIX}/change-team-category-activated", methods=["POST"])
@inject
def route_change_team_category_activated(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    team_category_service: TeamCategoryService = Provide[
        BackendContainer.backbone_container.team_category_service
    ],
):
    """
    改变激活状态
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="change_team_category_activated",
                action_params=data,
            )
            result = team_category_service.change_team_category_activated(
                team_category=TeamCategoryModel(**data), transaction=transaction
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict())
