from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.ability_permission_tree import AbilityPermissionTreeEntity
from infra_backbone.model.ability_permission_tree_model import AbilityPermissionTreeModel


class AbilityPermissionTreeRepository(BasicRepository):
    def insert_ability_permission_tree(
        self, data: AbilityPermissionTreeModel, transaction: Transaction
    ) -> str:
        """
        插入功能权限树
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity(
            entity_cls=AbilityPermissionTreeEntity,
            entity_data=data.dict(),
            transaction=transaction,
        )

    def get_max_seq_by_ability_permission_group_id(
        self, ability_permission_group_id: Optional[str] = None
    ):
        """
        获取功能权限树最大seq
        :param ability_permission_group_id:
        :return:
        """
        sql = """
        SELECT max(sap.seq) AS max_seq FROM st_ability_permission_tree sap
        """
        if ability_permission_group_id:
            sql += """
            WHERE sap.ability_permission_group_id=:ability_permission_group_id
            """
        else:
            sql += """
            WHERE sap.ability_permission_group_id IS NULL
            """
        data = self._execute_sql(
            sql=sql,
            params={
                "ability_permission_group_id": ability_permission_group_id,
            },
        )
        return data

    def delete_ability_permission_tree(
        self, ability_permission_tree_id: str, transaction: Transaction
    ):
        """
        删除功能权限
        :param ability_permission_tree_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=AbilityPermissionTreeEntity,
            entity_id=ability_permission_tree_id,
            transaction=transaction,
        )
