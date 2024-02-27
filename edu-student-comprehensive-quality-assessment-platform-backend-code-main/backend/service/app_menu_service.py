from typing import List

from infra_utility.algorithm.tree import list_to_tree

from backend.model.view.sidebar_menu_vm import SidebarViewModel
from infra_backbone.repository.menu_repository import MenuRepository


class AppMenuService:
    def __init__(
        self,
        menu_repository: MenuRepository,
    ):
        self.__menu_repository = menu_repository

    def get_user_sidebar_menu(self, role_id: str, menu_category: str) -> List[SidebarViewModel]:
        """
        获取用户侧边栏菜单
        :param role_id:
        :param menu_category:
        :return:
        """

        category_menu_list = self.__menu_repository.get_user_role_menu_list(
            role_id=role_id, menu_category=menu_category
        )
        return list_to_tree(
            original_list=category_menu_list,
            tree_node_type=SidebarViewModel,
        )
