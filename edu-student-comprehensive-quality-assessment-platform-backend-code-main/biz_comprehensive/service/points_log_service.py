from decimal import Decimal

from infra_basic.basic_resource import BasicResource
from infra_basic.transaction import Transaction

from biz_comprehensive.data.enum import EnumComprehensiveResource
from biz_comprehensive.model.calc_rule_model import CalcRuleModel
from biz_comprehensive.model.edit.calc_em import CalcResourceEditModel
from biz_comprehensive.model.points_log_model import EnumPointsLogStatus, PointsLogModel
from biz_comprehensive.repository.points_log_repository import PointsLogRepository
from biz_comprehensive.service.period_service import PeriodService


class PointsLogService:
    def __init__(self, points_log_repository: PointsLogRepository, period_service: PeriodService):
        self.__points_log_repository = points_log_repository
        self.__period_service = period_service

    def save_points_log(
        self,
        calc_rule: CalcRuleModel,
        calc_result: float,
        resource_data: CalcResourceEditModel,
        transaction: Transaction,
    ) -> BasicResource:
        """
        保存积分日志
        :param calc_rule:
        :param calc_result:
        :param resource_data:
        :param transaction:
        :return:
        """

        points_log = self.__points_log_repository.get_last_points_log_by_owner_res_and_symbol(
            owner_res_id=resource_data.owner_res_id,
            owner_res_category=resource_data.owner_res_category,
            symbol_id=calc_rule.belongs_to_res_id,
        )

        balanced_addition = 0
        balanced_subtraction = 0

        if points_log:
            balanced_addition = points_log.balanced_addition
            balanced_subtraction = points_log.balanced_subtraction

        if calc_result > 0:
            balanced_addition += calc_result
        else:
            balanced_subtraction += calc_result

        current_period = self.__period_service.get_current_semester_period_info()

        points_log_id = self.__points_log_repository.insert_points_log(
            data=PointsLogModel(
                owner_res_category=resource_data.owner_res_category,
                owner_res_id=resource_data.owner_res_id,
                gained_points=calc_result,
                symbol_id=calc_rule.belongs_to_res_id,
                balanced_addition=balanced_addition,
                balanced_subtraction=balanced_subtraction,
                status=EnumPointsLogStatus.CONFIRMED.name,
                belongs_to_period_id=current_period.id,
            ),
            transaction=transaction,
        )

        return BasicResource(category=EnumComprehensiveResource.POINTS_LOG.name, id=points_log_id)

    def revoke_points(self, cause_res_category: str, cause_res_id: str, transaction: Transaction):
        """
        撤销积分
        :param cause_res_category:
        :param cause_res_id:
        :param transaction:
        :return:
        """

        points_log_list = self.__points_log_repository.get_points_log_by_cause_res(
            cause_res_category=cause_res_category, cause_res_id=cause_res_id
        )

        for points_log in points_log_list:
            points_log.status = EnumPointsLogStatus.REVOKED.name
            self.__points_log_repository.update_points_log(
                data=points_log, transaction=transaction, limited_col_list=["status"]
            )
            last_points_log = (
                self.__points_log_repository.get_last_points_log_by_owner_res_and_symbol(
                    owner_res_id=points_log.owner_res_id,
                    owner_res_category=points_log.owner_res_category,
                    symbol_id=points_log.symbol_id,
                )
            )
            gained_points = points_log.gained_points * -1
            balanced_addition = last_points_log.balanced_addition
            balanced_subtraction = last_points_log.balanced_subtraction
            if points_log.gained_points > 0:
                balanced_addition = float(
                    Decimal(str(gained_points)) + Decimal(str(balanced_addition))
                )
            else:
                balanced_subtraction = float(
                    Decimal(str(gained_points)) + Decimal(str(balanced_subtraction))
                )
            self.__points_log_repository.insert_points_log(
                data=PointsLogModel(
                    owner_res_category=points_log.owner_res_category,
                    owner_res_id=points_log.owner_res_id,
                    gained_points=gained_points,
                    symbol_id=points_log.symbol_id,
                    balanced_addition=balanced_addition,
                    balanced_subtraction=balanced_subtraction,
                    status=EnumPointsLogStatus.REVERSED.name,
                    belongs_to_period_id=points_log.belongs_to_period_id,
                ),
                transaction=transaction,
            )
