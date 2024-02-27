"""
钉钉应用初始化参数
"""

from typing import Optional

from infra_basic.basic_model import BasePlusModel


class AgentPluginSetupOptions(BasePlusModel):
    """
    钉钉应用初始化参数
    """

    corp_id: str
    app_secret: str
    app_key: str
    agent_id: Optional[str]
    redis_url: Optional[str]
