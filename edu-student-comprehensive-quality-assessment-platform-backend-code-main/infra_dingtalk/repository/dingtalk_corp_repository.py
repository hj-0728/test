from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_dingtalk.entity.dingtalk_corp import DingtalkCorpEntity
from infra_dingtalk.model.dingtalk_corp_model import DingtalkCorpModel


class DingtalkCorpRepository(BasicRepository):
    """
    钉钉组织 数据库访问
    """

    def insert_dingtalk_corp(self, corp: DingtalkCorpModel, transaction: Transaction) -> str:
        """
        插入钉钉组织
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DingtalkCorpEntity, entity_model=corp, transaction=transaction
        )

    def get_dingtalk_corp(self) -> List[DingtalkCorpModel]:
        """
        获取钉钉组织
        """

        sql = """select * from st_dingtalk_corp"""
        return self._fetch_all_to_model(model_cls=DingtalkCorpModel, sql=sql)
