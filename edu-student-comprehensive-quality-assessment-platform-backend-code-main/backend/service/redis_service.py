import logging
from typing import Any

import orjson
from flask_jwt_extended import get_jwt_identity
from infra_basic.basic_resource import BasicResource
from infra_basic.errors.input import DataNotFoundError
from infra_basic.errors.permission import NeedLoginError
from infra_basic.redis_manager import RedisManager
from infra_utility.serialize_helper import ORJSONPickle

from backend.data.constant import AppRedisConst
from backend.model.view.user_profile_vm import UserProfileViewModel
from biz_comprehensive.model.period_model import PeriodModel
from biz_comprehensive.service.period_service import PeriodService
from infra_backbone.data.constant import SymbolConst
from infra_backbone.repository.user_repository import UserRepository
from infra_backbone.service.robot_service import RobotService
from infra_backbone.service.role_service import RoleService


class RedisService:
    """
    设置redis相关数据
    """

    def __init__(
        self,
        user_repository: UserRepository,
        role_service: RoleService,
        redis_manager: RedisManager,
        period_service: PeriodService,
        robot_service: RobotService,
    ):
        self.__user_repository = user_repository
        self.__role_service = role_service
        self.__redis_client = redis_manager.redis_client
        self.__period_service = period_service
        self.__robot_service = robot_service

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

    def clear_redis_user_profile_by_user(self, user_category: str, user_id: str):
        """
        根据用户id清除redis中的用户信息
        :param user_category:
        :param user_id:
        :return:
        """
        pattern = (
            AppRedisConst.SESSION + SymbolConst.COLON + user_category + SymbolConst.COLON + user_id
        )
        redis_key_list = self.__redis_client.keys(pattern=pattern + "*")
        for redis_key in redis_key_list:
            self.__redis_client.delete(redis_key)

    def set_redis_user_profile(self, user_profile: UserProfileViewModel, jwt_identity: str):
        """
        设置redis里的外部用户信息
        :param user_profile:
        :param jwt_identity:
        :return:
        """
        redis_key = AppRedisConst.SESSION + SymbolConst.COLON + jwt_identity
        self.__redis_client.set(
            name=redis_key, value=ORJSONPickle.encode_model(user_profile), ex=86400
        )

    def get_redis_user_profile(self) -> UserProfileViewModel:
        """
        获取redis里的外部用户信息
        :return:
        """
        jwt_identity = get_jwt_identity()
        redis_key = AppRedisConst.SESSION + SymbolConst.COLON + jwt_identity
        value = self.__redis_client.get(name=redis_key)
        return ORJSONPickle.decode_model(value, UserProfileViewModel)

    def check_user_profile_by_redis(self):
        """
        检查redis里的用户信息
        :return:
        """
        redis_key = AppRedisConst.SESSION + SymbolConst.COLON + get_jwt_identity()
        is_existed = self.exists(redis_key)
        if not is_existed:
            raise NeedLoginError("需要登录")

    def get_current_semester_period(self) -> PeriodModel:
        """
        获取redis里的当前学期周期信息
        :return:
        """
        redis_key = AppRedisConst.CURRENT_SEMESTER_PERIOD
        value = self.__redis_client.get(name=redis_key)
        if value:
            return ORJSONPickle.decode_model(value, PeriodModel)

        period = self.__period_service.get_current_semester_period_info()
        self.__redis_client.set(name=redis_key, value=ORJSONPickle.encode_model(period), ex=86400)
        return period

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

    def get_redis_robot_handler(self) -> BasicResource:
        """
        获取redis里的机器人handler
        :return:
        """
        redis_key = AppRedisConst.ROBOT_HANDLER
        value = self.__redis_client.get(name=redis_key)
        if value:
            return ORJSONPickle.decode_model(value, BasicResource)
        robot = self.__robot_service.get_system_robot().to_basic_handler()
        self.__redis_client.set(name=redis_key, value=ORJSONPickle.encode_model(robot))
        return robot
