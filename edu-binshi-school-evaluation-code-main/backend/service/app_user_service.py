import hashlib
from typing import Dict

import orjson
from flask import current_app
from flask_jwt_extended import get_jwt, get_jwt_identity
from infra_basic.errors import BusinessError
from infra_basic.errors.input import DataNotFoundError
from infra_basic.errors.permission import NeedLoginError
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.redis_manager import RedisManager
from infra_basic.transaction import Transaction
from infra_utility.serialize_helper import ORJSONPickle
from infra_utility.token_helper import generate_random_string
from loguru import logger

from backend.data.constant import FlaskConfigConst, RedisConst
from backend.model.edit.user_login_data_em import UserLoginDataEditModel
from backend.model.edit.user_reset_password_em import UserResetPasswordEditModel, \
    EnumUserType
from backend.service.authorization_service import AuthorizationService
from backend.service.redis_service import RedisService
from edu_binshi.service.student_service import StudentService
from infra_backbone.data.constant import SymbolConst
from infra_backbone.model.edit.user_password_em import UserPasswordEditModel
from infra_backbone.model.params.user_params import UserQueryParams
from infra_backbone.model.role_model import EnumRoleCode
from infra_backbone.model.user_model import UserModel
from infra_backbone.model.view.user_profile_vm import UserProfileViewModel
from infra_backbone.repository.user_repository import UserRepository
from infra_backbone.service.role_service import RoleService
from infra_backbone.service.user_service import UserService as BackboneUserService
from infra_backbone.utility.graphical_captcha_helper import GraphicalCaptchaHelper


