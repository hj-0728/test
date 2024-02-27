from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.calc_rule_pre_depends import CalcRulePreDependsEntity
from biz_comprehensive.model.calc_rule_pre_depends_model import CalcRulePreDependsModel


class CalcRulePreDependsRepository(BasicRepository):
    def insert_calc_rule_pre_depends(
        self, data: CalcRulePreDependsModel, transaction: Transaction
    ) -> str:
        """
        插入计算规则前置依赖
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=CalcRulePreDependsEntity, entity_model=data, transaction=transaction
        )

    def delete_calc_trigger(self, calc_rule_pre_depends_id: str, transaction: Transaction):
        """
        删除计算规则前置依赖
        :param calc_rule_pre_depends_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=CalcRulePreDependsEntity,
            entity_id=calc_rule_pre_depends_id,
            transaction=transaction,
        )

    def fetch_calc_trigger_by_input(self, calc_rule_id: str) -> List[CalcRulePreDependsModel]:
        """
        获取计算规则前置依赖根据计算规则id
        :param calc_rule_id:
        :return:
        """

        sql = """
        select * from st_calc_rule_pre_depends 
        where calc_rule_id=:calc_rule_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=CalcRulePreDependsModel,
            params={
                "calc_rule_id": calc_rule_id,
            },
        )
