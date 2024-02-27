from typing import List

import orjson
from flask import current_app
from flask_jwt_extended import get_jwt_identity
from infra_basic.errors.input import DataNotFoundError
from infra_basic.redis_manager import RedisManager

from backend.data.constant import RedisConst
from infra_backbone.data.constant import SymbolConst


class AppAbilityPermissionService:
    def __init__(
        self,
        redis_manager: RedisManager,
    ):
        self.__redis_client = redis_manager.redis_client

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
        redis_key = RedisConst.SESSION_ABILITY_PER + SymbolConst.COLON + get_jwt_identity()
        ability_permission_id_list = orjson.loads(self.__redis_client.get(name=redis_key))
        return ability_permission_id_list
