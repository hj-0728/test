from typing import List, Optional

from infra_basic.basic_resource import BasicResource
from infra_basic.transaction import Transaction
from infra_object_storage.error import ObjectStorageError
from infra_object_storage.model.file_info_model import FileExtInfoModel
from infra_object_storage.service.object_storage_service import ObjectStorageService

from infra_backbone.model.file_public_link_model import FilePublicLinkModel
from infra_backbone.model.view.file_vm import FileViewModel
from infra_backbone.repository.file_public_link_repository import FilePublicLinkRepository


class StorageService:
    def __init__(
        self,
        object_storage_service: ObjectStorageService,
        file_public_link_repository: FilePublicLinkRepository,
    ):
        self.__object_storage_service = object_storage_service
        self.__file_public_link_repository = file_public_link_repository

    def upload_files(
        self, file_list: List, transaction: Transaction, bucket_name: Optional[str] = None
    ) -> List[FileViewModel]:
        """
        批量上传文件并返回文件信息列表
        :param file_list:
        :param transaction:
        :param bucket_name:
        :return: List of file info objects
        """
        file_info_list = []

        for file_data in file_list:
            file_name = file_data.filename
            file_blob = file_data.read()

            if not file_blob:
                raise ObjectStorageError(f"file {file_name} is empty")

            file_info = self.__object_storage_service.upload_file(
                file_name=file_name,
                file_blob=file_blob,
                transaction=transaction,
                bucket_name=bucket_name,
            )

            file_info_list.append(
                FileViewModel(
                    id=file_info.id,
                    file_name=file_info.original_name,
                    url=file_info.url,
                )
            )
        return file_info_list

    def upload_file_with_resource(
        self,
        file_name: str,
        file_blob: bytes,
        transaction: Transaction,
        relationship: Optional[str] = None,
        resource: Optional[BasicResource] = None,
        is_public: bool = False,
    ) -> FileExtInfoModel:
        """
        上传文件并返回文件信息
        """
        if not file_blob:
            raise ObjectStorageError(f"file {file_name} is empty")

        if resource:
            file_info = self.__object_storage_service.upload_file_with_resource(
                file_name=file_name,
                file_blob=file_blob,
                resource=resource,
                relationship=relationship,
                is_public=is_public,
                transaction=transaction,
            )
        else:
            file_info = self.__object_storage_service.upload_file(
                file_name=file_name,
                file_blob=file_blob,
                transaction=transaction,
                is_public=is_public,
            )
        if is_public:
            self.__file_public_link_repository.insert_public_link(
                data=FilePublicLinkModel(file_id=file_info.id, public_link=file_info.url),
                transaction=transaction,
            )
        return file_info

    def get_resource_file_url(self, resource: BasicResource, relationship: str) -> Optional[str]:
        """
        获取资源文件url
        """
        file_public_link = self.__file_public_link_repository.fetch_resource_public_link(
            res_id=resource.id, res_category=resource.category, relationship=relationship
        )
        # 如果有公开链接，就返回公开链接
        if file_public_link:
            return file_public_link.public_link
        file_list = self.__object_storage_service.get_resource_related_file_list(
            resource=resource, relationship=relationship
        )
        # 如果有文件，就返回第一个文件的url
        if file_list:
            return file_list[0].url
        # 否则返回None
        return None
