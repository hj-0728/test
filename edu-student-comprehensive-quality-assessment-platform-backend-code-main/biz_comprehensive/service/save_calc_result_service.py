from datetime import datetime
from typing import Any, List, Optional

from infra_basic.basic_resource import BasicResource
from infra_basic.transaction import Transaction

from biz_comprehensive.model.calc_log_model import CalcLogModel
from biz_comprehensive.model.calc_rule_model import CalcRuleModel, EnumBelongsToResCategory
from biz_comprehensive.model.causation_model import CausationModel, EnumCausationEffectResCategory
from biz_comprehensive.model.edit.calc_em import CalcResourceEditModel
from biz_comprehensive.model.log_clue_model import EnumLogClueClueResCategory, LogClueModel
from biz_comprehensive.repository.calc_log_repository import CalcLogRepository
from biz_comprehensive.repository.causation_repository import CausationRepository
from biz_comprehensive.repository.log_clue_repository import LogClueRepository
from biz_comprehensive.service.indicator_score_service import IndicatorScoreService
from biz_comprehensive.service.medal_issued_log_service import MedalIssuedLogService
from biz_comprehensive.service.points_log_service import PointsLogService


class SaveCalcResultService:
    def __init__(
        self,
        calc_log_repository: CalcLogRepository,
        causation_repository: CausationRepository,
        points_log_service: PointsLogService,
        medal_issued_log_service: MedalIssuedLogService,
        indicator_score_service: IndicatorScoreService,
        log_clue_repository: LogClueRepository,
    ):
        self.__calc_log_repository = calc_log_repository
        self.__causation_repository = causation_repository
        self.__points_log_service = points_log_service
        self.__medal_issued_log_service = medal_issued_log_service
        self.__indicator_score_service = indicator_score_service
        self.__log_clue_repository = log_clue_repository

    def save_calc_result(
        self,
        calc_rule: CalcRuleModel,
        calc_log_result: CalcLogModel,
        resource_data: CalcResourceEditModel,
        transaction: Transaction,
    ) -> Optional[List[BasicResource]]:
        """
        保存计算结果及日志
        :return:
        """
        if not calc_log_result.calc_result:
            return
        calc_log_id = self.__calc_log_repository.insert_calc_log(
            data=calc_log_result, transaction=transaction
        )

        self.__causation_repository.insert_causation(
            data=CausationModel(
                cause_res_category=resource_data.clue_res_category,
                cause_res_id=resource_data.clue_res_id,
                effect_res_category=EnumCausationEffectResCategory.CALC_LOG.name,
                effect_res_id=calc_log_id,
                effected_on=datetime.now(),
            ),
            transaction=transaction,
        )

        log_res_list = []

        for res_result in calc_log_result.calc_result.get("calc_result", []):
            log_res = self.save_calc_result_log(
                calc_rule=calc_rule,
                calc_result=res_result.calc_result,
                resource_data=resource_data.cast_to(
                    CalcResourceEditModel,
                    owner_res_id=res_result.owner_res_id,
                    owner_res_category=res_result.owner_res_category,
                ),
                transaction=transaction,
            )

            log_res_list.append(log_res)

            self.__log_clue_repository.insert_log_clue(
                data=LogClueModel(
                    log_res_category=log_res.res_category,
                    log_res_id=log_res.id,
                    clue_res_category=EnumLogClueClueResCategory.CALC_LOG.name,
                    clue_res_id=calc_log_id,
                ),
                transaction=transaction,
            )

        return log_res_list

    def save_calc_result_log(
        self,
        calc_rule: CalcRuleModel,
        calc_result: Any,
        resource_data: CalcResourceEditModel,
        transaction: Transaction,
    ) -> BasicResource:
        """
        保存计算结果及日志
        :return:
        """
        save_result_log_func = {
            EnumBelongsToResCategory.INDICATOR.name: self.__indicator_score_service.save_indicator_score,
            EnumBelongsToResCategory.SYMBOL.name: self.__points_log_service.save_points_log,
            EnumBelongsToResCategory.MEDAL.name: self.__medal_issued_log_service.save_medal_issued_log,
            EnumBelongsToResCategory.EVALUATION_CRITERIA.name: self.__indicator_score_service.save_evaluation_criteria_score,
        }

        log_res = save_result_log_func[calc_rule.belongs_to_res_category](
            calc_rule=calc_rule,
            calc_result=calc_result,
            resource_data=resource_data,
            transaction=transaction,
        )

        if log_res:
            self.__causation_repository.insert_causation(
                data=CausationModel(
                    cause_res_category=resource_data.clue_res_category,
                    cause_res_id=resource_data.clue_res_id,
                    effect_res_category=log_res.res_category,
                    effect_res_id=log_res.res_id,
                    effected_on=datetime.now(),
                ),
                transaction=transaction,
            )

        return log_res
