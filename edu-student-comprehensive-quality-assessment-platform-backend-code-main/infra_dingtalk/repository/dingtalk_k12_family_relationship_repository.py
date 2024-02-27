"""
钉钉 k12 学生家庭关系
"""

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_dingtalk.entity.dingtalk_k12_family_relationship import (
    DingtalkK12FamilyRelationshipEntity,
)
from infra_dingtalk.model.dingtalk_k12_family_relationship_model import (
    DingtalkK12FamilyRelationshipModel,
)


class DingtalkK12FamilyRelationshipRepository(BasicRepository):
    """
    钉钉 k12 学生家庭关系
    """

    def insert_dingtalk_k12_family_relationship(
        self, family: DingtalkK12FamilyRelationshipModel, transaction: Transaction
    ):
        """
        插入k12的学生家长关系
        """
        self._insert_versioned_entity_by_model(
            entity_cls=DingtalkK12FamilyRelationshipEntity,
            entity_model=family,
            transaction=transaction,
        )

    def update_dingtalk_k12_family_relationship(
        self, family: DingtalkK12FamilyRelationshipModel, transaction: Transaction
    ):
        """
        更新k12的学生家长关系
        """
        self._update_versioned_entity_by_model(
            entity_cls=DingtalkK12FamilyRelationshipEntity,
            update_model=family,
            transaction=transaction,
        )

    def delete_dingtalk_k12_family_relationship(self, family_id: str, transaction: Transaction):
        """
        删除k12的学生家长关系
        """
        self._delete_versioned_entity_by_id(
            entity_cls=DingtalkK12FamilyRelationshipEntity,
            entity_id=family_id,
            transaction=transaction,
        )
