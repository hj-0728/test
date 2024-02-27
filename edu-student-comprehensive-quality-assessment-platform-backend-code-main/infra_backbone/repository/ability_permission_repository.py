from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.ability_permission import AbilityPermissionEntity
from infra_backbone.model.ability_permission_model import AbilityPermissionModel
from infra_backbone.model.edit.ability_permission_em import AbilityPermissionEditModel
from infra_backbone.model.view.ability_permission_vm import AbilityPermissionTreeViewModel


class AbilityPermissionRepository(BasicRepository):
    def insert_ability_permission(
        self, data: AbilityPermissionModel, transaction: Transaction
    ) -> str:
        """
        插入功能权限
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity(
            entity_cls=AbilityPermissionEntity,
            entity_data=data.dict(),
            transaction=transaction,
        )

    def get_ability_permission_by_id(self, ability_permission_id):
        """
        根据id获取功能全西安
        :param ability_permission_id:
        :return:
        """
        sql = """
        select * from st_ability_permission where id = :ability_permission_id
        """
        return self._fetch_first_to_model(
            model_cls=AbilityPermissionModel,
            sql=sql,
            params={"ability_permission_id": ability_permission_id},
        )

    def get_same_name_ability_permission(
        self, name: str, permission_id: Optional[str] = None
    ) -> int:
        """
        获取同名的功能权限
        :param name:
        :param permission_id:
        :return:
        """
        sql = """
        select * from st_ability_permission 
        where name = :name
        """
        if permission_id:
            sql += """and id != :permission_id"""
        return self._fetch_count(
            sql=sql,
            params={
                "name": name,
                "permission_id": permission_id,
            },
        )

    def get_same_code_ability_permission(
        self, code: str, permission_id: Optional[str] = None
    ) -> int:
        """
        获取相同编码的功能权限
        :param code:
        :param permission_id:
        :return:
        """

        sql = """
        select * from st_ability_permission 
        where code = :code
        """
        if permission_id:
            sql += """and id != :permission_id"""
        return self._fetch_count(
            sql=sql,
            params={
                "code": code,
                "permission_id": permission_id,
            },
        )

    def get_ability_permission_tree_list(self) -> List[AbilityPermissionTreeViewModel]:
        """
        功能权限树
        """
        sql = """
        with result as (
        select * from sv_ability_permission 
        order by seq)
        
        select *, row_number() over () as tree_seq  from result 
        
        """
        return self._fetch_all_to_model(
            sql=sql,
            params={},
            model_cls=AbilityPermissionTreeViewModel,
        )

    def update_ability_permission(
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
            entity_cls=AbilityPermissionEntity,
            update_model=permission,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def get_ability_permission_with_children(
        self,
        permission_id: str,
    ) -> List[AbilityPermissionEditModel]:
        """
        获取功能权限及子集
        :param permission_id:
        :return:
        """

        sql = """select * from sv_ability_permission
                where :permission_id = any(tree_id_list)"""
        return self._fetch_all_to_model(
            model_cls=AbilityPermissionEditModel,
            sql=sql,
            params={"permission_id": permission_id},
        )

    def delete_ability_permission(self, permission_id: str, transaction: Transaction):
        """
        删除功能权限
        :param permission_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=AbilityPermissionEntity,
            entity_id=permission_id,
            transaction=transaction,
        )

    def get_ability_permission(self) -> List[AbilityPermissionModel]:
        """
        获取所以的功能权限
        :return:
        """

        sql = """
        select * from st_ability_permission
        """

        return self._fetch_all_to_model(
            model_cls=AbilityPermissionModel,
            sql=sql,
        )
