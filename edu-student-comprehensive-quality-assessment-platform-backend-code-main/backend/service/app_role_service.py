from flask import current_app
from flask_jwt_extended import get_jwt_identity
from infra_basic.errors import BusinessError
from infra_basic.redis_manager import RedisManager
from infra_utility.serialize_helper import ORJSONPickle
from loguru import logger

from backend.data.constant import AppRedisConst
from backend.model.view.user_role_profile_vm import UserRoleProfileViewModel
from backend.repository.auth_repository import AuthRepository
from backend.service.redis_service import RedisService
from infra_backbone.data.constant import SymbolConst
from infra_backbone.model.role_model import EnumRoleCode, RoleModel
from infra_backbone.repository.role_repository import RoleRepository


class AppRoleService:
    def __init__(
        self,
        redis_manager: RedisManager,
        role_repository: RoleRepository,
        auth_repository: AuthRepository,
        redis_service: RedisService,
    ):
        self.__redis_client = redis_manager.redis_client
        self.__role_repository = role_repository
        self.__auth_repository = auth_repository
        self.__redis_service = redis_service

    def get_current_role(self) -> RoleModel:
        """
        获取当前角色
        :return:
        """
        try:
            redis_key = AppRedisConst.SESSION_ROLE + SymbolConst.COLON + get_jwt_identity()
            user_profile = ORJSONPickle.decode_model(
                data_content=self.__redis_client.get(name=redis_key),
                data_type=UserRoleProfileViewModel,
            )
            if not user_profile:
                raise BusinessError("未获取到用户角色信息")
            return RoleModel(id=user_profile.role_id, code=user_profile.role_code)
        except Exception as error:
            logger.error(error)
            raise BusinessError("未获取到用户角色信息")

    def set_redis_user_role(self, user_id: str) -> RoleModel:
        """
        设置redis里的用户角色信息
        :param user_id:
        :return:
        """

        dev = current_app.config.get("DEV", None)
        role = None
        if dev and dev.enabled:
            if dev.role_id:
                role = self.__role_repository.get_role_by_id(role_id=dev.role_id)
        if not role:
            user_role_list = self.__auth_repository.fetch_user_role_list(user_id=user_id)
            if not user_role_list:
                raise BusinessError("未获取到用户角色信息")
            role = user_role_list[0]

        self.set_user_role_profile(user_id=user_id, role_id=role.id, role_code=role.code)

        return role

    def set_user_role_profile(self, user_id: str, role_id: str, role_code: str):
        """
        设置用户角色信息
        :param user_id:
        :param role_id:
        :param role_code:
        :return:
        """
        redis_key = AppRedisConst.SESSION_ROLE + SymbolConst.COLON + get_jwt_identity()
        user_profile = UserRoleProfileViewModel(
            role_id=role_id,
            role_code=role_code,
            user_id=user_id,
        )
        self.__redis_service.set(key=redis_key, value=ORJSONPickle.encode_model(user_profile))

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
