"""
插件的服务
"""
import os

from infra_basic.redis_manager import RedisManager

from infra_dingtalk.agent_plugin.auth_plugin import AuthAgentPlugin
from infra_dingtalk.agent_plugin.k12_sync_plugin import K12SyncAgentPlugin
from infra_dingtalk.agent_plugin.sync_plugin import SyncAgentPlugin
from infra_dingtalk.model.dingtalk_agent_model import EnumDingtalkAgent
from infra_dingtalk.service.dingtalk_agent_service import DingtalkAgentService


class PluginService:
    def __init__(
        self,
        dingtalk_agent_service: DingtalkAgentService,
        redis_manager: RedisManager,
    ):
        self._dingtalk_agent_service = dingtalk_agent_service
        self._redis_manager = redis_manager

    def get_sync_plugin_instance_in_app(self, dingtalk_corp_id: str) -> SyncAgentPlugin:
        """
        获取 flask app 中的同步插件实例
        """
        agent = self._dingtalk_agent_service.get_dingtalk_agent(
            dingtalk_corp_id=dingtalk_corp_id, code=EnumDingtalkAgent.SYNC.name
        )
        plugin = SyncAgentPlugin(setup_options=agent.to_agent_plugin_setup_options())
        return plugin

    def get_auth_plugin_instance_in_app(
        self,
        dingtalk_corp_id: str,
    ) -> AuthAgentPlugin:
        """
        获取 flask app 中的身份验证插件实例
        """
        agent_code = os.environ.get("dingtalk_auth_agent_code")
        if not agent_code:
            agent_code = EnumDingtalkAgent.AUTH.name
        agent = self._dingtalk_agent_service.get_dingtalk_agent(
            dingtalk_corp_id=dingtalk_corp_id, code=agent_code
        )
        plugin = AuthAgentPlugin(setup_options=agent.to_agent_plugin_setup_options())
        return plugin

    def get_message_delivery_plugin_instance_in_app(
        self,
        dingtalk_corp_id: str,
    ) -> AuthAgentPlugin:
        """
        获取 flask app 中的消息发送插件实例
        """
        agent = self._dingtalk_agent_service.get_dingtalk_agent(
            dingtalk_corp_id=dingtalk_corp_id, code=EnumDingtalkAgent.MESSAGE_DELIVERY.name
        )
        plugin = AuthAgentPlugin(setup_options=agent.to_agent_plugin_setup_options())
        return plugin

    def get_k12_sync_plugin_instance_in_app(
        self,
        dingtalk_corp_id: str,
    ) -> K12SyncAgentPlugin:
        """
        获取 flask app 中的同步插件实例
        """
        agent = self._dingtalk_agent_service.get_dingtalk_agent(
            dingtalk_corp_id=dingtalk_corp_id, code=EnumDingtalkAgent.K12_SYNC.name
        )
        plugin = K12SyncAgentPlugin(setup_options=agent.to_agent_plugin_setup_options())
        return plugin
