from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.tag_info import TagInfoEntity
from infra_backbone.entity.tag_ownership import TagOwnershipEntity
from infra_backbone.entity.tag_ownership_relationship import TagOwnershipRelationshipEntity
from infra_backbone.model.tag_info_model import TagInfoModel
from infra_backbone.model.tag_ownership_model import TagOwnershipModel
from infra_backbone.model.tag_ownership_relationship_model import TagOwnershipRelationshipModel


class TagRepository(BasicRepository):
    def insert_tag_info(self, tag: TagInfoModel, transaction: Transaction) -> str:
        """
        添加标签信息
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=TagInfoEntity, entity_model=tag, transaction=transaction
        )

    def insert_tag_ownership(
        self, tag_ownership: TagOwnershipModel, transaction: Transaction
    ) -> str:
        """
        添加标签所属
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=TagOwnershipEntity, entity_model=tag_ownership, transaction=transaction
        )

    def get_tag_ownership_by_tag_id(self, tag_id: str) -> Optional[TagOwnershipModel]:
        """
        根据标签所属id获取标签所属信息
        """
        sql = """select * from st_tag_ownership where tag_id = :tag_id"""
        return self._fetch_first_to_model(
            sql=sql, model_cls=TagOwnershipModel, params={"tag_id": tag_id}
        )

    def insert_tag_ownership_relationship(
        self, tag_ownership_rel: TagOwnershipRelationshipModel, transaction: Transaction
    ) -> str:
        """
        添加标签所属资源的关系
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=TagOwnershipRelationshipEntity,
            entity_model=tag_ownership_rel,
            transaction=transaction,
        )

    def fetch_tag_info_by_name(self, name: str) -> Optional[TagInfoModel]:
        """
        根据标签名称获取标签信息
        """
        sql = """select * from st_tag_info where name = :name"""
        return self._fetch_first_to_model(sql=sql, model_cls=TagInfoModel, params={"name": name})

    def get_tag_list(self, resource_category: Optional[str]) -> List[TagInfoModel]:
        """
        获取所有tag
        """
        sql = """
         SELECT distinct ti.*,sto.id as tag_ownership_id
         FROM st_tag_info ti
         JOIN st_tag_ownership sto ON ti.id::text = sto.tag_id::text
         JOIN st_tag_ownership_relationship tor ON sto.id::text = tor.tag_ownership_id::text
                """
        if resource_category:
            sql += """
            where tor.resource_category = :resource_category
            """
        return self._fetch_all_to_model(
            sql=sql, model_cls=TagInfoModel, params={"resource_category": resource_category}
        )

    def get_tag_ownership_relationship_by_resource(
        self, resource_category: str, resource_id: str
    ) -> TagInfoModel:
        """
        获取相关tag
        """
        sql = """
         SELECT ti.id,ti.name,sto.id as tag_ownership_id,tor.id as tag_ownership_relationship_id
         FROM st_tag_info ti
         JOIN st_tag_ownership sto ON ti.id::text = sto.tag_id::text
         JOIN st_tag_ownership_relationship tor ON sto.id::text = tor.tag_ownership_id::text
         where resource_category=:resource_category and resource_id=:resource_id
                """
        return self._fetch_first_to_model(
            model_cls=TagInfoModel,
            sql=sql,
            params={
                "resource_category": resource_category,
                "resource_id": resource_id,
            },
        )

    def delete_tag_ownership_relationship_by_id(
        self,
        tag_ownership_relationship_id: str,
        transaction: Transaction,
    ):
        """
        删除tag_ownership_relationship
        """
        self._delete_versioned_entity_by_id(
            entity_cls=TagOwnershipRelationshipEntity,
            entity_id=tag_ownership_relationship_id,
            transaction=transaction,
        )
