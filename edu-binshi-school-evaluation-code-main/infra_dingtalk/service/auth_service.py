"""
身份验证
"""
from infra_basic.errors import BusinessError

from infra_dingtalk.service.plugin_service import PluginService


class AuthService:
    def __init__(self, plugin_service: PluginService):
        self._plugin_service = plugin_service

    def oauth_get_remote_user_info(self, dingtalk_corp_id: str, code: str):
        """
        获得远程用户信息
        @param dingtalk_corp_id:
        @param code:
        @return:
        """
        client = self._plugin_service.get_auth_plugin_instance_in_app(
            dingtalk_corp_id=dingtalk_corp_id
        )
        dingtalk_user_info = client.get_user_info(code=code)
        if dingtalk_user_info.err_code != 0:
            raise BusinessError("未获取到钉钉用户信息")
        return dingtalk_user_info

    def get_oauth_redirect(self, dingtalk_corp_id: str, redirect_uri: str) -> str:
        """
        获得腾讯认证后跳转的url
        @param dingtalk_corp_id:
        @param redirect_uri:
        @return:
        """
        client = self._plugin_service.get_auth_plugin_instance_in_app(
            dingtalk_corp_id=dingtalk_corp_id
        )
        return client.get_authorize_url(redirect_uri=redirect_uri)
