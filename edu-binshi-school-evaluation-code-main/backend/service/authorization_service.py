import logging
from typing import Dict, Union

from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.token_helper import generate_random_string

from backend.data.constant import RedisConst, SymbolConst
from backend.data.enum import EnumDingtalkUserCategory
from backend.model.view.dingtalk_user_vm import DingtalkUserVm
from backend.service.redis_service import RedisService
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.model.view.capacity_vm import CapacityVm
from infra_backbone.repository.capacity_repository import CapacityRepository
from infra_backbone.service.route_service import RouteService
from infra_dingtalk.repository.dingtalk_corp_repository import DingtalkCorpRepository
from infra_dingtalk.repository.dingtalk_k12_parent_repository import DingtalkK12ParentRepository
from infra_dingtalk.repository.dingtalk_user_repository import DingtalkUserRepository
from infra_dingtalk.service.auth_service import AuthService


class AuthorizationService:
    def __init__(
        self,
        route_service: RouteService,
        redis_service: RedisService,
        dingtalk_user_repository: DingtalkUserRepository,
        dingtalk_k12_parent_repository: DingtalkK12ParentRepository,
        dingtalk_corp_repository: DingtalkCorpRepository,
        dingtalk_auth_service: AuthService,
        capacity_repository: CapacityRepository,
    ):
        self.__route_service = route_service
        self.__redis_service = redis_service
        self.__dingtalk_corp_repository = dingtalk_corp_repository
        self.__dingtalk_auth_service = dingtalk_auth_service
        self.__dingtalk_user_repository = dingtalk_user_repository
        self.__dingtalk_k12_parent_repository = dingtalk_k12_parent_repository
        self.__capacity_repository = capacity_repository

    @staticmethod
    def build_token_data(jwt_identity: Union[Dict, str]) -> Dict:
        """
        生成token
        :param jwt_identity:
        :return:
        """
        access_token = create_access_token(identity=jwt_identity)
        refresh_token = create_refresh_token(identity=jwt_identity)
        return {"access_token": access_token, "refresh_token": refresh_token}

    def prepare_route(self, transaction: Transaction):
        """
        处理当前flask里面的路由信息
        :param transaction:
        :return:
        """
        flask_app_route_list = list(current_app.url_map.iter_rules())
        flask_app_route_set = {r.rule for r in flask_app_route_list}
        ignore_path = [
            "/api/web/user/login",
            "/api/favicon.ico",
            "/static/<path:filename>",
            "/api/web/user/get-login-validate-image",
            "/api/web/storage/tinymce-uploads",
        ]
        self.__route_service.refresh_route(
            flask_app_route_set=flask_app_route_set,
            ignore_path=ignore_path,
            transaction=transaction,
            remove_unused=False,
        )

    def get_current_dingtalk_corp_id(self) -> str:
        """
        在一个项目下只会一个钉钉的场景里面写的
        所以默认返回第一个
        """
        dingtalk_corp_list = self.__dingtalk_corp_repository.get_dingtalk_corp()
        if not dingtalk_corp_list:
            raise BusinessError("未获取到钉钉")
        return dingtalk_corp_list[0].id

    def get_dingtalk_oauth_jwt_token(self, code: str):
        """
        获取钉钉oauth token
        """
        dingtalk_corp_id = self.get_current_dingtalk_corp_id()
        oauth_result = self.__dingtalk_auth_service.oauth_get_remote_user_info(
            dingtalk_corp_id=dingtalk_corp_id,
            code=code,
        )
        logging.info(f"钉钉身份验证结果：{oauth_result}")
        if not oauth_result.user_id:
            raise BusinessError("未获取到钉钉用户身份")
        dingtalk_user = self.__dingtalk_user_repository.get_dingtalk_user_by_remote_user_id(
            remote_user_id=oauth_result.user_id, dingtalk_corp_id=dingtalk_corp_id
        )
        dingtalk_parent = (
            self.__dingtalk_k12_parent_repository.get_dingtalk_k12_parent_by_remote_user_id(
                remote_user_id=oauth_result.user_id, dingtalk_corp_id=dingtalk_corp_id
            )
        )

        if not dingtalk_user and not dingtalk_parent:
            raise BusinessError("未获取到用户信息")
        user_profile = DingtalkUserVm(
            dingtalk_user_id=dingtalk_user.id if dingtalk_user else None,
            dingtalk_k12_parent_id=dingtalk_parent.id if dingtalk_parent else None,
            dingtalk_corp_id=dingtalk_corp_id,
            remote_user_id=oauth_result.user_id,
            user_category=EnumDingtalkUserCategory.DINGTALK_USER.name,
        )
        capacity_list = []
        if dingtalk_user:
            user_profile.user_category = EnumDingtalkUserCategory.DINGTALK_USER.name
            capacity_list = self.__capacity_repository.get_k12_capacity_list_by_dingtalk_user_id(
                dingtalk_user_id=dingtalk_user.id
            )
        if dingtalk_parent:
            capacity_list.append(
                CapacityVm(name=EnumCapacityCode.PARENT.value, code=EnumCapacityCode.PARENT.name)
            )
        if not capacity_list:
            raise BusinessError("未获取到职责信息")
        user_profile.capacity_code = capacity_list[0].code
        if not dingtalk_user:
            user_profile.user_category = EnumDingtalkUserCategory.DINGTALK_K12_PARENT.name
            user_profile.capacity_code = EnumCapacityCode.PARENT.name
        jwt_identity = (
            RedisConst.DD_USER
            + SymbolConst.COLON
            + oauth_result.user_id
            + SymbolConst.COLON
            + generate_random_string(12)
        )
        self.__redis_service.set_redis_dingtalk_user_profile(
            user_profile=user_profile, jwt_identity=jwt_identity
        )
        return self.build_token_data(jwt_identity=jwt_identity)

    def get_dingtalk_oauth_redirect_url(self, redirect_uri: str):
        """
        获取重定向的地址
        """
        dingtalk_corp_id = self.get_current_dingtalk_corp_id()
        return self.__dingtalk_auth_service.get_oauth_redirect(
            dingtalk_corp_id=dingtalk_corp_id, redirect_uri=redirect_uri
        )
