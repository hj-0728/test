from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.resource_interface import Resource
from infra_object_storage.model.file_info_model import FileExtInfoModel

from backend.model.view.file_vm import FileVm
from infra_backbone.model.view.file_vm import FileViewModel


class StorageRepository(BasicRepository):
    def get_resource_related_file_list(
        self, resource: Resource, relationship: Optional[str] = None
    ) -> List[FileViewModel]:
        sql = """
        select f.id, f.original_name as file_name from st_file_info f 
        inner join st_file_relationship fr 
        on f.id=fr.file_id and fr.resource_category=:resource_category 
        and fr.resource_id=:resource_id
        and relationship=:relationship
        """
        return self._fetch_all_to_model(
            model_cls=FileViewModel,
            sql=sql,
            params={
                "resource_id": resource.res_id,
                "resource_category": resource.res_category,
                "relationship": relationship,
            },
        )

    def get_file_info_by_id(
        self,
        file_id: str,
    ) -> Optional[FileVm]:
        sql = """
        SELECT sfi.id,sfi.original_name AS file_name,ssi.bucket_name,ssi.object_name
        FROM st_file_info sfi
        INNER JOIN st_object_storage_raw ssi ON ssi.id = sfi.storage_info_id
        WHERE sfi.id = :file_id
        """
        return self._fetch_first_to_model(
            model_cls=FileVm,
            sql=sql,
            params={
                "file_id": file_id,
            },
        )

    def get_file_list_by_ids(self, file_ids: List[str]) -> List[FileExtInfoModel]:
        """

        :param file_ids:
        :return:
        """

        sql = """
        select i.id,bucket_name,object_name,checksum,size,storage_info_id,original_name
        from st_file_info i 
        INNER JOIN st_object_storage_raw r on i.storage_info_id=r.id
        INNER JOIN st_object_storage_account a on a.id=r.object_storage_account_id
        where i.id=any(array[:file_ids])
        """

        return self._fetch_all_to_model(
            model_cls=FileExtInfoModel,
            sql=sql,
            params={
                "file_ids": file_ids,
            },
        )
