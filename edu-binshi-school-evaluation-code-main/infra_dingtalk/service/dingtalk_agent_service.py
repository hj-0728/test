"""
企业微信应用服务
"""
from infra_basic.errors.input import DataNotFoundError

from infra_dingtalk.model.dingtalk_agent_model import DingtalkAgentModel
from infra_dingtalk.repository.dingtalk_agent_repository import DingtalkAgentRepository


class DingtalkAgentService:
    def __init__(self, dingtalk_agent_repository: DingtalkAgentRepository):
        self._dingtalk_agent_repository = dingtalk_agent_repository

    def get_dingtalk_agent(self, dingtalk_corp_id: str, code: str) -> DingtalkAgentModel:
        """
        企业微信应用
        """
        agent = self._dingtalk_agent_repository.fetch_dingtalk_agent(
            dingtalk_corp_id=dingtalk_corp_id, code=code
        )
        if not agent:
            raise DataNotFoundError(f"{dingtalk_corp_id}的同步应用")
        return agent
