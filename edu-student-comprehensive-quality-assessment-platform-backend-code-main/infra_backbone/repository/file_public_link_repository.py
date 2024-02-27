from typing import Optional, List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.file_public_link import FilePublicLinkEntity
from infra_backbone.model.file_public_link_model import FilePublicLinkModel


class FilePublicLinkRepository(BasicRepository):
    """
    文件的公开连接
    """

    def insert_public_link(self, data: FilePublicLinkModel, transaction: Transaction):
        """
        插入文件的公开链接
        """
        self._insert_versioned_entity_by_model(
            entity_cls=FilePublicLinkEntity,
            entity_model=data,
            transaction=transaction,
        )

    def fetch_resource_public_link(
        self, res_id: str, res_category: str, relationship: str
    ) -> Optional[FilePublicLinkModel]:
        """
        获取资源的公开链接
        """
        sql = """select * from sv_file_relationship_public_link
        where res_id = :res_id and res_category = :res_category and relationship = :relationship"""
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=FilePublicLinkModel,
            params={
                "res_id": res_id,
                "res_category": res_category,
                "relationship": relationship,
            },
        )

    def fetch_file_public_link_by_file_ids(self, file_ids: List[str]) -> List[FilePublicLinkModel]:
        """
        获取文件的公开链接
        :param file_ids:
        :return:
        """

        sql = """
        select * from st_file_public_link where file_id=any(:file_ids)
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=FilePublicLinkModel,
            params={"file_ids": file_ids},
        )
