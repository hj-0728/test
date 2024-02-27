"""
学期 repository
"""
from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from biz_comprehensive.entity.period import PeriodEntity
from biz_comprehensive.model.period_model import PeriodModel


class PeriodRepository(BasicRepository):
    """
    学期 repository
    """

    def insert_period(
        self,
        period: PeriodModel,
        transaction: Transaction,
    ):
        """
        添加周期
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=PeriodEntity, entity_model=period, transaction=transaction
        )

    def get_current_period_info_by_period_category(
        self, period_category: str
    ) -> Optional[PeriodModel]:
        """
        根据周期类型获取当前周期
        :param period_category:
        :return:
        """
        sql = """
        select sp.*, spc.code as category_code, spc.name as category_name from st_period sp
        join st_period_category spc on sp.period_category_id = spc.id
        where spc.code = :period_category and sp.started_on <= now() and sp.ended_on > now()
        """
        return self._fetch_first_to_model(
            model_cls=PeriodModel, sql=sql, params={"period_category": period_category}
        )

    def get_period_list_by_category_code_list(
        self, period_category_code_list: List[str]
    ) -> List[PeriodModel]:
        """

        :param period_category_code_list:
        :return:
        """

        sql = """
        select p.* from st_period p 
        inner join st_period_category pc on p.period_category_id=pc.id
        where pc.code=any(array[:period_category_code_list])
        """

        return self._fetch_all_to_model(
            model_cls=PeriodModel,
            sql=sql,
            params={"period_category_code_list": period_category_code_list},
        )

    def get_period_by_id(self, period_id: str) -> Optional[PeriodModel]:
        """

        :param period_id:
        :return:
        """

        sql = """
        select p.*,pc.code as category_code,pc.name as category_name
        from st_period p 
        inner join st_period_category pc on p.period_category_id=pc.id
        where p.id=:period_id
        """

        return self._fetch_first_to_model(
            model_cls=PeriodModel, sql=sql, params={"period_id": period_id}
        )

    def get_period_by_category(self, period_category: str) -> List[PeriodModel]:
        """
        根据周期类型获取当前周期
        :param period_category:
        :return:
        """
        sql = """
        select sp.*, spc.code as category_code, spc.name as category_name from st_period sp
        join st_period_category spc on sp.period_category_id = spc.id
        where spc.code = :period_category 
        order by sp.started_on desc
        """
        return self._fetch_all_to_model(
            model_cls=PeriodModel, sql=sql, params={"period_category": period_category}
        )

    def get_period_list_by_category_code(self, period_category_code: str) -> List[PeriodModel]:
        """
        根据周期类型获取当前周期
        :param period_category_code:
        :return:
        """

        sql = """
        select p.* from st_period p 
        inner join st_period_category pc on p.period_category_id=pc.id
        where pc.code=:period_category_code
        order by started_on desc
        """

        return self._fetch_all_to_model(
            model_cls=PeriodModel,
            sql=sql,
            params={"period_category_code": period_category_code},
        )
