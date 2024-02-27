"""
功能权限蓝图层
"""

import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler
from backend.data.constant import FlaskConfigConst
from infra_backbone.model.edit.ability_permission_em import AbilityPermissionEditModel
from infra_backbone.model.edit.granted_ability_permission_em import AbilityPermissionAssignEm
from infra_backbone.service.ability_permission_service import AbilityPermissionService

blueprint_ability_permission = Blueprint(
    name="ability_permission",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/ability-permission"


@blueprint_ability_permission.route(f"{WEB_PREFIX}/tree", methods=["GET"])
@inject
def route_get_ability_permission_tree(
    ability_permission_service: AbilityPermissionService = Provide[
        BackendContainer.backbone_container.ability_permission_service
    ],
) -> jsonify:
    """
    获取功能权限树
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = ability_permission_service.build_full_ability_permission_tree()
        carrier.push_succeed_data(data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict())


@blueprint_ability_permission.route(f"{WEB_PREFIX}/create", methods=["POST"])
@inject
def route_create_ability_permission(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    ability_permission_service: AbilityPermissionService = Provide[
        BackendContainer.backbone_container.ability_permission_service
    ],
) -> jsonify:
    """
    创建功能权限
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        ability_permission_em = AbilityPermissionEditModel(**data)
        trans = uow.log_transaction(
            handler=get_current_handler(),
            action="create_ability_permission",
            action_params=data,
        )
        with uow:
            ability_permission_service.create_ability_permission(
                ability_permission_em=ability_permission_em,
                transaction=trans,
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_ability_permission.route(f"{WEB_PREFIX}/edit", methods=["POST"])
@inject
def route_edit_ability_permission(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    ability_permission_service: AbilityPermissionService = Provide[
        BackendContainer.backbone_container.ability_permission_service
    ],
) -> jsonify:
    """
    编辑功能权限
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        ability_permission_em = AbilityPermissionEditModel(**data)
        trans = uow.log_transaction(
            handler=get_current_handler(),
            action="edit_ability_permission",
            action_params=data,
        )
        with uow:
            ability_permission_service.update_ability_permission(
                ability_permission_em=ability_permission_em,
                transaction=trans,
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict())


@blueprint_ability_permission.route(f"{WEB_PREFIX}/delete/<string:permission_id>", methods=["POST"])
@inject
def route_delete_ability_permission(
    permission_id: str,
    uow: UnitOfWork = Provide[BackendContainer.uow],
    ability_permission_service: AbilityPermissionService = Provide[
        BackendContainer.backbone_container.ability_permission_service
    ],
) -> jsonify:
    """
    编辑功能权限
    :return:
    """
    carrier = MessageCarrier()
    try:
        trans = uow.log_transaction(
            handler=get_current_handler(),
            action="delete_ability_permission",
            action_params={"permission_id": permission_id},
        )
        with uow:
            ability_permission_service.delete_ability_permission(
                permission_id=permission_id,
                transaction=trans,
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict())


@blueprint_ability_permission.route(f"{WEB_PREFIX}/assign", methods=["POST"])
@inject
def route_save_permission_assign(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    ability_permission_service: AbilityPermissionService = Provide[
        BackendContainer.backbone_container.ability_permission_service
    ],
) -> jsonify:
    """
    保存授权数据
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        ability_permission_assign_em = AbilityPermissionAssignEm(**data)
        trans = uow.log_transaction(
            handler=get_current_handler(),
            action="save_permission_assign",
            action_params=data,
        )
        with uow:
            ability_permission_service.save_ability_permission_assign(
                ability_permission_assign_em=ability_permission_assign_em,
                transaction=trans,
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict())


@blueprint_ability_permission.route(f"{WEB_PREFIX}/assign-tree", methods=["POST"])
@inject
def route_get_ability_permission_assign_tree(
    ability_permission_service: AbilityPermissionService = Provide[
        BackendContainer.backbone_container.ability_permission_service
    ],
) -> jsonify:
    """
    获取权限树的授权详情数据
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        ability_permission_assign_em = AbilityPermissionAssignEm(**data)
        result = ability_permission_service.get_ability_permission_assign_tree(
            ability_permission_assign_em=ability_permission_assign_em,
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
