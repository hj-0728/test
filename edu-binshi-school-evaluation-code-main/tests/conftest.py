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

from backend.backend_containers import BackendContainer
from context_sync.context_sync_containers import ContextSyncContainer
from domain_evaluation.domain_evaluation_containers import DomainEvaluationContainer
from edu_binshi.edu_evaluation_containers import EduEvaluationContainer
from infra_backbone.backbone_container import BackboneContainer
from infra_backbone.object_storage_container import ObjectStorageContainer
from infra_backbone.service.robot_service import RobotService

import infra_backbone
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
def prepare_backbone_container(prepare_uow) -> BackboneContainer:
    container = BackboneContainer(uow=prepare_uow)
    container.init_resources()
    return container


@fixture()
def prepare_backend_container(prepare_uow) -> BackendContainer:
    container = BackendContainer(uow=prepare_uow)
    container.init_resources()
    return container


@fixture()
def prepare_storage_container(prepare_database, prepare_uow) -> ObjectStorageContainer:
    object_storage_container = ObjectStorageContainer(uow=prepare_uow)
    object_storage_container.init_resources()
    return object_storage_container


@fixture()
def prepare_domain_evaluation_container(prepare_uow) -> DomainEvaluationContainer:
    container = DomainEvaluationContainer(uow=prepare_uow)
    container.init_resources()
    return container


@fixture()
def prepare_edu_evaluation_container(prepare_uow) -> EduEvaluationContainer:
    container = EduEvaluationContainer(uow=prepare_uow)
    container.init_resources()
    return container


@fixture()
def prepare_handler() -> Resource:
    return BasicResource(category="test_handler", id=generate_random_string())


@fixture()
def prepare_dingtalk_container(prepare_uow) -> DingtalkContainer:
    container = DingtalkContainer(uow=prepare_uow)
    container.init_resources()
    return container


@fixture()
def prepare_context_sync_container(prepare_uow) -> ContextSyncContainer:
    container = ContextSyncContainer(uow=prepare_uow)
    container.init_resources()
    return container


@fixture()
def prepare_transaction(prepare_handler) -> Transaction:
    return Transaction(
        id=generate_uuid_id(),
        handler_category=prepare_handler.res_category,
        handler_id=prepare_handler.res_id,
        handled_at=local_now(),
        action="test_object_storage",
        is_succeed=True,
    )


@fixture()
def prepare_robot(prepare_backbone_container) -> BasicResource:
    uow = prepare_backbone_container.uow()
    with uow:
        robot_service: RobotService = prepare_backbone_container.robot_service()
        robot = robot_service.get_system_robot().to_basic_handler()
    return robot


def test_init_database_table(prepare_database):
    prepare_database.create_tables(scan_module=infra_backbone)

