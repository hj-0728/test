import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork
from infra_pub_sub_manager.sync_pub_client import SyncPubClient
from infra_utility.serialize_helper import ORJSONPickle

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler, get_current_user_id
from backend.data.constant import FlaskConfigConst
from backend.model.edit.command_em import CommandEm
from backend.model.edit.command_generate_input_score_log_em import (
    CommandGenerateInputScoreLogEditModel,
    EnumTriggerCategory,
)
from backend.service.app_team_service import AppTeamService
from infra_backbone.model.edit.team_em import TeamEditModal
from infra_backbone.model.params.team_query_params import TeamQueryParams
from infra_backbone.service.team_service import TeamService

blueprint_team = Blueprint(
    name="team",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/team"


@blueprint_team.route(f"{WEB_PREFIX}/list", methods=["POST"])
@inject
def route_get_team_list(
    team_service: TeamService = Provide[BackendContainer.backbone_container.team_service],
):
    """
    获取小组列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = team_service.get_team_list_page(
            current_user_id=get_current_user_id(),
            query_params=TeamQueryParams(**data),
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_team.route(f"{WEB_PREFIX}/save", methods=["POST"])
@inject
def route_save_team(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    team_service: TeamService = Provide[BackendContainer.backbone_container.team_service],
    pub_client: SyncPubClient = Provide[BackendContainer.pub_client],
):
    """
    保存小组数据
    :param uow:
    :param team_service:
    :param pub_client:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            team_em = TeamEditModal(**data)
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="save_team",
                action_params=data,
            )
            result = team_service.save_team(
                team_em=team_em,
                transaction=transaction,
            )
        command_args = CommandGenerateInputScoreLogEditModel(
            trigger_category=EnumTriggerCategory.TEAM_CATEGORY.value,
            trigger_ids=[team_em.team_category_id],
        )
        command = CommandEm(category="task_handle_generate_input_score_log", args=command_args)
        pub_client.send_message(message=ORJSONPickle.encode_model(command))
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_team.route(f"{WEB_PREFIX}/delete/<string:team_id>", methods=["POST"])
@inject
def route_delete_team(
    team_id: str,
    uow: UnitOfWork = Provide[BackendContainer.uow],
    app_team_service: AppTeamService = Provide[BackendContainer.app_team_service],
):
    """
    删除小组
    :param uow:
    :param team_id:
    :param app_team_service:
    """
    carrier = MessageCarrier()
    try:
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="delete_team",
                action_params={"team_id": team_id},
            )
            result = app_team_service.delete_team(
                team_id=team_id,
                transaction=transaction,
            )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_team.route(f"{WEB_PREFIX}/detail/<string:team_id>", methods=["GET"])
@inject
def route_get_team_detail(
    team_id: str,
    team_service: TeamService = Provide[BackendContainer.backbone_container.team_service],
):
    """
    获取小组详情信息
    :param team_id:
    :param team_service:
    """
    carrier = MessageCarrier()
    try:
        result = team_service.get_team_detail(
            team_id=team_id,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
