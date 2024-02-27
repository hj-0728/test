"""
钉钉用户service
"""
import logging
import traceback

from flask import current_app
from flask_jwt_extended import get_jwt_identity
from infra_basic.basic_resource import BasicResource
from infra_basic.errors import BusinessError
from infra_basic.errors.input import DataNotFoundError
from infra_basic.redis_manager import RedisManager
from infra_utility.serialize_helper import ORJSONPickle
from loguru import logger

from backend.data.constant import RedisConst, SymbolConst
from backend.data.enum import EnumDingtalkUserCategory
from backend.model.view.dingtalk_user_for_mobile_vm import DingtalkUserForMobileVm
from backend.model.view.dingtalk_user_vm import DingtalkUserVm
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.model.view.capacity_vm import CapacityVm
from infra_backbone.repository.capacity_repository import CapacityRepository
from infra_dingtalk.repository.dingtalk_k12_parent_repository import DingtalkK12ParentRepository
from infra_dingtalk.repository.dingtalk_user_repository import DingtalkUserRepository


class AppDingtalkUserService:
    def __init__(
        self,
        redis_manager: RedisManager,
        dingtalk_user_repository: DingtalkUserRepository,
        dingtalk_parent_repository: DingtalkK12ParentRepository,
        capacity_repository: CapacityRepository,
    ):
        self.__redis_client = redis_manager.redis_client
        self.__dingtalk_user_repository = dingtalk_user_repository
        self.__dingtalk_parent_repository = dingtalk_parent_repository
        self.__capacity_repository = capacity_repository

    def get_current_dingtalk_user(self):
        """
        获取当前钉钉用户
        """
        dev = current_app.config.get("DEV")
        if dev and dev.enabled:
            user = self.__dingtalk_user_repository.get_dingtalk_user_by_id(
                user_id=dev.dingtalk_user_id
            )
            parent = self.__dingtalk_parent_repository.get_dingtalk_k12_parent_by_id(
                k12_parent_id=dev.dingtalk_k12_parent_id
            )
            if user:
                dingtalk_user = DingtalkUserVm(
                    dingtalk_corp_id=user.dingtalk_corp_id,
                    dingtalk_user_id=user.id,
                    remote_dingtalk_user_id=user.remote_user_id,
                    user_category=EnumDingtalkUserCategory.DINGTALK_USER.name,
                )
            elif parent:
                dingtalk_user = DingtalkUserVm(
                    dingtalk_corp_id=parent.dingtalk_corp_id,
                    dingtalk_k12_parent_id=parent.id,
                    remote_dingtalk_k12_parent_id=parent.remote_user_id,
                    user_category=EnumDingtalkUserCategory.DINGTALK_K12_PARENT.name,
                )
            else:
                raise DataNotFoundError("该用户")
            return dingtalk_user
        try:
            redis_key = RedisConst.SESSION + SymbolConst.COLON + get_jwt_identity()
            return ORJSONPickle.decode_model(
                data_content=self.__redis_client.get(name=redis_key),
                data_type=DingtalkUserVm,
            )
        except Exception as error:
            traceback.print_exc()
            logging.error(error)
            raise DataNotFoundError("身份信息")

    def get_current_dingtalk_handler(self) -> BasicResource:
        """
        获得当前dingtalk_user_id
        :return:
        """
        dev = current_app.config.get("DEV", None)
        if dev and dev.enabled:
            if not dev.dingtalk_user_id:
                raise DataNotFoundError("未获取到配置文件dev中的dingtalk_user_id")
            return dev.dingtalk_user_id
        redis_key = RedisConst.SESSION + SymbolConst.COLON + get_jwt_identity()
        user_profile = ORJSONPickle.decode_model(
            data_content=self.__redis_client.get(name=redis_key),
            data_type=DingtalkUserVm,
        )
        logger.info(f"user_profile: {user_profile}")
        return BasicResource(
            id=user_profile.res_id(),
            category=user_profile.res_category(),
        )

    def get_dingtalk_user_info(self, remote_user_id: str, dingtalk_corp_id: str):
        """
        获取当前钉钉用户信息
        """
        dingtalk_user = self.__dingtalk_user_repository.get_dingtalk_user_by_remote_user_id(
            remote_user_id=remote_user_id, dingtalk_corp_id=dingtalk_corp_id
        )
        dingtalk_parent = (
            self.__dingtalk_parent_repository.get_dingtalk_k12_parent_by_remote_user_id(
                remote_user_id=remote_user_id, dingtalk_corp_id=dingtalk_corp_id
            )
        )
        if not dingtalk_user and not dingtalk_parent:
            raise BusinessError("未找到钉钉用户信息")
        capacity_list = []
        if dingtalk_user:
            capacity_list = self.__capacity_repository.get_k12_capacity_list_by_dingtalk_user_id(
                dingtalk_user_id=dingtalk_user.id
            )
        if dingtalk_parent:
            capacity_list.append(
                CapacityVm(name=EnumCapacityCode.PARENT.value, code=EnumCapacityCode.PARENT.name)
            )

        if not capacity_list:
            raise BusinessError("未找到用户职责信息")
        if dingtalk_user:
            return DingtalkUserForMobileVm(
                id=dingtalk_user.id,
                name=dingtalk_user.name if dingtalk_user else None,
                user_category=EnumDingtalkUserCategory.DINGTALK_USER.name,
                dingtalk_corp_id=dingtalk_user.dingtalk_corp_id,
                capacity_list=capacity_list,
                current_capacity=capacity_list[0],
            )

        return DingtalkUserForMobileVm(
            id=dingtalk_user.id,
            name=dingtalk_user.name if dingtalk_user else None,
            user_category=EnumDingtalkUserCategory.DINGTALK_K12_PARENT.name,
            dingtalk_corp_id=dingtalk_user.dingtalk_corp_id,
            capacity_list=capacity_list,
            current_capacity=capacity_list[0],
        )
