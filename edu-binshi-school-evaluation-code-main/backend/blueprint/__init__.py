"""
蓝图初始化
"""
from dependency_injector.wiring import inject, Provide
from flask import current_app, request
from flask_jwt_extended import get_jwt_identity
from infra_basic.basic_resource import BasicResource
from infra_basic.errors.input import DataNotFoundError
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.data.constant import RedisConst
from backend.model.view.period_vm import PeriodVm
from backend.service.app_dingtalk_user_service import AppDingtalkUserService
from backend.service.app_role_service import AppRoleService
from backend.service.app_user_service import AppUserService
from backend.service.period_service import PeriodService
from infra_backbone.data.constant import SymbolConst
from infra_backbone.model.user_role_model import UserRoleModel
from infra_backbone.service.people_service import PeopleService
from infra_backbone.service.robot_service import RobotService
from infra_backbone.service.user_role_service import UserRoleService


@inject
def get_current_user_id(
    app_user_service: AppUserService = Provide[BackendContainer.app_user_service],
):
    """
    获取当前用户id
    :return:
    """
    dev = current_app.config.get("DEV", None)
    if dev and dev.enabled:
        if not dev.user_id:
            raise DataNotFoundError("配置文件dev中的user_id")
        return dev.user_id
    category = get_current_user_category()
    return app_user_service.get_current_user_id(current_category=category)


def get_current_user_category() -> str:
    """
    获取当前用户类型，没有改的话这个就随缘哪个类型吧
    :return:
    """
    dev = current_app.config.get("DEV", None)
    if dev and dev.enabled:
        if dev.platform == "WEB":
            return RedisConst.USER
        return RedisConst.DD_USER
    user_category = get_jwt_identity().split(SymbolConst.COLON)[0]
    if not user_category:
        return "未获取用户类型"
    return user_category


def get_current_dd_remote_user_id() -> str:
    """
    获取当前钉钉用户remote_user_id
    :return:
    """
    dev = current_app.config.get("DEV", None)
    if dev and dev.enabled:
        return dev.remote_user_id
    return get_jwt_identity().split(SymbolConst.COLON)[1]


@inject
def get_current_handler(
    app_dingtalk_user_service: AppDingtalkUserService = Provide[
        BackendContainer.app_dingtalk_user_service
    ],
) -> BasicResource:
    """
    获取当前操作者
    """
    category = get_current_user_category()
    if category == RedisConst.DD_USER:
        return app_dingtalk_user_service.get_current_dingtalk_handler()
    return BasicResource(category=category, id=get_current_user_id())


@inject
def load_system_robot(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    robot_service: RobotService = Provide[BackendContainer.backbone_container.robot_service],
) -> BasicResource:
    with uow:
        robot = robot_service.get_system_robot().to_basic_handler()
    return robot


def get_robot_handler() -> BasicResource:
    robot = current_app.config.get("ROBOT")
    if robot:
        return robot
    robot = load_system_robot()
    current_app.config["ROBOT"] = robot
    return robot


@inject
def get_current_role_code(
    app_role_service: AppRoleService = Provide[BackendContainer.app_role_service],
) -> str:
    """
    获取当前用户角色
    :return:
    """
    return app_role_service.get_current_role_code()


@inject
def get_current_role_id(
    app_role_service: AppRoleService = Provide[BackendContainer.app_role_service],
) -> str:
    """
    获取当前角色
    :return:
    """
    return app_role_service.get_current_role_id()


@inject
def get_current_user_role(
    user_role_service: UserRoleService = Provide[
        BackendContainer.backbone_container.user_role_service
    ],
) -> UserRoleModel:
    """
    获取当前用户角色
    """
    return user_role_service.get_user_role_model(
        user_id=get_current_user_id(), role_id=get_current_role_id()
    )


def get_current_user_role_handler():
    """
    获取当前用户角色操作
    """
    return BasicResource(category="USER_ROLE", id=get_current_user_role().id)


def get_dingtalk_corp_id() -> str:
    """
    优先从头里面读取钉钉corp id
    否则则从配置文件中读取开发的钉钉corp id
    都未获取到则抛出异常
    :return:
    """
    dev = current_app.config.get("DEV", None)
    if dev and dev.enabled and dev.dingtalk_corp_id:
        return dev.dingtalk_corp_id
    # return 'a878cd9e-bc3b-4acf-a953-c50074a75043'
    dingtalk_corp_id = request.headers.get("DINGTALK-CORP-ID", None)
    if dingtalk_corp_id:
        return dingtalk_corp_id
    raise DataNotFoundError("钉钉corp id")


@inject
def get_current_people_id(
    people_service: PeopleService = Provide[BackendContainer.backbone_container.people_service],
) -> str:
    """
    获取当前用户id
    :return:
    """
    dev = current_app.config.get("DEV", None)
    if dev and dev.enabled:
        if not dev.people_id:
            raise DataNotFoundError("配置文件dev中的people_id")
        return dev.people_id
    user_id = get_current_user_id()
    role_code = get_current_role_code()
    return people_service.get_people_by_user_id_and_role_code(
        user_id=user_id, role_code=role_code
    ).id


@inject
def get_current_period(
    period_service: PeriodService = Provide[BackendContainer.period_service],
) -> PeriodVm:
    """
    获取当前周期
    :return:
    """

    return period_service.get_current_period()


@inject
def get_current_period_id(
    period_service: PeriodService = Provide[BackendContainer.period_service],
) -> str:
    """
    获取当前周期id
    :return:
    """

    return period_service.get_current_period().id
