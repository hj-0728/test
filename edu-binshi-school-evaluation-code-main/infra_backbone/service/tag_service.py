from typing import Optional

from infra_basic.transaction import Transaction

from infra_backbone.model.edit.save_tag_em import SaveTagEditModel
from infra_backbone.model.tag_info_model import TagInfoModel
from infra_backbone.model.tag_ownership_model import TagOwnershipModel
from infra_backbone.model.tag_ownership_relationship_model import TagOwnershipRelationshipModel
from infra_backbone.repository.tag_repository import TagRepository


class TagService:
    def __init__(self, tag_repository: TagRepository):
        self._tag_repository = tag_repository

    def save_tag_and_related_relationship(
        self, tag: SaveTagEditModel, transaction: Transaction
    ) -> str:
        """
        保存标签信息
        """
        tag.id = self.save_tag_info(tag_em=tag, transaction=transaction) if not tag.id else tag.id
        tag_ownership_id = self.save_tag_ownership(tag=tag, transaction=transaction)
        for tag_ownership_relationship in tag.tag_ownership_relationship_list:
            self._tag_repository.insert_tag_ownership_relationship(
                tag_ownership_rel=TagOwnershipRelationshipModel(
                    tag_ownership_id=tag_ownership_id,
                    resource_category=tag_ownership_relationship.resource_category,
                    resource_id=tag_ownership_relationship.resource_id,
                    relationship=tag_ownership_relationship.relationship,
                ),
                transaction=transaction,
            )
        return tag.id

    def save_tag_ownership(self, tag: SaveTagEditModel, transaction: Transaction) -> str:
        """
        保存标签所属信息
        """
        tag_ownership = self._tag_repository.get_tag_ownership_by_tag_id(tag_id=tag.id)
        if not tag_ownership:
            owner_category = (
                tag.owner_category if tag.owner_category else transaction.handler_category
            )
            owner_id = tag.owner_id if tag.owner_id else transaction.handler_id
            return self._tag_repository.insert_tag_ownership(
                tag_ownership=TagOwnershipModel(
                    tag_id=tag.id,
                    code=tag.code,
                    owner_category=owner_category,
                    owner_id=owner_id,
                    is_editable=tag.is_editable,
                    is_activated=tag.is_activated,
                ),
                transaction=transaction,
            )
        return tag_ownership.id

    def save_tag_info(self, tag_em: SaveTagEditModel, transaction: Transaction) -> str:
        """
        保存标签信息
        """
        tag = self._tag_repository.fetch_tag_info_by_name(name=tag_em.name)
        if not tag:
            return self._tag_repository.insert_tag_info(
                tag=TagInfoModel(name=tag_em.name), transaction=transaction
            )
        return tag.id

    def get_tag_list(self, resource_category: Optional[str]):
        return self._tag_repository.get_tag_list(resource_category=resource_category)

    def save_tag_and_update_related_relationship(
        self, tag: SaveTagEditModel, transaction: Transaction
    ) -> str:
        """
        保存标签信息并关联，确保只有一个关联，有原始的先删了
        """
        tag.id = self.save_tag_info(tag_em=tag, transaction=transaction) if not tag.id else tag.id
        tag_ownership_id = self.save_tag_ownership(tag=tag, transaction=transaction)
        for tag_ownership_relationship in tag.tag_ownership_relationship_list:
            self.update_related_relationship(
                tag_ownership_relationship=TagOwnershipRelationshipModel(
                    tag_ownership_id=tag_ownership_id,
                    resource_category=tag_ownership_relationship.resource_category,
                    resource_id=tag_ownership_relationship.resource_id,
                    relationship=tag_ownership_relationship.relationship,
                ),
                transaction=transaction
            )
        return tag.id

    def update_related_relationship(
            self,
            tag_ownership_relationship: TagOwnershipRelationshipModel,
            transaction: Transaction
    ):
        """
        更新关联关系
        """
        old_tag_ownership_info = self._tag_repository.get_tag_ownership_relationship_by_resource(
            resource_category=tag_ownership_relationship.resource_category,
            resource_id=tag_ownership_relationship.resource_id,
        )
        if old_tag_ownership_info:
            if old_tag_ownership_info.tag_ownership_id != tag_ownership_relationship.tag_ownership_id:
                self._tag_repository.delete_tag_ownership_relationship_by_id(
                    tag_ownership_relationship_id=old_tag_ownership_info.tag_ownership_relationship_id,
                    transaction=transaction,
                )
            else:
                return
        self._tag_repository.insert_tag_ownership_relationship(
            tag_ownership_rel=tag_ownership_relationship,
            transaction=transaction,
        )

    def delete_tag_ownership_relationship(self, tag_ownership_relationship_id: str, transaction: Transaction):
        """
        删除tag ownership relationship
        """
        self._tag_repository.delete_tag_ownership_relationship_by_id(
            tag_ownership_relationship_id=tag_ownership_relationship_id,
            transaction=transaction,
        )
