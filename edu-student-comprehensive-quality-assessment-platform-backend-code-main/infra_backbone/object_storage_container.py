"""
对象存储容器
"""
from dependency_injector import containers, providers
from infra_basic.sqlalchemy_uow import SqlAlchemyUnitOfWork
from infra_object_storage.helper.object_storage_client import ObjectStorageClient
from infra_object_storage.repository.object_storage_repository import ObjectStorageRepository
from infra_object_storage.service.object_storage_service import ObjectStorageService


class ObjectStorageContainer(containers.DeclarativeContainer):
    uow = providers.Dependency(instance_of=SqlAlchemyUnitOfWork)  # type: ignore

    # type: ignore
    object_storage_client = providers.ThreadLocalSingleton(ObjectStorageClient)  # type: ignore

    object_storage_repository = providers.ThreadLocalSingleton(  # type: ignore
        ObjectStorageRepository, db_session=uow.provided.db_session
    )

    object_storage_service = providers.ThreadLocalSingleton(  # type: ignore
        ObjectStorageService,
        object_storage_repository=object_storage_repository,
        object_storage_client=object_storage_client,
    )
