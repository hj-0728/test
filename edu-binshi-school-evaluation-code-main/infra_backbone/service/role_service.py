from typing import List, Optional

from infra_basic.errors import BusinessError
from infra_basic.query_params import PageFilterParams
from infra_basic.transaction import Transaction

from infra_backbone.model.role_model import RoleModel
from infra_backbone.repository.role_repository import RoleRepository


class RoleService:
    def __init__(
        self,
        role_repository: RoleRepository,
    ):
        self.__role_repository = role_repository

    def get_role_list_by_user_id(self, user_id: str):
        """
        根据用户id获得角色列表
        :param user_id:
        :return:
        """
        role_list = self.__role_repository.get_role_list_by_user_id(
            user_id=user_id,
        )
        if len(role_list) == 0:
            raise BusinessError("当前用户未配置相关角色")
        return role_list

    def get_first_role_info_by_user_id(self, user_id: str):
        """
        根据用户id获得第一个角色信息
        :param user_id:
        :return:
        """
        return self.get_role_list_by_user_id(user_id=user_id)[0]

    def get_all_role_list(self):
        """
        获取所有角色
        :return:
        """
        return self.__role_repository.get_all_role_list()

    def get_user_role_list(self, user_id: str):
        """
        获取用户的角色
        :param user_id:
        :return:
        """
        return self.__role_repository.get_role_list_by_user_id(
            user_id=user_id,
        )

    def change_is_activated(self, role: RoleModel, transaction: Transaction):
        """
        改变激活状态
        :param role:
        :param transaction:
        :return:
        """

        self.__role_repository.update_role_info(
            role=role, transaction=transaction, col_list=["is_activated"]
        )

    def get_role_info(
        self,
        role_id: str,
    ) -> Optional[RoleModel]:
        """
        获取角色信息
        :param role_id:
        :return:
        """
        return self.__role_repository.get_role_by_id(role_id=role_id)

    def save_role(self, role: RoleModel, transaction: Transaction):
        """
        新增或更新角色信息
        :param role:
        :param transaction:
        :return:
        """
        is_existed_name = self.__role_repository.get_role_by_name(name=role.name, filter_id=role.id)
        is_existed_code = self.__role_repository.get_role_by_code(code=role.code, filter_id=role.id)
        if is_existed_name:
            raise BusinessError("已存在相同名称的角色")
        if is_existed_code:
            raise BusinessError("已存在相同编码的角色")
        if role.id:
            role_info = self.__role_repository.get_role_by_id(role_id=role.id)
            if not role_info:
                raise BusinessError("未获取到角色相关信息")
            return self.__role_repository.update_role_info(
                role=role,
                transaction=transaction,
                col_list=["name", "comments", "is_activated"],
            )
        return self.__role_repository.insert_role(data=role, transaction=transaction)

    def get_role_by_code(
        self,
        code: str,
    ) -> Optional[RoleModel]:
        """
        根据编码获取角色
        :param code:
        :return:
        """
        return self.__role_repository.get_role_by_code(code=code)

    def get_role_list_page_info(self, query_params: PageFilterParams, role_code: str):
        """
        获取角色列表页信息
        """
        return self.__role_repository.get_role_list_page_info(
            query_params=query_params, current_role_code=role_code
        )

    def get_role_filter_list(self, role_code: str):
        return self.__role_repository.get_role_filter_list(role_code=role_code)
