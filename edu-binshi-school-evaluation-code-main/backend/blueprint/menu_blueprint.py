"""
菜单
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
from backend.service.app_role_service import AppRoleService
from infra_backbone.model.menu_model import EnumMenuCategory, MenuModel
from infra_backbone.service.menu_service import MenuService

blueprint_menu = Blueprint(
    name="menu",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/menu"
DINGTALK_PREFIX = "/dingtalk/menu"


@blueprint_menu.route(f"{WEB_PREFIX}/get-db-tree", methods=["GET"])
@inject
def route_get_user_menu_tree(
    menu_service: MenuService = Provide[BackendContainer.backbone_container.menu_service],
    role_service: AppRoleService = Provide[BackendContainer.app_role_service],
) -> jsonify:
    """
    获取用户菜单
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = menu_service.get_current_role_menu_tree(
            role_id=role_service.get_current_role_id(),
            menu_category=EnumMenuCategory.WEB.name,
        )
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_menu.route(f"{WEB_PREFIX}/tree/<string:category>", methods=["GET"])
@inject
def route_get_menu_tree(
    category,
    menu_service: MenuService = Provide[BackendContainer.backbone_container.menu_service],
) -> jsonify:
    """
    获取菜单树
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = menu_service.build_full_menu_tree(menu_category=category)
        carrier.push_succeed_data(data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_menu.route(f"{WEB_PREFIX}/add", methods=["POST"])
@inject
def route_add_tree(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    menu_service: MenuService = Provide[BackendContainer.backbone_container.menu_service],
) -> jsonify:
    """
    创建菜单
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="save_menu",
            action_params=data,
        )
        with uow:
            data = menu_service.add_menu(menu=MenuModel(**data), transaction=transaction)
        carrier.push_succeed_data(data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_menu.route(f"{WEB_PREFIX}/edit", methods=["POST"])
@inject
def route_edit_menu(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    menu_service: MenuService = Provide[BackendContainer.backbone_container.menu_service],
) -> jsonify:
    """
    编辑菜单
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="edit_menu",
            action_params=data,
        )
        with uow:
            menu_service.edit_menu(menu=MenuModel(**data), transaction=transaction)
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_menu.route(f"{WEB_PREFIX}/delete/<menu_id>", methods=["POST"])
@inject
def route_delete_menu(
    menu_id,
    uow: UnitOfWork = Provide[BackendContainer.uow],
    menu_service: MenuService = Provide[BackendContainer.backbone_container.menu_service],
) -> jsonify:
    """
    删除菜单
    :return:
    """
    carrier = MessageCarrier()
    try:
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="delete_menu",
            action_params={"menu_id": menu_id},
        )
        with uow:
            menu_service.delete_menu(menu_id=menu_id, transaction=transaction)
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_menu.route(f"{WEB_PREFIX}/update-sort", methods=["POST"])
@inject
def route_update_menu_sort(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    menu_service: MenuService = Provide[BackendContainer.backbone_container.menu_service],
) -> jsonify:
    """
    更新菜单排序
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="update_menu_sort",
            action_params=data,
        )
        with uow:
            menu_service.update_menu_sort(
                menu_list=[MenuModel(**x) for x in data],
                transaction=transaction,
            )
        carrier.push_succeed_data()
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict())


@blueprint_menu.route(f"{DINGTALK_PREFIX}/list", methods=["GET"])
@inject
def route_get_mobile_menu_list(
    menu_service: MenuService = Provide[BackendContainer.backbone_container.menu_service],
    role_service: AppRoleService = Provide[BackendContainer.app_role_service],
) -> jsonify:
    """
    手机端 获取当前用户可以操作的菜单
    :return:
    """
    carrier = MessageCarrier()
    try:
        # data = menu_service.get_current_role_menu_list_for_mobile(
        #     role_id=role_service.get_current_role_id(),
        #     menu_category=EnumMenuCategory.MOBILE.name,
        # )
        carrier.push_succeed_data(data=[])
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
