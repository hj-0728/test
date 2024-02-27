from typing import List

from flask import current_app
from flask_jwt_extended import get_jwt_identity
from infra_basic.errors.input import DataNotFoundError
from infra_basic.redis_manager import RedisManager
from infra_utility.serialize_helper import ORJSONPickle

from backend.data.constant import RedisConst
from infra_backbone.data.constant import SymbolConst
from infra_backbone.model.role_model import EnumRoleCode, RoleModel
from infra_backbone.model.view.user_profile_vm import UserProfileViewModel
from infra_backbone.repository.role_repository import RoleRepository


class AppRoleService:
    def __init__(
        self,
        redis_manager: RedisManager,
        role_repository: RoleRepository,
    ):
        self.__redis_client = redis_manager.redis_client
        self.__role_repository = role_repository

    def get_current_role(self) -> RoleModel:
        """
        获取当前角色
        :return:
        """
        dev = current_app.config.get("DEV", None)
        if dev and dev.enabled:
            if not dev.role_id:
                raise DataNotFoundError("未获取到配置文件dev中的role_id")
            role = self.__role_repository.get_role_by_id(role_id=dev.role_id)
        else:
            redis_key = RedisConst.SESSION + SymbolConst.COLON + get_jwt_identity()
            user_profile = ORJSONPickle.decode_model(
                data_content=self.__redis_client.get(name=redis_key),
                data_type=UserProfileViewModel,
            )
            role = RoleModel(id=user_profile.role_id, code=user_profile.role_code)
        if not role or not role.id:
            raise DataNotFoundError("未获取到角色")
        return role

    def get_current_role_id(self) -> str:
        """
        获得当前角色id
        :return:
        """
        return self.get_current_role().id

    def get_current_role_code(self) -> str:
        """
        获得当前角色code
        :return:
        """
        return self.get_current_role().code

    def get_teacher_role_list(self, role_code: str) -> List[RoleModel]:
        """
        获取老师角色列表(即除了学生的角色)
        :param role_code:
        :return:
        """

        role_list = self.__role_repository.get_role_filter_list(role_code=role_code)

        return [x for x in role_list if x.code != EnumRoleCode.STUDENT.name]
