from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_handler
from backend.data.constant import FlaskConfigConst
from infra_backbone.model.menu_model import MenuModel
from infra_backbone.model.view.get_menu_tree_vm import GetMenuTreeViewModel
from infra_backbone.service.menu_service import MenuService

blueprint_menu = Blueprint(
    name="menu",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/menu"


@blueprint_menu.route(f"{WEB_PREFIX}/save", methods=["POST"])
@inject
def route_save_menu(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    menu_service: MenuService = Provide[BackendContainer.backbone_container.menu_service],
) -> jsonify:
    """
    save
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
            menu_service.save_menu(menu=MenuModel(**data), transaction=transaction)
    except BusinessError as err:
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_menu.route(f"{WEB_PREFIX}/get-info/<string:menu_id>", methods=["GET"])
@inject
def route_get_menu_info(
    menu_id: str,
    menu_service: MenuService = Provide[BackendContainer.backbone_container.menu_service],
) -> jsonify:
    """
    save
    """
    carrier = MessageCarrier()
    try:
        data = menu_service.get_menu_info(menu_id=menu_id)
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_menu.route(f"{WEB_PREFIX}/get-tree", methods=["POST"])
@inject
def route_get_menu_tree(
    menu_service: MenuService = Provide[BackendContainer.backbone_container.menu_service],
) -> jsonify:
    """
    获取菜单树
    """
    carrier = MessageCarrier()
    try:
        data = menu_service.build_full_menu_tree(
            params=GetMenuTreeViewModel(**request.get_json(silent=True))
        )
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_menu.route(f"{WEB_PREFIX}/delete/<string:menu_id>", methods=["POST"])
@inject
def route_delete_menu(
    menu_id: str,
    uow: UnitOfWork = Provide[BackendContainer.uow],
    menu_service: MenuService = Provide[BackendContainer.backbone_container.menu_service],
) -> jsonify:
    """
    删除菜单
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
    except BusinessError as err:
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
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="delete_menu",
            action_params=data,
        )
        with uow:
            menu_service.update_menu_sort(
                menu_list=[MenuModel(**x) for x in data], transaction=transaction
            )
    except BusinessError as err:
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
