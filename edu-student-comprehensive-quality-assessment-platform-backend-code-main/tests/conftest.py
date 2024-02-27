

import pytest
from infra_basic.basic_resource import BasicResource
from infra_basic.database import Database
from infra_basic.resource_interface import Resource
from infra_basic.sqlalchemy_uow import SqlAlchemyUnitOfWork
from infra_basic.transaction import Transaction
from infra_utility.config_helper import load_to_env, unload_from_env
from infra_utility.datetime_helper import local_now
from infra_utility.log_helper import config_logger
from infra_utility.token_helper import generate_random_string, generate_uuid_id
from pytest import fixture

from backend.backend_container import BackendContainer
import backend
from biz_comprehensive.comprehensive_container import ComprehensiveContainer
from infra_backbone.backbone_container import BackboneContainer
from infra_backbone.service.robot_service import RobotService
from infra_dingtalk.dingtalk_container import DingtalkContainer


@fixture()
def env_setup():
    config_logger(level="INFO", show_file=True, show_thread=True)
    load_to_env(__file__, "../app.toml")
    yield
    unload_from_env(__file__, "../app.toml")
    # check_env()


@fixture()
def prepare_database(env_setup) -> Database:
    return Database()


@fixture()
def prepare_uow(prepare_database) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(engine=prepare_database.engine)


@fixture()
def prepare_app_container(prepare_uow) -> BackendContainer:
    container = BackendContainer(uow=prepare_uow)
    container.init_resources()
    return container


@fixture()
def prepare_handler() -> Resource:
    return BasicResource(category="test_handler", id=generate_random_string())


@fixture()
def prepare_transaction(prepare_handler) -> Transaction:
    return Transaction(
        id=generate_uuid_id(),
        handler_category=prepare_handler.res_category,
        handler_id=prepare_handler.res_id,
        handled_on=local_now(),
        action="test_object_storage",
        is_succeed=True,
    )


@pytest.fixture()
def prepare_backbone_container(prepare_uow) -> BackboneContainer:
    container = BackboneContainer(uow=prepare_uow)
    container.init_resources()
    return container


@fixture()
def prepare_dingtalk_container(prepare_uow) -> DingtalkContainer:
    container = DingtalkContainer(uow=prepare_uow)
    container.init_resources()
    return container


@fixture()
def prepare_biz_comprehensive(prepare_uow) -> ComprehensiveContainer:
    container = ComprehensiveContainer(uow=prepare_uow)
    container.init_resources()
    return container


@fixture()
def prepare_robot(prepare_backbone_container) -> BasicResource:
    uow = prepare_backbone_container.uow()
    with uow:
        robot_service: RobotService = prepare_backbone_container.robot_service()
        robot = robot_service.get_system_robot().to_basic_handler()
    return robot


def test_init_database_table(prepare_database):
    prepare_database.create_tables(scan_module=backend)

