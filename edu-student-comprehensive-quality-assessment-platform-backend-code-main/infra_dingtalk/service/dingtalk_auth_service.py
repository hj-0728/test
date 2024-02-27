"""
身份验证
"""
from infra_basic.errors import BusinessError
from loguru import logger

from infra_dingtalk.data.agent_plugin.dingtalk_user_info import DingtalkUserInfo
from infra_dingtalk.model.view.oauth_result_vm import EnumOauthUserCategory, OauthResultViewModel
from infra_dingtalk.repository.dingtalk_k12_parent_repository import DingtalkK12ParentRepository
from infra_dingtalk.repository.dingtalk_user_repository import DingtalkUserRepository
from infra_dingtalk.service.dingtalk_corp_service import DingtalkCorpService
from infra_dingtalk.service.plugin_service import PluginService


class DingtalkAuthService:
    def __init__(
        self,
        plugin_service: PluginService,
        dingtalk_corp_service: DingtalkCorpService,
        dingtalk_user_repository: DingtalkUserRepository,
        dingtalk_k12_parent_repository: DingtalkK12ParentRepository,
    ):
        self.__plugin_service = plugin_service
        self.__dingtalk_corp_service = dingtalk_corp_service
        self.__dingtalk_user_repository = dingtalk_user_repository
        self.__dingtalk_k12_parent_repository = dingtalk_k12_parent_repository

    def oauth_get_remote_user_info(self, dingtalk_corp_id: str, code: str) -> DingtalkUserInfo:
        """
        获得远程用户信息
        @param dingtalk_corp_id:
        @param code:
        @return:
        """
        client = self.__plugin_service.get_auth_plugin_instance_in_app(
            dingtalk_corp_id=dingtalk_corp_id
        )
        try:
            dingtalk_user_info = client.get_user_info(code=code)
        except Exception as e:
            logger.error(f"获取钉钉用户信息失败：{e}")
            raise BusinessError("获取钉钉用户信息失败")
        return dingtalk_user_info

    def get_oauth_redirect(self, dingtalk_corp_id: str, redirect_uri: str) -> str:
        """
        获得腾讯认证后跳转的url
        @param dingtalk_corp_id:
        @param redirect_uri:
        @return:
        """
        client = self.__plugin_service.get_auth_plugin_instance_in_app(
            dingtalk_corp_id=dingtalk_corp_id
        )
        return client.get_authorize_url(redirect_uri=redirect_uri)

    def get_dingtalk_oauth_result(self, code: str, desired_identity: str) -> OauthResultViewModel:
        """
        获取钉钉用户信息
        :param code:
        :param desired_identity:
        :return:
        """
        if desired_identity not in EnumOauthUserCategory.__members__:
            raise BusinessError("身份类型错误")
        dingtalk_corp_id = self.__dingtalk_corp_service.get_current_dingtalk_corp_id()
        remote_user = self.oauth_get_remote_user_info(
            dingtalk_corp_id=dingtalk_corp_id,
            code=code,
        )
        logger.info(f"钉钉身份验证结果：{remote_user}")
        if not remote_user.user_id:
            raise BusinessError("未获取到钉钉用户身份")
        oauth_result = OauthResultViewModel(
            remote_user_id=remote_user.user_id,
            dingtalk_corp_id=dingtalk_corp_id,
            user_category=desired_identity,
        )
        if desired_identity == EnumOauthUserCategory.DINGTALK_USER.name:
            dingtalk_user = self.__dingtalk_user_repository.get_dingtalk_user_by_remote_user_id(
                remote_user_id=remote_user.user_id, dingtalk_corp_id=dingtalk_corp_id
            )
            if not dingtalk_user:
                raise BusinessError("未获取到教职工身份信息")
            oauth_result.dingtalk_user_id = dingtalk_user.id
            return oauth_result

        dingtalk_parent = (
            self.__dingtalk_k12_parent_repository.get_dingtalk_k12_parent_by_remote_user_id(
                remote_user_id=remote_user.user_id, dingtalk_corp_id=dingtalk_corp_id
            )
        )
        if not dingtalk_parent:
            raise BusinessError("未获取到用户信息")
        oauth_result.dingtalk_k12_parent_id = dingtalk_parent.id
        return oauth_result
