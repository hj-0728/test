from datetime import datetime

from infra_basic.basic_resource import BasicResource
from infra_basic.transaction import Transaction

from biz_comprehensive.data.enum import EnumComprehensiveResource
from biz_comprehensive.model.calc_rule_model import CalcRuleModel
from biz_comprehensive.model.edit.calc_em import CalcResourceEditModel
from biz_comprehensive.model.medal_issued_log_model import (
    EnumMedalIssuedLogStatus,
    MedalIssuedLogModel,
)
from biz_comprehensive.repository.medal_issued_log_repository import MedalIssuedLogRepository


class MedalIssuedLogService:
    def __init__(self, medal_issued_log_repository: MedalIssuedLogRepository):
        self.__medal_issued_log_repository = medal_issued_log_repository

    def save_medal_issued_log(
        self,
        calc_rule: CalcRuleModel,
        calc_result: int,
        resource_data: CalcResourceEditModel,
        transaction: Transaction,
    ):
        """
        保存勋章发放日志
        :param calc_rule:
        :param calc_result:
        :param resource_data:
        :param transaction:
        :return:
        """

        if calc_result <= 0:
            return

        medal_issued_log_id = self.__medal_issued_log_repository.insert_medal_issued_log(
            data=MedalIssuedLogModel(
                medal_id=calc_rule.belongs_to_res_id,
                calc_rule_id=calc_rule.id,
                issued_res_category=calc_rule.belongs_to_res_id,
                issued_res_id=calc_rule.belongs_to_res_id,
                issued_on=datetime.now(),
                status=EnumMedalIssuedLogStatus.ISSUED.name,
            ),
            transaction=transaction,
        )

        return BasicResource(
            category=EnumComprehensiveResource.MEDAL_ISSUE_LOG.name, id=medal_issued_log_id
        )
