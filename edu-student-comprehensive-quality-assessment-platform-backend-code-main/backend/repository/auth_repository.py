from typing import List

from infra_basic.basic_repository import BasicRepository

from backend.model.view.sidebar_menu_vm import SidebarViewModel
from infra_backbone.model.role_model import RoleModel


class AuthRepository(BasicRepository):
    def fetch_user_sidebar_menu(self) -> List[SidebarViewModel]:
        """
        获取用户侧边栏菜单
        :return:
        """
        sql = """select id, parent_id, name, path, icon, seq from sv_menu"""
        return self._fetch_all_to_model(sql=sql, model_cls=SidebarViewModel)

    def fetch_user_role_list(self, user_id: str) -> List[RoleModel]:
        """
        获取用户角色列表
        :param user_id:
        :return:
        """
        sql = """
        select r.* from st_user_role ur INNER JOIN st_role r on ur.role_id=r.id
        where is_activated is true
        """
        return self._fetch_all_to_model(sql=sql, model_cls=RoleModel)
