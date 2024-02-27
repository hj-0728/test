from dependency_injector.wiring import inject, Provide
from flask import current_app
from infra_basic.basic_resource import BasicResource
from infra_basic.uow_interface import UnitOfWork

from backend.backend_container import BackendContainer
from backend.service.auth_service import AuthService
from backend.service.redis_service import RedisService
from biz_comprehensive.model.period_model import PeriodModel
from infra_backbone.service.robot_service import RobotService


@inject
def get_current_user_id(
    redis_service: RedisService = Provide[BackendContainer.redis_service],
) -> str:
    """
    获取当前用户id
    :param redis_service:
    :return:
    """
    user_profile = redis_service.get_redis_user_profile()
    return user_profile.user_id


@inject
def get_current_handler(
    redis_service: RedisService = Provide[BackendContainer.redis_service],
) -> BasicResource:
    """
    获取当前handler
    :return:
    """
    user_profile = redis_service.get_redis_user_profile()
    return BasicResource(
        category=user_profile.user_category,
        id=user_profile.user_id,
    )


def get_current_role_code() -> str:
    """
    获取当前用户角色
    :return:
    """
    return "SYSTEM_ADMIN"


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
def get_current_people_id(
    auth_service: AuthService = Provide[BackendContainer.auth_service],
) -> str:
    """
    获取当前用户id
    :return:
    """
    return auth_service.get_current_people_id()


@inject
def get_current_semester_period(
    redis_service: RedisService = Provide[BackendContainer.redis_service],
) -> PeriodModel:
    """
    获取当前学期
    :param redis_service:
    :return:
    """
    return redis_service.get_current_semester_period()


@inject
def get_current_semester_period_id(
    redis_service: RedisService = Provide[BackendContainer.redis_service],
) -> str:
    """
    获取当前学期id
    :param redis_service:
    :return:
    """
    return redis_service.get_current_semester_period().id
