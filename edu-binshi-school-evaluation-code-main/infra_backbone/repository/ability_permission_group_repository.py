from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.ability_permission_group import AbilityPermissionGroupEntity
from infra_backbone.model.ability_permission_group_model import AbilityPermissionGroupModel
from infra_backbone.model.edit.ability_permission_em import AbilityPermissionEditModel


class AbilityPermissionGroupRepository(BasicRepository):
    def insert_ability_permission_group(
        self, data: AbilityPermissionGroupModel, transaction: Transaction
    ) -> str:
        """
        插入功能权限分组
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity(
            entity_cls=AbilityPermissionGroupEntity,
            entity_data=data.dict(),
            transaction=transaction,
        )

    def get_same_name_ability_permission_group(
        self, name: str, ability_permission_group_id: Optional[str] = None
    ) -> int:
        """
        获取同名的功能权限
        :param name:
        :param ability_permission_group_id:
        :return:
        """
        sql = """
        select * from st_ability_permission_group 
        where name = :name
        """
        if ability_permission_group_id:
            sql += """and id != :ability_permission_group_id"""
        return self._fetch_count(
            sql=sql,
            params={
                "name": name,
                "ability_permission_group_id": ability_permission_group_id,
            },
        )

    def get_same_code_ability_permission_group(
        self, code: str, ability_permission_group_id: Optional[str] = None
    ) -> int:
        """
        获取相同编码的功能权限
        :param code:
        :param ability_permission_group_id:
        :return:
        """

        sql = """
        select * from st_ability_permission_group 
        where code = :code
        """
        if ability_permission_group_id:
            sql += """and id != :ability_permission_group_id"""
        return self._fetch_count(
            sql=sql,
            params={
                "code": code,
                "ability_permission_group_id": ability_permission_group_id,
            },
        )

    def update_ability_permission_group(
        self,
        permission: AbilityPermissionEditModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新功能权限
        :param permission:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        return self._update_versioned_entity_by_model(
            entity_cls=AbilityPermissionGroupEntity,
            update_model=permission,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_ability_permission_group(self, permission_group_id: str, transaction: Transaction):
        """
        删除功能权限
        :param permission_group_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=AbilityPermissionGroupEntity,
            entity_id=permission_group_id,
            transaction=transaction,
        )
