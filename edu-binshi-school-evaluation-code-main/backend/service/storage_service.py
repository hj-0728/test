from typing import List, Optional

from infra_basic.transaction import Transaction
from infra_object_storage.error import ObjectStorageError
from infra_object_storage.model.file_info_model import FileExtInfoModel
from infra_object_storage.service.object_storage_service import ObjectStorageService


class StorageService:
    def __init__(
        self,
        object_storage_service: ObjectStorageService,
    ):
        self.__object_storage_service = object_storage_service

    def upload_files(
        self, file_list: List, transaction: Transaction, bucket_name: Optional[str] = None
    ) -> List[FileExtInfoModel]:
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

            file_info_list.append(file_info)
        return file_info_list
