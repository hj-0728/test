from typing import List, Optional

from infra_basic.transaction import Transaction

from biz_comprehensive.model.calc_trigger_model import CalcTriggerModel
from biz_comprehensive.repository.calc_rule_repository import CalcRuleRepository
from biz_comprehensive.repository.calc_trigger_repository import CalcTriggerRepository


class CalcTriggerService:
    def __init__(
        self,
        calc_trigger_repository: CalcTriggerRepository,
        calc_rule_repository: CalcRuleRepository,
    ):
        self.__calc_trigger_repository = calc_trigger_repository
        self.__calc_rule_repository = calc_rule_repository

    def save_calc_trigger(self, calc_trigger: CalcTriggerModel, transaction: Transaction):
        """
        保存计算触发器
        :param calc_trigger:
        :param transaction:
        :return:
        """

        calc_trigger_db = self.__calc_trigger_repository.fetch_calc_trigger(
            calc_trigger=calc_trigger
        )

        if not calc_trigger_db:
            return self.__calc_trigger_repository.insert_calc_trigger(
                data=calc_trigger, transaction=transaction
            )

    def delete_calc_trigger_and_calc_by_input_res(
        self,
        input_res_category: str,
        input_res_id: str,
        transaction: Transaction,
        rule_belongs_to_res_id: Optional[str] = None,
        rule_belongs_to_res_category: Optional[str] = None,
    ):
        """
        删除计算触发器和规则
        :param input_res_category:
        :param input_res_id:
        :param rule_belongs_to_res_id: 指定需要删除类型
        :param rule_belongs_to_res_category:
        :param transaction:
        :return:
        """

        calc_trigger_list = self.__calc_trigger_repository.fetch_need_delete_calc_trigger_and_rule_list_by_input_res(
            input_res_category=input_res_category,
            input_res_id=input_res_id,
            rule_belongs_to_res_id=rule_belongs_to_res_id,
            rule_belongs_to_res_category=rule_belongs_to_res_category,
        )

        for calc_trigger in calc_trigger_list:
            self.__calc_trigger_repository.delete_calc_trigger(
                calc_trigger_id=calc_trigger.id, transaction=transaction
            )

            if calc_trigger.rule_can_be_deleted:
                self.__calc_rule_repository.delete_calc_rule(
                    calc_rule_id=calc_trigger.calc_rule_id, transaction=transaction
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

        return self.__calc_trigger_repository.fetch_calc_trigger_by_input(
            input_res_category=input_res_category,
            input_res_id=input_res_id,
        )
