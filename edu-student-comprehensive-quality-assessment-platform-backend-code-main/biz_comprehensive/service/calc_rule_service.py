from datetime import datetime
from typing import Optional

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction

from biz_comprehensive.model.calc_log_model import CalcLogModel
from biz_comprehensive.model.calc_rule_model import CalcRuleModel, EnumCalcFunc, EnumPreCalcFunc
from biz_comprehensive.model.edit.calc_em import CalcResourceEditModel, SaveCalcRuleAssignEditModel
from biz_comprehensive.repository.calc_rule_repository import CalcRuleRepository
from biz_comprehensive.service.calc_rule_calc_func_service import CalcRuleCalcFuncService
from biz_comprehensive.service.calc_rule_post_func_service import CalcRulePostFuncService
from biz_comprehensive.service.calc_rule_pre_func_service import CalcRulePreFuncService


class CalcRuleService:
    def __init__(
        self,
        calc_rule_repository: CalcRuleRepository,
        calc_rule_pre_func_service: CalcRulePreFuncService,
        calc_rule_calc_func_service: CalcRuleCalcFuncService,
        calc_rule_post_func_service: CalcRulePostFuncService,
    ):
        self.__calc_rule_repository = calc_rule_repository
        self.__calc_rule_pre_func_service = calc_rule_pre_func_service
        self.__calc_rule_calc_func_service = calc_rule_calc_func_service
        self.__calc_rule_post_func_service = calc_rule_post_func_service

    def save_assign_calc_rule(
        self, calc_rule: SaveCalcRuleAssignEditModel, transaction: Transaction
    ) -> str:
        """
        保存 assign 类型计算规则
        :param calc_rule:
        :param transaction:
        :return:
        """

        if not calc_rule:
            raise BusinessError("calc_rule 不能为空")

        calc_rule_info = calc_rule.cast_to(CalcRuleModel)
        calc_rule_info.pre_func = EnumPreCalcFunc.HANDLE_CALC_RES.value
        calc_rule_info.calc_func = EnumCalcFunc.ASSIGN.value
        calc_rule_info.calc_func_params = {"score": calc_rule.score}
        return self.__calc_rule_repository.insert_calc_rule(
            data=calc_rule_info, transaction=transaction
        )

    def get_symbol_calc_rule_by_symbol_code(self, symbol_code: str) -> Optional[CalcRuleModel]:
        """
        获取符号计算规则根据符号code
        :param symbol_code:
        :return:
        """

        return self.__calc_rule_repository.get_symbol_calc_rule_by_symbol_code(
            symbol_code=symbol_code
        )

    def get_calc_rule_by_id(self, calc_rule_id: str) -> Optional[CalcRuleModel]:
        """
        获取计算规则根据id
        :param calc_rule_id:
        :return:
        """

        return self.__calc_rule_repository.fetch_calc_rule_by_id(calc_rule_id=calc_rule_id)

    def calc_rule_calc_object_result(
        self, calc_rule: CalcRuleModel, resource_data: CalcResourceEditModel
    ) -> CalcLogModel:
        """
        计算对象分数
        :param calc_rule:
        :param resource_data:
        :return:
        """

        pre_result = self.__calc_rule_pre_func_service.execute_calc_rule_pre_func(
            calc_rule=calc_rule, resource_data=resource_data
        )

        calc_result = self.__calc_rule_calc_func_service.execute_calc_rule_calc_func(
            calc_rule=calc_rule,
            pre_result=pre_result.calc_result,
        )

        post_result = self.__calc_rule_post_func_service.execute_calc_rule_post_func(
            calc_rule=calc_rule,
            resource_data=resource_data,
        )

        return CalcLogModel(
            calc_rule_id=calc_rule.id,
            calc_on=datetime.now(),
            pre_func=pre_result.func,
            pre_func_args=pre_result.func_args,
            calc_func=calc_result.func,
            calc_func_args=calc_result.func_args,
            post_func=post_result.func,
            post_func_args=post_result.func_args,
            calc_result={
                "pre_result": pre_result.calc_result,
                "calc_result": calc_result.calc_result,
            },
        )
