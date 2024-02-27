from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.ability_permission_assign import AbilityPermissionAssignEntity
from infra_backbone.model.ability_permission_assign_model import (
    AbilityPermissionAssignModel,
    AbilityPermissionAssignTreeViewModel,
)


class AbilityPermissionAssignRepository(BasicRepository):
    def insert_ability_permission_assign(
        self, data: AbilityPermissionAssignModel, transaction: Transaction
    ) -> str:
        """
        插入功能权限分组
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity(
            entity_cls=AbilityPermissionAssignEntity,
            entity_data=data.dict(),
            transaction=transaction,
        )

    def get_ability_permission_assign_em_by_params(
        self, assign_resource_category: str, assign_resource_id: str
    ) -> List[AbilityPermissionAssignModel]:
        """
        获取符合条件的功能权限授权
        """
        sql = """
        select * from st_ability_permission_assign
        where assign_resource_category = :assign_resource_category
        and assign_resource_id = :assign_resource_id
        """
        return self._fetch_all_to_model(
            model_cls=AbilityPermissionAssignModel,
            sql=sql,
            params={
                "assign_resource_category": assign_resource_category,
                "assign_resource_id": assign_resource_id,
            },
        )

    def delete_ability_permission_assign_by_id(
        self, ability_permission_assign_id: str, transaction: Transaction
    ):
        """
        删除功能权限
        :param ability_permission_assign_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=AbilityPermissionAssignEntity,
            entity_id=ability_permission_assign_id,
            transaction=transaction,
        )

    def get_ability_permission_assign_tree(
        self, assign_resource_category: str, assign_resource_id: str
    ) -> List[AbilityPermissionAssignTreeViewModel]:
        """
        获取符合条件的功能权限授权
        """
        sql = """
        with result as(
            select sap.* ,
            case when sga.assign_resource_id is not null then true else false end as granted
            from sv_ability_permission sap
            left join st_ability_permission_assign sga on sap.id = sga.ability_permission_id
            and sga.assign_resource_id= :assign_resource_id AND sga.assign_resource_category = :assign_resource_category
            order by sort_info
        )
        select  * ,row_number() over () as tree_seq from result
        """
        return self._fetch_all_to_model(
            model_cls=AbilityPermissionAssignTreeViewModel,
            sql=sql,
            params={
                "assign_resource_category": assign_resource_category,
                "assign_resource_id": assign_resource_id,
            },
        )
