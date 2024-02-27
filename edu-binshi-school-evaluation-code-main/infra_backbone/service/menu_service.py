from typing import List

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.algorithm.tree import list_to_tree

from infra_backbone.model.menu_model import MenuModel
from infra_backbone.model.role_model import EnumRoleCode
from infra_backbone.model.view.menu_vm import MenuViewModel
from infra_backbone.repository.menu_repository import MenuRepository


class MenuService:
    def __init__(
        self,
        menu_repository: MenuRepository,
    ):
        self.__menu_repository = menu_repository

    def get_current_role_menu_tree(self, role_id: str, menu_category: str):
        """
        获取当前角色的菜单路径列表
        :param role_id:
        :param menu_category:
        :return:
        """
        category_menu_list = self.__menu_repository.get_user_role_menu_list(
            role_id=role_id, menu_category=menu_category
        )
        return list_to_tree(
            original_list=category_menu_list,
            tree_node_type=MenuViewModel,
        )

    def get_current_role_menu_list_for_mobile(
        self, role_id: str, role_code: str, menu_category: str
    ):
        """
        手机端 获取当前角色的菜单列表
        :param role_id:
        :param role_code:
        :param menu_category:
        :return:
        """
        data = self.__menu_repository.get_user_role_menu_list(
            role_id=role_id, menu_category=menu_category
        )
        result = []
        for idx, menu in enumerate(data):
            if role_code == EnumRoleCode.TEACHER.name:
                if menu.path not in ["/evaluation-statistics/index", "/ranking/LUCKY_COIN"]:
                    result.append(menu)
            else:
                if menu.path != "/ranking/LUCKY_COIN":
                    result.append(menu)
        return result

    def build_full_menu_tree(self, menu_category: str) -> List[MenuViewModel]:
        """
        构建菜单树
        :param menu_category:
        :return:
        """
        return list_to_tree(
            original_list=self.__menu_repository.get_menu_list(menu_category=menu_category),
            tree_node_type=MenuViewModel,
        )

    def add_menu(self, menu: MenuModel, transaction: Transaction):
        """
        添加菜单
        :param menu:
        :param transaction:
        :return:
        """
        if self.__menu_repository.get_same_name_menu(name=menu.name, category=menu.category):
            raise BusinessError("已存在相同的菜单")
        return self.__menu_repository.insert_menu(data=menu, transaction=transaction)

    def edit_menu(self, menu: MenuModel, transaction: Transaction):
        """
        编辑菜单
        :param menu:
        :param transaction:
        :return:
        """
        if self.__menu_repository.get_same_name_menu(
            name=menu.name, category=menu.category, menu_id=menu.id
        ):
            raise BusinessError("已存在相同的菜单")
        self.__menu_repository.update_menu(
            data=menu,
            transaction=transaction,
            limited_col_list=["name", "path", "icon"],
        )

    def delete_menu(self, menu_id: str, transaction: Transaction):
        """
        删除菜单
        :param menu_id:
        :param transaction:
        :return:
        """
        menu_list = self.__menu_repository.get_menu_with_children(menu_id=menu_id)
        for menu in menu_list:
            if not menu.id:
                continue
            self.__menu_repository.delete_menu(
                menu_id=menu.id,
                transaction=transaction,
            )

    def update_menu_sort(self, menu_list: List[MenuModel], transaction: Transaction):
        """
        更新菜单的排序
        :param menu_list:
        :param transaction:
        :return:
        """

        for menu in menu_list:
            self.__menu_repository.update_menu(
                data=menu,
                transaction=transaction,
                limited_col_list=["parent_id", "seq"],
            )
