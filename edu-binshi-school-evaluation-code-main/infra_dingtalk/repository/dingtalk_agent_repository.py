"""
钉钉应用 数据库访问
"""
from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_dingtalk.entity.dingtalk_agent import DingtalkAgentEntity
from infra_dingtalk.model.dingtalk_agent_model import DingtalkAgentModel


class DingtalkAgentRepository(BasicRepository):
    """
    钉钉应用 数据库访问
    """

    def insert_dingtalk_agent(self, agent: DingtalkAgentModel, transaction: Transaction) -> str:
        """
        插入钉钉应用
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DingtalkAgentEntity, entity_model=agent, transaction=transaction
        )

    def fetch_dingtalk_agent(
        self, dingtalk_corp_id: str, code: str
    ) -> Optional[DingtalkAgentModel]:
        """
        获取钉钉的应用
        """
        sql = """select sda.*, sdc.remote_corp_id from st_dingtalk_agent sda
        inner join st_dingtalk_corp sdc on sda.dingtalk_corp_id = sdc.id
        where dingtalk_corp_id = :dingtalk_corp_id and code = :code"""
        return self._fetch_first_to_model(
            model_cls=DingtalkAgentModel,
            sql=sql,
            params={
                "dingtalk_corp_id": dingtalk_corp_id,
                "code": code,
            },
        )
