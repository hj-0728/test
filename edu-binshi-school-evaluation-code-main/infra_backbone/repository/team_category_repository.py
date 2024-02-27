from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import OrderCondition, PageFilterParams, PageInitParams
from infra_basic.transaction import Transaction

from infra_backbone.entity.team_category import TeamCategoryEntity
from infra_backbone.model.team_category_model import TeamCategoryModel
from infra_backbone.model.params.team_category_query_params import TeamCategoryQueryParams


class TeamCategoryRepository(BasicRepository):
    """
    小组类型 repository
    """

    def get_team_category_by_name(
        self,
        name: str,
        team_category_id: Optional[str],
    ) -> Optional[TeamCategoryModel]:
        """
        通过name获取小组类型
        :param name:
        :param team_category_id:
        :return:
        """
        sql = """
        select * from st_team_category 
        where name=:name
        """

        if team_category_id:
            sql += """
            AND id!=:team_category_id
            """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=TeamCategoryModel,
            params={"name": name, "team_category_id": team_category_id},
        )

    def update_team_category(
        self,
        team_category: TeamCategoryModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新小组类型
        """
        self._update_versioned_entity_by_model(
            entity_cls=TeamCategoryEntity,
            update_model=team_category,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def insert_team_category(self, team_category: TeamCategoryModel, transaction: Transaction):
        """
        插入小组类型
        """
        self._insert_versioned_entity_by_model(
            entity_cls=TeamCategoryEntity, entity_model=team_category, transaction=transaction
        )

    def fetch_team_category(self) -> List[TeamCategoryModel]:
        """
        获取小组类型
        """
        sql = """select * from st_team_category where is_activated is true"""
        return self._fetch_all_to_model(model_cls=TeamCategoryModel, sql=sql)

    def fetch_team_category_page(
        self, query_params: TeamCategoryQueryParams
    ) -> PaginationCarrier[TeamCategoryModel]:
        """
        获取小组类型
        """
        sql = """select * from st_team_category"""
        if query_params.is_activated and query_params.is_activated == "isActivated":
            sql += """ where is_activated is true"""
        if query_params.is_activated and query_params.is_activated == "isNotActivated":
            sql += """ where is_activated is false"""
        page_init_params = PageInitParams(
            sql=sql,
            order_columns=[OrderCondition(column_name="name")],
            filter_columns=[
                "name",
            ],
        )
        return self._paginate(
            result_type=TeamCategoryModel,
            total_params=page_init_params,
            page_params=query_params,
        )

    def get_team_category_detail(
        self,
        team_category_id: str,
    ) -> TeamCategoryModel:
        """
        获取小组类型详情
        :param team_category_id:
        :return:
        """

        sql = """
        SELECT stc.id, stc.version, stc.name, stc.code, stc.is_activated
        FROM st_team_category stc
        WHERE stc.id = :team_category_id
        """

        return self._fetch_first_to_model(
            model_cls=TeamCategoryModel,
            sql=sql,
            params={
                "team_category_id": team_category_id,
            },
        )

    def fetch_team_category_by_id(self, team_category_id: str) -> Optional[TeamCategoryModel]:
        """
        通过id获取小组类型
        """
        sql = """select * from st_team_category where id=:team_category_id"""
        return self._fetch_first_to_model(
            model_cls=TeamCategoryModel, sql=sql, params={"team_category_id": team_category_id}
        )

    def get_team_category_for_prepare_only_one_team_category_schema(self,benchmark_id: Optional[str]) -> List[TeamCategoryModel]:
        """
        获取小组类型
        (获取当下可未被禁用的小组类型，以及传入的benchmark_id关联的小组类型，
        因为有可能被禁用了，所以还是得捞出来让用户看到以前选的什么)
        """
        sql = """
        select * from st_team_category where is_activated is true
        
        """
        if benchmark_id:
            sql += """
            union
            select tc.* from st_team_category tc 
            inner join cv_benchmark cb on cb.benchmark_strategy_params ->> 'teamCategoryId' = tc.id
            where cb.id = :benchmark_id
            """
        return self._fetch_all_to_model(
            model_cls=TeamCategoryModel,
            sql=sql,
            params={
                "benchmark_id": benchmark_id
            }
        )