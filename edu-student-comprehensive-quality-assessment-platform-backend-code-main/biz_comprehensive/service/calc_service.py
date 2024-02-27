from typing import List, Optional

from infra_basic.basic_resource import BasicResource
from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction

from biz_comprehensive.model.calc_rule_model import EnumBelongsToResCategory
from biz_comprehensive.model.calc_trigger_model import (
    CalcTriggerModel,
    EnumCalcTriggerInputResCategory,
)
from biz_comprehensive.model.edit.calc_em import (
    CalcResourceEditModel,
    SaveCalcAssignEditModel,
    SaveCalcRuleAssignEditModel,
)
from biz_comprehensive.model.observation_point_model import EnumObservationPointCategory
from biz_comprehensive.model.symbol_model import EnumSymbolCode
from biz_comprehensive.repository.symbol_repository import SymbolRepository
from biz_comprehensive.service.calc_rule_service import CalcRuleService
from biz_comprehensive.service.calc_trigger_service import CalcTriggerService
from biz_comprehensive.service.save_calc_result_service import SaveCalcResultService


class CalcService:
    def __init__(
        self,
        calc_trigger_service: CalcTriggerService,
        calc_rule_service: CalcRuleService,
        symbol_repository: SymbolRepository,
        save_calc_result_service: SaveCalcResultService,
    ):
        self.__calc_trigger_service = calc_trigger_service
        self.__calc_rule_service = calc_rule_service
        self.__symbol_repository = symbol_repository
        self.__save_calc_result_service = save_calc_result_service

    def save_assign_calc(self, calc_info: SaveCalcAssignEditModel, transaction: Transaction):
        """
        保存 assign 类型计算
        :param calc_info:
        :param transaction:
        :return:
        """

        calc_rule_id = self.__calc_rule_service.save_assign_calc_rule(
            calc_rule=calc_info.cast_to(SaveCalcRuleAssignEditModel), transaction=transaction
        )

        self.__calc_trigger_service.save_calc_trigger(
            calc_trigger=calc_info.cast_to(CalcTriggerModel, calc_rule_id=calc_rule_id),
            transaction=transaction,
        )

    def save_bright_spot_calc(
        self, input_res_category: str, input_res_id: str, transaction: Transaction
    ):
        """
        保存闪光点计算
        :param input_res_category:
        :param input_res_id:
        :param transaction:
        :return:
        """

        # 获取闪光点的规则
        calc_rule = self.__calc_rule_service.get_symbol_calc_rule_by_symbol_code(
            symbol_code=EnumSymbolCode.BRIGHT_SPOT.name
        )
        if not calc_rule:
            # 获取积分符号
            symbol = self.__symbol_repository.fetch_symbol_by_code(
                code=EnumSymbolCode.BRIGHT_SPOT.name
            )
            calc_rule_id = self.__calc_rule_service.save_assign_calc_rule(
                calc_rule=SaveCalcRuleAssignEditModel(
                    belongs_to_res_id=symbol.id,
                    belongs_to_res_category=EnumBelongsToResCategory.SYMBOL.name,
                ),
                transaction=transaction,
            )
        else:
            calc_rule_id = calc_rule.id
        self.__calc_trigger_service.save_calc_trigger(
            calc_trigger=CalcTriggerModel(
                calc_rule_id=calc_rule_id,
                input_res_category=input_res_category,
                input_res_id=input_res_id,
            ),
            transaction=transaction,
        )

    def save_observation_point_calc_points(
        self,
        observation_point_id: str,
        observation_point_category: str,
        point_score: int,
        transaction: Transaction,
    ):
        """
        保存观测点计算积分
        :param observation_point_id:
        :param observation_point_category:
        :param point_score:
        :param transaction:
        :return:
        """

        # 获取积分符号
        symbol = self.__symbol_repository.fetch_symbol_by_code(code=EnumSymbolCode.POINTS.name)

        self.__calc_trigger_service.delete_calc_trigger_and_calc_by_input_res(
            input_res_category=EnumCalcTriggerInputResCategory.OBSERVATION_POINT.name,
            input_res_id=observation_point_id,
            transaction=transaction,
            rule_belongs_to_res_id=symbol.id,
            rule_belongs_to_res_category=EnumBelongsToResCategory.SYMBOL.name,
        )

        calc_rule_info = SaveCalcAssignEditModel(
            belongs_to_res_category=EnumBelongsToResCategory.SYMBOL.name,
            belongs_to_res_id=symbol.id,
            input_res_category=EnumCalcTriggerInputResCategory.OBSERVATION_POINT.name,
            input_res_id=observation_point_id,
            score=point_score,
        )

        self.save_assign_calc(calc_info=calc_rule_info, transaction=transaction)

        if observation_point_category == EnumObservationPointCategory.COMMEND.name:
            self.save_bright_spot_calc(
                input_res_category=EnumCalcTriggerInputResCategory.OBSERVATION_POINT.name,
                input_res_id=observation_point_id,
                transaction=transaction,
            )

    def calc_and_save_all_result(
        self, resource_data: CalcResourceEditModel, transaction: Transaction
    ) -> List[BasicResource]:
        """
        计算并保存所有结果
        :param resource_data:
        :param transaction:
        :return:
        """

        calc_trigger_list = self.__calc_trigger_service.fetch_calc_trigger_by_input(
            input_res_category=resource_data.input_res_category,
            input_res_id=resource_data.input_res_id,
        )

        log_result_list = []

        for calc_trigger in calc_trigger_list:
            log_result = self.calc_and_save_result_by_calc_rule(
                calc_rule_id=calc_trigger.calc_rule_id,
                resource_data=resource_data,
                transaction=transaction,
            )
            if log_result:
                log_result_list.extend(log_result)

        return log_result_list

    def calc_and_save_result_by_calc_rule(
        self, calc_rule_id: str, resource_data: CalcResourceEditModel, transaction: Transaction
    ) -> Optional[List[BasicResource]]:
        """
        计算并保存结果根据计算规则
        :param calc_rule_id:
        :param resource_data:
        :param transaction:
        :return:
        """

        calc_rule = self.__calc_rule_service.get_calc_rule_by_id(calc_rule_id=calc_rule_id)
        if not calc_rule:
            raise BusinessError("计算规则不存在")

        calc_log_result = self.__calc_rule_service.calc_rule_calc_object_result(
            calc_rule=calc_rule,
            resource_data=resource_data,
        )

        if calc_log_result.calc_result:
            return self.__save_calc_result_service.save_calc_result(
                calc_rule=calc_rule,
                calc_log_result=calc_log_result,
                resource_data=resource_data,
                transaction=transaction,
            )
