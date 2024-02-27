"""
周期类型 repository
"""
from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from edu_binshi.entity.period_category import PeriodCategoryEntity
from edu_binshi.model.period_category_model import PeriodCategoryModel


class PeriodCategoryRepository(BasicRepository):
    """
    周期类型 repository
    """

    def insert_period_category(
        self,
        period_category: PeriodCategoryModel,
        transaction: Transaction,
    ):
        """
        添加周期类型
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=PeriodCategoryEntity, entity_model=period_category, transaction=transaction
        )

    def get_period_category_by_code(
        self, period_category_code: str
    ) -> Optional[PeriodCategoryModel]:
        """

        :param period_category_code:
        :return:
        """

        sql = """
        select * from st_period_category where code=:period_category_code
        """

        return self._fetch_first_to_model(
            model_cls=PeriodCategoryModel,
            sql=sql,
            params={"period_category_code": period_category_code},
        )

    def get_period_category_list(
        self,
    ) -> List[PeriodCategoryModel]:
        """
        获取周期类型列表
        :return:
        """

        sql = """
        select * from st_period_category
        """

        return self._fetch_all_to_model(
            model_cls=PeriodCategoryModel,
            sql=sql,
            params={},
        )
