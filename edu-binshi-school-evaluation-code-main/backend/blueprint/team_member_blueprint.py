import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler
from backend.data.constant import FlaskConfigConst
from infra_backbone.model.edit.team_member_em import TeamMemberEm
from infra_backbone.model.params.team_can_select_people_query_params import (
    TeamCanSelectPeopleQueryParams,
)
from infra_backbone.model.params.team_member_query_params import TeamMemberQueryParams
from infra_backbone.service.team_member_service import TeamMemberService

blueprint_team_member = Blueprint(
    name="team_member",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/team-member"


@blueprint_team_member.route(f"{WEB_PREFIX}/list", methods=["POST"])
@inject
def route_get_team_member_list(
    team_member_service: TeamMemberService = Provide[
        BackendContainer.backbone_container.team_member_service
    ],
):
    """
    获取小组列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = team_member_service.get_team_member_list_page(
            query_params=TeamMemberQueryParams(**data),
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_team_member.route(f"{WEB_PREFIX}/can-select-people-list", methods=["POST"])
@inject
def route_get_can_select_people_list(
    team_member_service: TeamMemberService = Provide[
        BackendContainer.backbone_container.team_member_service
    ],
):
    """
    获取小组可选人员列表
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = team_member_service.get_can_select_people_list_page(
            query_params=TeamCanSelectPeopleQueryParams(**data),
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_team_member.route(f"{WEB_PREFIX}/save", methods=["POST"])
@inject
def route_save_team_member(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    team_member_service: TeamMemberService = Provide[
        BackendContainer.backbone_container.team_member_service
    ],
):
    """
    保存小组成员
    """
    carrier = MessageCarrier()
    try:
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="save_team_member",
            )
            data = request.get_json(silent=True)
            team_member_service.save_team_member(
                team_member_em=TeamMemberEm(**data),
                transaction=transaction,
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_team_member.route(f"{WEB_PREFIX}/delete/<string:team_member_id>", methods=["POST"])
@inject
def route_delete_team_member(
    team_member_id: str,
    team_member_service: TeamMemberService = Provide[
        BackendContainer.backbone_container.team_member_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    删除小组成员
    """
    carrier = MessageCarrier()
    try:
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="delete_team_member",
            )
            team_member_service.delete_team_member_by_team_member_id(
                team_member_id=team_member_id,
                transaction=transaction,
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
