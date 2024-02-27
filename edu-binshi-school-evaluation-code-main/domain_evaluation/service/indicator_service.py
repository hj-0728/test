from infra_basic.transaction import Transaction

from domain_evaluation.model.indicator_model import IndicatorModel
from domain_evaluation.repository.indicator_repository import IndicatorRepository


class IndicatorService:
    """
    指标 service
    """

    def __init__(self, indicator_repository: IndicatorRepository):
        self.__indicator_repository = indicator_repository

    def save_indicator(self, indicator: IndicatorModel, transaction: Transaction):
        """
        保存指标
        """
        if not indicator.id:
            return self.__indicator_repository.insert_indicator(
                indicator=indicator, transaction=transaction
            )
        self.__indicator_repository.update_indicator(
            indicator=indicator, transaction=transaction, limited_col_list=["name", "comments"]
        )
        return indicator.id