class AppUserService:
    def __init__(
        self,
        user_service: BackboneUserService,
        user_repository: UserRepository,
        role_service: RoleService,
        redis_service: RedisService,
        authorization_service: AuthorizationService,
        redis_manager: RedisManager,
        student_service: StudentService,
    ):
        self.__user_service = user_service
        self.__user_repository = user_repository
        self.__role_service = role_service
        self.__redis_service = redis_service
        self.__authorization_service = authorization_service
        self.__redis_client = redis_manager.redis_client
        self.__student_service = student_service

    def user_login(
        self,
        user_params: UserLoginDataEditModel,
        transaction: Transaction,
    ):
        """
        用户登录
        :param user_params:
        :param transaction:
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

        jwt_identity = (
            RedisConst.USER
            + SymbolConst.COLON
            + user_info.id
            + SymbolConst.COLON
            + generate_random_string(12)
        )
        self.add_redis_user_profile(
            user_id=user_info.id,
            jwt_identity=jwt_identity,
        )

        return self.__authorization_service.build_token_data(jwt_identity=jwt_identity)

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
            RedisConst.VERIFY_LOGIN_IMAGE
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
            raise DataNotFoundError("未获取到用户相关信息")
        self.__redis_service.set(
            key=redis_key, value=ORJSONPickle.encode_model(user_profile), ex=86400
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
            raise DataNotFoundError("未获取到用户相关功能权限信息")
        ability_permission_id_list = list(
            set(map(lambda x: x.ability_permission_id, user_ability_per_list))
        )
        self.__redis_service.set(
            key=redis_key, value=orjson.dumps(ability_permission_id_list), ex=86400
        )

    def create_verify_image_for_login(
        self,
    ) -> str:
        """
        :result: image_on_base64_str
        """

        image_src, answer = GraphicalCaptchaHelper().captcha()
        redis_key = (
            RedisConst.VERIFY_LOGIN_IMAGE
            + SymbolConst.COLON
            + hashlib.md5(image_src.strip().encode()).hexdigest()
        )
        self.__redis_service.set(
            key=redis_key,
            value=orjson.dumps(answer),
            ex=FlaskConfigConst.IMAGE_VERIFICATION_CODE_VALIDITY_PERIOD,
        )
        return image_src

    def refresh_user_expire_login_data(self, jwt_identity: str) -> Dict:
        """
        刷新登录信息
        :param jwt_identity:
        :return:
        """
        user_id = jwt_identity.split(SymbolConst.COLON)[0]
        self.add_redis_user_profile(
            user_id=user_id,
            jwt_identity=jwt_identity,
        )
        return self.__authorization_service.build_token_data(jwt_identity=jwt_identity)

    def check_user_profile_by_redis(self):
        redis_key = RedisConst.SESSION + SymbolConst.COLON + get_jwt_identity()
        is_existed = self.__redis_service.exists(redis_key)
        if not is_existed:
            raise NeedLoginError("需要登录")

    @staticmethod
    def set_black_list():
        """
        设置过期Token黑名单
        :return:
        """
        jwt_redis_blocklist = current_app.config["JWT_REDIS_BLOCKLIST"]
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])

    def change_user_password(
        self,
        user_password: UserPasswordEditModel,
        user_id: str,
        transaction: Transaction,
    ):
        """
        修改用户密码
        :param user_password:
        :param user_id:
        :param transaction:
        :return:
        """
        flag = self.__user_service.change_user_password(
            user_password=user_password, user_id=user_id, transaction=transaction
        )
        if flag:
            self.__redis_service.clear_redis_user_profile_by_user_id(
                user_category=RedisConst.USER, user_id=user_id
            )

    def update_user_activated(
        self,
        user: UserModel,
        transaction: Transaction,
    ):
        """
        启用、禁用用户
        :param user:
        :param transaction:
        :return:
        """
        self.__user_service.update_user_activated(user=user, transaction=transaction)
        if not user.is_activated:
            self.__redis_service.clear_redis_user_profile_by_user_id(
                user_category=RedisConst.USER, user_id=user.id
            )

    def reset_password(
        self,
        data: UserResetPasswordEditModel,
        transaction: Transaction,
    ):
        """
        重置用户密码
        :param data:
        :param transaction:
        :return:
        """
        new_password = None
        if data.user_type == EnumUserType.STUDENT.name:
            new_password = self.__student_service.get_student_init_password()
        new_password = self.__user_service.reset_password(
            data=data,
            transaction=transaction,
            new_password=new_password
        )
        if new_password:
            self.__redis_service.clear_redis_user_profile_by_user_id(
                user_category=RedisConst.USER, user_id=data.id
            )
        return new_password

    def edit_user(self, data: UserModel, transaction: Transaction):
        """
        更新用户
        :param data:
        :param transaction:
        :return:
        """
        self.__user_service.edit_user(data=data, transaction=transaction)
        self.__redis_service.clear_redis_user_profile_by_user_id(
            user_category=RedisConst.USER, user_id=data.id
        )

    def get_current_user_id(self, current_category: str):
        user_id = get_jwt_identity().split(SymbolConst.COLON)[1]
        if current_category == RedisConst.DD_USER:
            redis_key = RedisConst.SESSION + SymbolConst.COLON + get_jwt_identity()
            user_profile = ORJSONPickle.decode_model(
                data_content=self.__redis_client.get(name=redis_key),
                data_type=UserProfileViewModel,
            )
            user_id = user_profile.user_id
        if not user_id:
            raise DataNotFoundError("未获取到当前用户身份")
        return user_id

    def get_teacher_list(self, params: UserQueryParams) -> PaginationCarrier[UserModel]:
        """
        获取用户列表
        """
        if params.current_user_role_code == EnumRoleCode.SYSTEM_ADMIN.name:
            params.filter_out_role_code = [EnumRoleCode.STUDENT.name]
        else:
            params.filter_out_role_code = [
                EnumRoleCode.STUDENT.name,
                EnumRoleCode.SYSTEM_ADMIN.name,
            ]
        return self.__user_repository.get_user_list(
            params=params,
        )

    def disable_unavailable_user(self, transaction: Transaction):
        """
        禁用不可的用户
        """
        user_list = self.__user_repository.fetch_need_disable_user()
        for user in user_list:
            user.is_activated = False
            self.__user_repository.update_user(
                data=user,
                transaction=transaction,
                limited_col_list=["is_activated"],
            )
