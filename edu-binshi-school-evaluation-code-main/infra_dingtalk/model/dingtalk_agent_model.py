import os
from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel

from infra_dingtalk.data.agent_plugin.setup_options import AgentPluginSetupOptions


class EnumDingtalkAgent(Enum):
    """
    应用
    """

    SYNC = "同步"
    K12_SYNC = "K12同步"
    AUTH = "身份验证"
    MESSAGE_DELIVERY = "消息提醒"


class DingtalkAgentModel(VersionedModel):
    """
    钉钉应用
    """

    dingtalk_corp_id: str
    remote_agent_id: Optional[str]
    code: str
    app_key: str
    app_secret: str

    remote_corp_id: Optional[str]

    def to_agent_plugin_setup_options(self) -> AgentPluginSetupOptions:
        redis_url = os.environ.get("redis_url")
        return AgentPluginSetupOptions(
            corp_id=self.remote_corp_id,
            app_key=self.app_key,
            app_secret=self.app_secret,
            agent_id=self.remote_agent_id,
            redis_url=redis_url,
        )
