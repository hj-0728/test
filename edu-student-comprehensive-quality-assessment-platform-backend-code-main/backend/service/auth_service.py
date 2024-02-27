import hashlib
from typing import Dict, Union

import orjson
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.token_helper import generate_random_string

from backend.data.constant import AppRedisConst
from backend.data.enum import EnumUserCategory
from backend.data.settings import DevSetting
from backend.model.edit.user_login_data_em import UserLoginDataEditModel
from backend.model.view.token_vm import TokenViewModel
from backend.model.view.user_info_vm import UserInfoViewModel
from backend.model.view.user_profile_vm import UserProfileViewModel
from backend.repository.auth_repository import AuthRepository
from backend.service.app_ability_permission_service import AppAbilityPermissionService
from backend.service.app_role_service import AppRoleService
from backend.service.redis_service import RedisService
from context_sync.service.context_people_user_map_service import ContextPeopleUserMapService
from infra_backbone.data.constant import SymbolConst
from infra_backbone.service.user_service import UserService
from infra_backbone.utility.graphical_captcha_helper import GraphicalCaptchaHelper
from infra_dingtalk.service.dingtalk_auth_service import DingtalkAuthService


class AuthService:
    def __init__(
        self,
        auth_repository: AuthRepository,
        redis_service: RedisService,
        dingtalk_auth_service: DingtalkAuthService,
        context_people_user_map_service: ContextPeopleUserMapService,
        user_service: UserService,
        app_role_service: AppRoleService,
        app_ability_permission_service: AppAbilityPermissionService,
    ):
        self.__auth_repository = auth_repository
        self.__redis_service = redis_service
        self.__dingtalk_auth_service = dingtalk_auth_service
        self.__context_people_user_map_service = context_people_user_map_service
        self.__user_service = user_service
        self.__app_role_service = app_role_service
        self.__app_ability_permission_service = app_ability_permission_service

    def login(
        self, user_params: UserLoginDataEditModel, transaction: Transaction
    ) -> TokenViewModel:
        """
        登录
        :return:
        """
        user_info = self.__user_service.verify_user_name_and_password(
            name=user_params.name,
            password=user_params.password,
            transaction=transaction,
        )

        self.verify_login_image_code(
            image_src=user_params.validate_image_src,
            code=user_params.validate_code,
            to_upper=True,  # 忽略大小写
        )

        people_id = self.__user_service.get_people_id_by_user_id(user_id=user_info.id)

        user_profile = UserProfileViewModel(
            user_category=EnumUserCategory.USER.name,
            user_id=user_info.id,
            people_id=people_id,
        )

        return self.get_user_profile_token(user_profile=user_profile)

    def get_current_user_info(self, user_id: str) -> UserInfoViewModel:
        """
        获取当前用户信息
        :param user_id:
        :return:
        """

        role_list = self.__auth_repository.fetch_user_role_list(user_id=user_id)

        role = self.__app_role_service.set_redis_user_role(user_id=user_id)

        self.__app_ability_permission_service.set_redis_user_ability_permission(
            user_id=user_id,
            role_id=role.id,
        )

        user = self.__user_service.get_user(user_id=user_id)

        return UserInfoViewModel(
            id=user_id,
            name=user.name,
            role_list=role_list,
            current_role=role_list[0],
        )

    def get_dingtalk_oauth_jwt_token(self, code: str, desired_identity: str) -> TokenViewModel:
        """
        获取钉钉oauth token
        """
        oauth_result = self.__dingtalk_auth_service.get_dingtalk_oauth_result(
            code=code, desired_identity=desired_identity
        )
        user_id = oauth_result.get_user_id()
        people_id = self.__context_people_user_map_service.get_people_id_by_user_resource(
            res_id=user_id, res_category=oauth_result.user_category
        )
        user_profile = UserProfileViewModel(
            user_category=oauth_result.user_category,
            user_id=user_id,
            people_id=people_id,
        )
        return self.get_user_profile_token(user_profile=user_profile)

    def get_user_profile_token(self, user_profile: UserProfileViewModel) -> TokenViewModel:
        """
        获取外部用户信息token
        :param user_profile:
        :return:
        """
        jwt_identity = (
            f"{user_profile.user_category}{SymbolConst.COLON}{user_profile.user_id}"
            f"{SymbolConst.COLON}{generate_random_string(12)}"
        )
        self.__redis_service.set_redis_user_profile(
            user_profile=user_profile, jwt_identity=jwt_identity
        )
        return self.build_token_data(jwt_identity=jwt_identity)

    @staticmethod
    def build_token_data(jwt_identity: Union[Dict, str]) -> TokenViewModel:
        """
        生成token
        :param jwt_identity:
        :return:
        """
        access_token = create_access_token(identity=jwt_identity)
        refresh_token = create_refresh_token(identity=jwt_identity)
        return TokenViewModel(access_token=access_token, refresh_token=refresh_token)

    def get_current_people_id(self) -> str:
        """
        获取当前用户people_id
        :return:
        """
        user_profile = self.__redis_service.get_redis_user_profile()
        if not user_profile.people_id:
            raise BusinessError("未获取到用户people信息")
        return user_profile.people_id

    def get_dev_user_login_token(self) -> TokenViewModel:
        """
        开发环境用户登录
        :return:
        """
        dev: DevSetting = current_app.config.get("DEV_SETTING", None)
        if not dev or not dev.enabled:
            raise BusinessError("禁止开发虚假登录")
        if dev.user_category in [
            EnumUserCategory.DINGTALK_USER.name,
            EnumUserCategory.DINGTALK_K12_PARENT.name,
        ]:
            people_id = self.__context_people_user_map_service.get_people_id_by_user_resource(
                res_id=dev.user_id, res_category=dev.user_category
            )
        else:
            people_id = self.__user_service.get_people_id_by_user_id(user_id=dev.user_id)
        user_profile = UserProfileViewModel(
            user_category=dev.user_category,
            user_id=dev.user_id,
            people_id=people_id,
        )
        return self.get_user_profile_token(user_profile=user_profile)

    def create_verify_image_for_login(
        self,
    ) -> str:
        """
        :result: image_on_base64_str
        """

        image_src, answer = GraphicalCaptchaHelper().captcha()
        redis_key = (
            AppRedisConst.VERIFY_LOGIN_IMAGE
            + SymbolConst.COLON
            + hashlib.md5(image_src.strip().encode()).hexdigest()
        )
        self.__redis_service.set(
            key=redis_key,
            value=orjson.dumps(answer),
            ex=AppRedisConst.IMAGE_VERIFICATION_CODE_VALIDITY_PERIOD,
        )
        return image_src

    def verify_login_image_code(self, image_src, code, to_upper=False) -> bool:
        """
        根据验证码图片从redis中获取答案
        :param image_src:
        :param code:
        :param to_upper:
        :return:
        """
        if not image_src:
            raise BusinessError("未获取到图片验证码信息")
        if not code:
            raise BusinessError("图片验证码不得为空")
        if to_upper:
            code = code.upper()
        redis_key = (
            AppRedisConst.VERIFY_LOGIN_IMAGE
            + SymbolConst.COLON
            + hashlib.md5(image_src.strip().encode()).hexdigest()
        )
        redis_code = self.__redis_service.get(redis_key)
        if redis_code is None:
            raise BusinessError("图片验证码已失效，请刷新图片。")
        if redis_code != code:
            raise BusinessError("图片验证码错误。")
        self.__redis_service.delete(redis_key)
        return True
