from typing import List

import orjson
from flask import current_app
from flask_jwt_extended import get_jwt_identity
from infra_basic.errors.input import DataNotFoundError
from infra_basic.redis_manager import RedisManager

from backend.data.constant import AppRedisConst
from backend.service.redis_service import RedisService
from infra_backbone.data.constant import SymbolConst
from infra_backbone.repository.user_repository import UserRepository


class AppAbilityPermissionService:
    def __init__(
        self,
        redis_manager: RedisManager,
        user_repository: UserRepository,
        redis_service: RedisService,
    ):
        self.__redis_client = redis_manager.redis_client
        self.__user_repository = user_repository
        self.__redis_service = redis_service

    def get_current_ability_permission_id_list(self) -> List[str]:
        """
        获得当前功能权限 列表
        :return:
        """
        dev = current_app.config.get("DEV", None)
        if dev and dev.enabled:
            if not dev.role_id:
                raise DataNotFoundError("未获取到配置文件dev中的role_id")
            return dev.role_id
        redis_key = AppRedisConst.SESSION_ABILITY_PER + SymbolConst.COLON + get_jwt_identity()
        ability_permission_id_list = orjson.loads(self.__redis_client.get(name=redis_key))
        return ability_permission_id_list

    def set_redis_user_ability_permission(self, user_id: str, role_id: str):
        """
        设置redis里的用户信息
        :param user_id:
        :param role_id:
        :return:
        """
        redis_key = AppRedisConst.SESSION_ABILITY_PER + SymbolConst.COLON + get_jwt_identity()

        user_ability_per_list = self.__user_repository.get_user_ability_permission(
            user_id=user_id, role_id=role_id
        )

        if not user_ability_per_list:
            raise DataNotFoundError("未获取到用户相关功能权限信息")

        ability_permission_id_list = list(
            set(map(lambda x: x.ability_permission_id, user_ability_per_list))
        )

        self.__redis_service.set(key=redis_key, value=orjson.dumps(ability_permission_id_list))
