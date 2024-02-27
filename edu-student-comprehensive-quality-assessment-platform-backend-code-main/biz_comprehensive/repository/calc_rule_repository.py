from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.calc_rule import CalcRuleEntity
from biz_comprehensive.model.calc_rule_model import CalcRuleModel, EnumBelongsToResCategory


class CalcRuleRepository(BasicRepository):
    def insert_calc_rule(self, data: CalcRuleModel, transaction: Transaction) -> str:
        """
        插入计算规则
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=CalcRuleEntity, entity_model=data, transaction=transaction
        )

    def delete_calc_rule(self, calc_rule_id: str, transaction: Transaction):
        """
        删除计算规则
        :param calc_rule_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=CalcRuleEntity, entity_id=calc_rule_id, transaction=transaction
        )

    def get_symbol_calc_rule_by_symbol_code(self, symbol_code: str) -> Optional[CalcRuleModel]:
        """
        获取符号计算规则根据符号code
        :param symbol_code:
        :return:
        """

        sql = """
        select cr.* from st_calc_rule cr 
        inner join st_symbol ss on cr.belongs_to_res_id=ss.id and cr.belongs_to_res_category=:belongs_to_res_category
        where ss.code=:symbol_code
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=CalcRuleModel,
            params={
                "symbol_code": symbol_code,
                "belongs_to_res_category": EnumBelongsToResCategory.SYMBOL.name,
            },
        )

    def fetch_calc_rule_by_id(self, calc_rule_id: str) -> Optional[CalcRuleModel]:
        """

        :param calc_rule_id:
        :return:
        """

        sql = """
        select * from st_calc_rule where id=:calc_rule_id
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=CalcRuleModel,
            params={
                "calc_rule_id": calc_rule_id,
            },
        )
