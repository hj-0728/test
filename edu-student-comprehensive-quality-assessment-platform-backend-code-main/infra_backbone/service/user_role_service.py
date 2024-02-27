from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction

from infra_backbone.model.user_role_model import SaveUserRoleModel, UserRoleModel
from infra_backbone.repository.user_role_repository import UserRoleRepository


class UserRoleService:
    def __init__(
        self,
        user_role_repository: UserRoleRepository,
    ):
        self.__user_role_repository = user_role_repository

    def save_user_role(self, data: SaveUserRoleModel, transaction: Transaction):
        """
        保存用户角色
        :param data:
        :param transaction:
        :return:
        """
        user_role_list = self.__user_role_repository.get_user_role_list_by_user_id(
            user_id=data.user_id,
        )
        for user_role in user_role_list:
            self.__user_role_repository.delete_user_role(
                user_role_id=user_role.id,
                transaction=transaction,
            )
        for role_id in data.role_id_list:
            self.__user_role_repository.insert_user_role(
                data=UserRoleModel(
                    user_id=data.user_id,
                    role_id=role_id,
                ),
                transaction=transaction,
            )

    def get_user_role_model(self, user_id: str, role_id: str) -> UserRoleModel:
        """
        获取用户角色
        """
        result = self.__user_role_repository.get_user_role_model_by_user_id_and_role_id(
            user_id=user_id, role_id=role_id
        )
        if not result:
            raise BusinessError("未获取到用户角色信息")
        return result
