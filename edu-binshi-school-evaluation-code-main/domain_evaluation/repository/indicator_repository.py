from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from domain_evaluation.entity.indicator import IndicatorEntity
from domain_evaluation.model.indicator_model import IndicatorModel


class IndicatorRepository(BasicRepository):
    """
    指标 Repository
    """

    def insert_indicator(
        self,
        indicator: IndicatorModel,
        transaction: Transaction,
    ) -> str:
        """
        插入指标
        :param indicator:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=IndicatorEntity, entity_model=indicator, transaction=transaction
        )

    def update_indicator(
        self,
        indicator: IndicatorModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        :param indicator:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        return self._update_versioned_entity_by_model(
            entity_cls=IndicatorEntity,
            update_model=indicator,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def fetch_indicator_by_id(self, indicator_id: str) -> Optional[IndicatorModel]:
        """
        根据 id 获取指标
        :param indicator_id:
        :return:
        """

        sql = """
        select * 
        from st_indicator 
        where id=:indicator_id
        """

        return self._fetch_first_to_model(
            model_cls=IndicatorModel,
            sql=sql,
            params={
                "indicator_id": indicator_id
            }
        )
