"""
学期 repository
"""
from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from edu_binshi.entity.period import PeriodEntity
from edu_binshi.model.period_model import PeriodModel
from edu_binshi.model.view.period_vm import PeriodTreeNodeVm


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
        where spc.code = :period_category and sp.start_at <= now() and sp.finish_at >= now()
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
        order by sp.start_at DESC
        """
        return self._fetch_all_to_model(
            model_cls=PeriodModel, sql=sql, params={"period_category": period_category}
        )

    def get_period_tree_list(self, period_category_code: str = None) -> List[PeriodTreeNodeVm]:
        """
        获取周期树
        :param period_category_code:
        :return:
        """
        sql = """
        WITH RECURSIVE period AS (
        SELECT sp.id, sp.period_category_id, sp.name, sp.start_at, sp.finish_at, sp.parent_id, 
        ARRAY[sp.id::text] AS path_ids, spc.name AS category_name, spc.code AS category_code
        FROM st_period sp
        INNER JOIN st_period_category spc ON spc.id = sp.period_category_id
        WHERE sp.parent_id IS NULL
        UNION ALL
        SELECT sp.id, sp.period_category_id, sp.name, sp.start_at, sp.finish_at, sp.parent_id,
        array_append(p_1.path_ids, sp.id::text) AS array_append, spc.name AS category_name, spc.code AS category_code
        FROM st_period sp
        JOIN period p_1 ON p_1.id = sp.parent_id
        INNER JOIN st_period_category spc ON spc.id = sp.period_category_id
        )
        """

        if period_category_code:
            sql += """
            , filter_ids AS (
            SELECT DISTINCT UNNEST(p.path_ids) AS id
            FROM period p
            WHERE p.category_code = :period_category_code
            )
            """

        sql += """
        SELECT p.*
        FROM period p
        """

        if period_category_code:
            sql += """
            INNER JOIN filter_ids fi ON fi.id = p.id
            """

        return self._fetch_all_to_model(
            model_cls=PeriodTreeNodeVm,
            sql=sql,
            params={"period_category_code": period_category_code},
        )

    def get_period_list_by_category_code(self, period_category_code: str) -> List[PeriodModel]:
        """
        根据周期类型获取当前周期
        :param period_category_code:
        :return:
        """

        sql = """
        select p.* from st_period p 
        INNER JOIN st_period_category pc on p.period_category_id=pc.id
        where pc.code=:period_category_code
        ORDER BY start_at desc
        """

        return self._fetch_all_to_model(
            model_cls=PeriodModel,
            sql=sql,
            params={"period_category_code": period_category_code},
        )
