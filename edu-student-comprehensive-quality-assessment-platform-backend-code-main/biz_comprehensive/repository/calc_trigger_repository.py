from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.calc_trigger import CalcTriggerEntity
from biz_comprehensive.model.calc_trigger_model import CalcTriggerModel
from biz_comprehensive.model.view.calc_trigger_vm import CalcTriggerViewModel


class CalcTriggerRepository(BasicRepository):
    def insert_calc_trigger(self, data: CalcTriggerModel, transaction: Transaction) -> str:
        """
        插入计算触发器
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=CalcTriggerEntity, entity_model=data, transaction=transaction
        )

    def delete_calc_trigger(self, calc_trigger_id: str, transaction: Transaction):
        """
        删除计算触发器
        :param calc_trigger_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=CalcTriggerEntity, entity_id=calc_trigger_id, transaction=transaction
        )

    def fetch_need_delete_calc_trigger_and_rule_list_by_input_res(
        self,
        input_res_category: str,
        input_res_id: str,
        rule_belongs_to_res_id: Optional[str],
        rule_belongs_to_res_category: Optional[str],
    ) -> List[CalcTriggerViewModel]:
        """
        获取计算触发器列表
        :param input_res_category:
        :param input_res_id:
        :param rule_belongs_to_res_id:
        :param rule_belongs_to_res_category:
        :return:
        """

        sql = """
        with calc_trigger as (
        select ct.* from st_calc_trigger ct 
        INNER JOIN st_calc_rule cr on ct.calc_rule_id=cr.id 
        where input_res_category =:input_res_category and input_res_id =:input_res_id
        """
        if rule_belongs_to_res_id and rule_belongs_to_res_category:
            sql += """
            and cr.belongs_to_res_id =:rule_belongs_to_res_id 
            and cr.belongs_to_res_category =:rule_belongs_to_res_category
            """
        sql += """)
        , calc_rule as (
        select DISTINCT ct.calc_rule_id from calc_trigger ct 
        INNER JOIN st_calc_trigger sct on ct.calc_rule_id=sct.calc_rule_id and ct.input_res_id!=sct.input_res_id
        )
        select ct.*,case when cr.calc_rule_id is null then true else false end as rule_can_be_deleted
        from calc_trigger ct left join calc_rule cr on ct.calc_rule_id=cr.calc_rule_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=CalcTriggerViewModel,
            params={
                "input_res_category": input_res_category,
                "input_res_id": input_res_id,
                "rule_belongs_to_res_id": rule_belongs_to_res_id,
                "rule_belongs_to_res_category": rule_belongs_to_res_category,
            },
        )

    def fetch_calc_trigger(self, calc_trigger: CalcTriggerModel) -> Optional[CalcTriggerModel]:
        """
        获取是否存在相同的计算触发器
        :param calc_trigger:
        :return:
        """

        sql = """
        select * from st_calc_trigger 
        where input_res_category=:input_res_category and input_res_id=:input_res_id and calc_rule_id=:calc_rule_id
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=CalcTriggerModel,
            params={
                "input_res_category": calc_trigger.input_res_category,
                "input_res_id": calc_trigger.input_res_id,
                "calc_rule_id": calc_trigger.calc_rule_id,
            },
        )

    def fetch_calc_trigger_by_input(
        self, input_res_category: str, input_res_id: str
    ) -> List[CalcTriggerModel]:
        """
        获取计算触发器 通过 input res
        :param input_res_category:
        :param input_res_id:
        :return:
        """

        sql = """
        select * from st_calc_trigger 
        where input_res_category=:input_res_category and input_res_id=:input_res_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=CalcTriggerModel,
            params={
                "input_res_category": input_res_category,
                "input_res_id": input_res_id,
            },
        )
