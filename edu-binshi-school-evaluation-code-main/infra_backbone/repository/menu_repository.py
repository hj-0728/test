from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.menu import MenuEntity
from infra_backbone.model.menu_model import MenuModel
from infra_backbone.model.view.menu_vm import MenuViewModel


class MenuRepository(BasicRepository):
    def insert_menu(self, data: MenuModel, transaction: Transaction) -> str:
        """
        插入菜单
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=MenuEntity, entity_model=data, transaction=transaction
        )

    def update_menu(
        self,
        data: MenuModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        编辑菜单
        :param data:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        self._update_versioned_entity_by_model(
            entity_cls=MenuEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_menu(self, menu_id: str, transaction: Transaction):
        """
        删除菜单
        :param menu_id:
        :param transaction:
        :return:
        """
        self._delete_versioned_entity_by_id(
            entity_cls=MenuEntity, entity_id=menu_id, transaction=transaction
        )

    def get_user_role_menu_list(self, role_id: str, menu_category: str) -> List[MenuViewModel]:
        """
        获取用户角色允许的菜单
        :param role_id:
        :param menu_category:
        :return:
        """

        sql = """
        select sm.* from st_ability_permission_assign pa1
        inner join st_ability_permission_assign pa2
        on pa2.ability_permission_id = pa1.ability_permission_id
        and pa2.assign_resource_category = 'MENU'
        inner join sv_menu sm on sm.id = pa2.assign_resource_id
        where pa1.assign_resource_id = :role_id
        and pa1.assign_resource_category = 'ROLE'
        and sm.category = :menu_category
        UNION
        SELECT *
        FROM sv_menu
        WHERE array_length(permission_id_list, 1) is NULL
        and category = :menu_category
        ORDER BY seq
        """
        return self._fetch_all_to_model(
            model_cls=MenuViewModel,
            sql=sql,
            params={
                "role_id": role_id,
                "menu_category": menu_category,
            },
        )

    def get_menu_list(self, menu_category: str) -> List[MenuViewModel]:
        """
        获取菜单树
        :param menu_category:
        :return:
        """
        sql = """
        select * from sv_menu
        where category=:menu_category order by sort_info
        """
        return self._fetch_all_to_model(
            model_cls=MenuViewModel,
            sql=sql,
            params={"menu_category": menu_category},
        )

    def get_same_name_menu(
        self, name: str, category: str, menu_id: Optional[str] = None
    ) -> MenuModel:
        """
        获取同名的菜单
        :param name:
        :param category:
        :param menu_id:
        :return:
        """
        sql = """
        select * from st_menu where name = :name
        and category = :category
        """
        if menu_id:
            sql += " and id <> :menu_id "
        return self._fetch_first_to_model(
            model_cls=MenuModel,
            sql=sql,
            params={"name": name, "menu_id": menu_id, "category": category},
        )

    def get_menu_with_children(self, menu_id: str) -> List[MenuViewModel]:
        """
        获取菜单及子菜单
        :param menu_id:
        :return:
        """
        sql = """select * from sv_menu
        where :menu_id = any(tree_id_list)"""
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=MenuViewModel,
            params={"menu_id": menu_id},
        )
