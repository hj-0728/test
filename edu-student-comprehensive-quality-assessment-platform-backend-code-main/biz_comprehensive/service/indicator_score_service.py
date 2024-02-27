from typing import Any

from infra_basic.basic_resource import BasicResource
from infra_basic.transaction import Transaction

from biz_comprehensive.data.enum import EnumComprehensiveResource
from biz_comprehensive.model.calc_rule_model import CalcRuleModel
from biz_comprehensive.model.edit.calc_em import CalcResourceEditModel
from biz_comprehensive.model.indicator_final_score_model import IndicatorFinalScoreModel
from biz_comprehensive.model.indicator_score_log_model import IndicatorScoreLogModel
from biz_comprehensive.repository.indicator_final_score_repository import (
    IndicatorFinalScoreRepository,
)
from biz_comprehensive.repository.indicator_score_log_repository import IndicatorScoreLogRepository


class IndicatorScoreService:
    def __init__(
        self,
        indicator_score_log_repository: IndicatorScoreLogRepository,
        indicator_final_score_repository: IndicatorFinalScoreRepository,
    ):
        self.__indicator_score_log_repository = indicator_score_log_repository
        self.__indicator_final_score_repository = indicator_final_score_repository

    def save_indicator_score(
        self,
        calc_rule: CalcRuleModel,
        calc_result: Any,
        resource_data: CalcResourceEditModel,
        transaction: Transaction,
    ) -> BasicResource:
        """
        保存指标分数日志
        :param calc_rule:
        :param calc_result:
        :param resource_data:
        :param transaction:
        :return:
        """

        string_score = None
        numeric_score = None

        if isinstance(calc_result, str):
            string_score = calc_result
        else:
            numeric_score = calc_result

        indicator_score = self.__indicator_final_score_repository.get_indicator_final_score_by_owner_res_and_indicator(
            owner_res_id=resource_data.owner_res_id,
            owner_res_category=resource_data.owner_res_category,
            indicator_id=calc_rule.belongs_to_res_id,
        )

        if indicator_score:
            indicator_score_id = indicator_score.id

            indicator_score.string_score = string_score
            indicator_score.numeric_score = numeric_score

            self.__indicator_final_score_repository.update_indicator_final_score(
                data=indicator_score,
                transaction=transaction,
                limited_col_list=["numeric_score", "string_score"],
            )
        else:
            indicator_score = IndicatorFinalScoreModel(
                owner_res_id=resource_data.owner_res_id,
                owner_res_category=resource_data.owner_res_category,
                indicator_id=calc_rule.belongs_to_res_id,
                string_score=string_score,
                numeric_score=numeric_score,
            )

            indicator_score_id = (
                self.__indicator_final_score_repository.insert_indicator_final_score(
                    data=indicator_score,
                    transaction=transaction,
                )
            )

        indicator_score_log_id = self.__indicator_score_log_repository.insert_indicator_score_log(
            data=IndicatorScoreLogModel(
                indicator_score_id=indicator_score_id,
                owner_res_category=resource_data.owner_res_category,
                owner_res_id=resource_data.owner_res_id,
                string_score=string_score,
                numeric_score=numeric_score,
            ),
            transaction=transaction,
        )

        return BasicResource(
            category=EnumComprehensiveResource.MEDAL_ISSUE_LOG.name, id=indicator_score_log_id
        )

    def save_evaluation_criteria_score(
        self,
        calc_rule: CalcRuleModel,
        calc_result: Any,
        resource_data: CalcResourceEditModel,
        transaction: Transaction,
    ):
        """
        保存评价标准分数日志
        :param calc_rule:
        :param calc_result:
        :param resource_data:
        :param transaction:
        :return:
        """

        pass
