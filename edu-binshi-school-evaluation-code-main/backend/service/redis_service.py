import logging
from typing import Any

import orjson
from flask_jwt_extended import get_jwt_identity
from infra_basic.errors.input import DataNotFoundError
from infra_basic.redis_manager import RedisManager
from infra_utility.serialize_helper import ORJSONPickle

from backend.data.constant import RedisConst
from backend.data.enum import EnumDingtalkUserCategory
from backend.model.view.dingtalk_user_vm import DingtalkUserVm
from backend.model.view.period_vm import PeriodVm
from infra_backbone.data.constant import SymbolConst
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.repository.user_repository import UserRepository
from infra_backbone.service.role_service import RoleService
from infra_dingtalk.repository.dingtalk_k12_parent_repository import DingtalkK12ParentRepository
from infra_dingtalk.repository.dingtalk_user_repository import DingtalkUserRepository


class RedisService:
    """
    设置redis相关数据
    """

    def __init__(
        self,
        user_repository: UserRepository,
        role_service: RoleService,
        redis_manager: RedisManager,
        dingtalk_k12_parent_repository: DingtalkK12ParentRepository,
        dingtalk_user_repository: DingtalkUserRepository,
    ):
        self.__user_repository = user_repository
        self.__role_service = role_service
        self.__redis_client = redis_manager.redis_client
        self.__dingtalk_k12_parent_repository = dingtalk_k12_parent_repository
        self.__dingtalk_user_repository = dingtalk_user_repository

    def add_redis_user_profile(
        self,
        user_id: str,
        jwt_identity: str,
    ):
        """

        :param user_id:
        :param jwt_identity:
        :return:
        """
        role_info = self.__role_service.get_first_role_info_by_user_id(user_id=user_id)
        redis_key = RedisConst.SESSION + SymbolConst.COLON + jwt_identity
        self.set_redis_user_profile(user_id=user_id, role_id=role_info.id, redis_key=redis_key)
        ability_permission_redis_key = (
            RedisConst.SESSION_ABILITY_PER + SymbolConst.COLON + jwt_identity
        )

        self.set_redis_user_ability_permission(
            user_id=user_id,
            role_id=role_info.id,
            redis_key=ability_permission_redis_key,
        )

    def update_redis_user_profile_current_role(self, role_id: str, user_id: str):
        """
        更新redis用户信息的当前角色
        :param role_id:
        :param user_id:
        :return:
        """
        redis_key = RedisConst.SESSION + SymbolConst.COLON + get_jwt_identity()
        self.set_redis_user_profile(user_id=user_id, role_id=role_id, redis_key=redis_key)

    def set_redis_user_profile(self, user_id: str, role_id: str, redis_key: str):
        """
        设置redis里的用户信息
        :param user_id:
        :param role_id:
        :param redis_key:
        :return:
        """
        user_profile = self.__user_repository.get_user_profile(user_id=user_id, role_id=role_id)
        if not user_profile:
            raise DataNotFoundError("用户相关信息")
        self.__redis_client.set(
            name=redis_key, value=ORJSONPickle.encode_model(user_profile), ex=86400
        )

    def set_redis_user_ability_permission(self, user_id: str, role_id: str, redis_key: str):
        """
        设置redis里的用户信息
        :param user_id:
        :param role_id:
        :param redis_key:
        :return:
        """
        user_ability_per_list = self.__user_repository.get_user_ability_permission(
            user_id=user_id, role_id=role_id
        )
        if not user_ability_per_list:
            raise DataNotFoundError("用户相关功能权限信息")
        ability_permission_id_list = list(
            set(map(lambda x: x.ability_permission_id, user_ability_per_list))
        )
        self.__redis_client.set(
            name=redis_key, value=orjson.dumps(ability_permission_id_list), ex=86400
        )

    def clear_redis_user_profile_by_user_id(self, user_category: str, user_id: str):
        """
        根据用户id清除redis中的用户信息
        :param user_category:
        :param user_id:
        :return:
        """
        pattern = (
            RedisConst.SESSION + SymbolConst.COLON + user_category + SymbolConst.COLON + user_id
        )
        redis_key_list = self.__redis_client.keys(pattern=pattern + "*")
        for redis_key in redis_key_list:
            self.__redis_client.delete(redis_key)

    def set_redis_dingtalk_user_profile(self, user_profile: DingtalkUserVm, jwt_identity: str):
        """
        设置redis里的钉钉用户信息
        :param user_profile:
        :param jwt_identity:
        :return:
        """
        redis_key = RedisConst.SESSION + SymbolConst.COLON + jwt_identity
        self.__redis_client.set(
            name=redis_key, value=ORJSONPickle.encode_model(user_profile), ex=86400
        )

    def set_redis_period(self, period_profile: PeriodVm, redis_key: str = None):
        """
        设置redis里的阶段信息
        :param period_profile:
        :param redis_key:
        :return:
        """

        if not redis_key:
            redis_key = RedisConst.PERIOD + SymbolConst.COLON + get_jwt_identity()

        self.__redis_client.set(
            name=redis_key, value=ORJSONPickle.encode_model(period_profile), ex=86400
        )

    def update_redis_user_profile_current_capacity_for_mobile(
        self, capacity_code: str, remote_user_id: str, dingtalk_corp_id: str
    ):
        """
        手机端 更新redis用户信息的当前角色
        :param capacity_code:
        :param remote_user_id:
        :param dingtalk_corp_id:
        :return:
        """
        redis_key = RedisConst.SESSION + SymbolConst.COLON + get_jwt_identity()
        dingtalk_user = self.__dingtalk_user_repository.get_dingtalk_user_by_remote_user_id(
            remote_user_id=remote_user_id,
            dingtalk_corp_id=dingtalk_corp_id,
        )
        dingtalk_parent = (
            self.__dingtalk_k12_parent_repository.get_dingtalk_k12_parent_by_remote_user_id(
                remote_user_id=remote_user_id,
                dingtalk_corp_id=dingtalk_corp_id,
            )
        )
        if capacity_code == EnumCapacityCode.PARENT.name:
            if not dingtalk_parent:
                raise DataNotFoundError("用户相关信息")
            user_profile = DingtalkUserVm(
                dingtalk_user_id=dingtalk_user.id if dingtalk_user else None,
                dingtalk_k12_parent_id=dingtalk_parent.id if dingtalk_parent else None,
                dingtalk_corp_id=dingtalk_corp_id,
                remote_user_id=remote_user_id,
                user_category=EnumDingtalkUserCategory.DINGTALK_K12_PARENT.name,
                capacity_code=capacity_code,
            )
        else:
            if not dingtalk_user:
                raise DataNotFoundError("用户相关信息")
            user_profile = DingtalkUserVm(
                dingtalk_user_id=dingtalk_user.id if dingtalk_user else None,
                dingtalk_k12_parent_id=dingtalk_parent.id if dingtalk_parent else None,
                dingtalk_corp_id=dingtalk_corp_id,
                remote_user_id=remote_user_id,
                user_category=EnumDingtalkUserCategory.DINGTALK_USER.name,
                capacity_code=capacity_code,
            )
        self.__redis_client.set(
            name=redis_key, value=ORJSONPickle.encode_model(user_profile), ex=86400
        )

    def set(self, key: str, value: Any, ex: int = 86400):
        """
        向redis里记录值
        :return:
        """
        try:
            self.__redis_client.set(name=key, value=value, ex=ex)
        except Exception as error:
            logging.error(error)

    def get(self, key: str):
        """
        读取redis里面的值
        :return:
        """
        try:
            value = self.__redis_client.get(name=key)
            return orjson.loads(value)
        except Exception as error:
            logging.error(error)
            return None

    def delete(self, key: str):
        """
        删除redis里面的值
        """
        try:
            self.__redis_client.delete(key)
        except Exception as error:
            logging.error(error)
        return None

    def exists(self, key: str):
        """
        redis里面的值是否存在
        """
        try:
            return self.__redis_client.exists(key)
        except Exception as error:
            logging.error(error)
