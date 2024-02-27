from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.user_role import UserRoleEntity
from infra_backbone.model.user_role_model import UserRoleModel


class UserRoleRepository(BasicRepository):
    def insert_user_role(self, data: UserRoleModel, transaction: Transaction) -> str:
        """
        插入用户角色
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=UserRoleEntity,
            entity_model=data,
            transaction=transaction,
        )

    def update_user_role(
        self,
        data: UserRoleModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新用户人员信息
        :param data:
        :param transaction:
        :param limited_col_list:
        :return:
        """

        return self._update_versioned_entity_by_model(
            entity_cls=UserRoleEntity,
            update_model=data,
            limited_col_list=limited_col_list,
            transaction=transaction,
        )

    def delete_user_role(self, user_role_id: str, transaction: Transaction):
        """
        删除用户角色
        :param user_role_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=UserRoleEntity,
            entity_id=user_role_id,
            transaction=transaction,
        )

    def get_user_role_list_by_user_id(self, user_id: str) -> List[UserRoleModel]:
        """
        根据用户id获得用户角色列表
        :param user_id:
        :return:
        """
        sql = """
        SELECT * FROM st_user_role WHERE user_id = :user_id
        """
        return self._fetch_all_to_model(
            sql=sql, model_cls=UserRoleModel, params={"user_id": user_id}
        )

    def get_user_role_model_by_user_id_and_role_id(
        self, user_id: str, role_id: str
    ) -> Optional[UserRoleModel]:
        """
        根据用户id、角色id获得用户角色
        :param user_id:
        :param role_id:
        :return:
        """
        sql = """
              SELECT ur.*,sr.code as role_code  FROM st_user_role ur 
              inner join st_role sr on sr.id = ur.role_id
               WHERE ur.user_id = :user_id and ur.role_id = :role_id
              """
        return self._fetch_first_to_model(
            sql=sql, model_cls=UserRoleModel, params={"user_id": user_id, "role_id": role_id}
        )
