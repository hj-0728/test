from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import OrderCondition, PageInitParams

from biz_comprehensive.model.observation_action_model import EnumPerformerResCategory
from biz_comprehensive.model.param.class_report_query_params import (
    ClassReportPageFilterParams,
    ClassReportQueryParams,
)
from biz_comprehensive.model.points_log_model import EnumPointsLogOwnerResCategory
from biz_comprehensive.model.symbol_model import EnumSymbolCode
from biz_comprehensive.model.view.observation_log_vm import ObservationLogViewModel
from biz_comprehensive.model.view.observation_points_count_vm import ObservationPointsCountViewModel
from biz_comprehensive.model.view.period_category_date_vm import EnumPeriodCategoryDate
from biz_comprehensive.model.view.ranking_item_vm import RankingItemViewModel
from infra_backbone.data.enum import EnumBackboneResource, EnumFileRelationship
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.model.people_model import PeopleModel


class ClassReportRepository(BasicRepository):
    def fetch_class_observation_points_count(
        self, params: ClassReportQueryParams
    ) -> List[ObservationPointsCountViewModel]:
        """
        获取观察点数量统计
        """

        if params.period_category == EnumPeriodCategoryDate.SEMESTER.name:
            sql = """
            select observation_point_category as category, sum(gained_points) as points
            from st_observation_point_points_snapshot ss
            where ss.dimension_dept_tree_id = :tree_id
            and ss.belongs_to_period_id = :period_id
            and ss.symbol_code = :points
            and ss.owner_res_category = :establishment_assign
            group by observation_point_category
            """
        else:
            sql = """
            select observation_point_category as category, sum(gained_points) as points
            from st_observation_point_points_snapshot ss
            where ss.dimension_dept_tree_id = :tree_id
            and ss.observation_on >= :started_on and ss.observation_on < :ended_on
            and ss.belongs_to_period_id = :period_id
            and ss.symbol_code = :points
            and ss.owner_res_category = :establishment_assign
            group by observation_point_category
            """
        return self._fetch_all_to_model(
            model_cls=ObservationPointsCountViewModel,
            sql=sql,
            params={
                **params.dict(),
                "points": EnumSymbolCode.POINTS.name,
                "establishment_assign": EnumPointsLogOwnerResCategory.ESTABLISHMENT_ASSIGN.name,
            },
        )

    def fetch_class_top3_ranking(
        self, params: ClassReportQueryParams
    ) -> List[RankingItemViewModel]:
        """
        获取前3名排行榜
        :param params:
        :return:
        """
        sql = """
        with owner as (
        select owner_res_id as establishment_assign_id, sum(gained_points) as points
        from st_observation_point_points_snapshot
        where dimension_dept_tree_id = :tree_id
        and observation_on >= :started_on and observation_on < :ended_on
        and belongs_to_period_id = :period_id
        and owner_res_category = :establishment_assign
        and symbol_code = :points
        group by owner_res_id
        order by points desc limit 3
        )
        select distinct n.*, sp.id, sp.name from owner n
        inner join st_establishment_assign_history sh on sh.id = n.establishment_assign_id
        inner join st_people sp on sp.id = sh.people_id
        order by points desc
        """
        return self._fetch_all_to_model(
            model_cls=RankingItemViewModel,
            sql=sql,
            params={
                **params.dict(),
                "establishment_assign": EnumPointsLogOwnerResCategory.ESTABLISHMENT_ASSIGN.name,
                "points": EnumSymbolCode.POINTS.name,
            },
        )

    def fetch_top3_ranking_missing_people(
        self, existed_assign_ids: List[str], tree_id: str, missing_count: int
    ) -> List[RankingItemViewModel]:
        """
        获取前3名排行榜缺少的人
        :return:
        """
        sql = """
        select sa.id as establishment_assign_id, 0 as points, sp.id, sp.name
        from st_establishment se	
        inner join st_capacity sc on sc.id = se.capacity_id and sc.code = :student
        inner join st_establishment_assign sa on sa.establishment_id = se.id
        inner join st_people sp on sp.id = sa.people_id
        where se.dimension_dept_tree_id = :tree_id
        and sa.id != all(array[:existed_assign_ids])
        order by sp.name limit :missing_count
        """
        return self._fetch_all_to_model(
            model_cls=RankingItemViewModel,
            sql=sql,
            params={
                "student": EnumCapacityCode.STUDENT.name,
                "tree_id": tree_id,
                "existed_assign_ids": existed_assign_ids,
                "missing_count": missing_count,
            },
        )

    def fetch_class_full_ranking(
        self, params: ClassReportQueryParams
    ) -> List[RankingItemViewModel]:
        """
        获取完成的排行榜
        :param params:
        :return:
        """
        sql = """
        with owner as (
        select owner_res_id as establishment_assign_id, sum(gained_points) as points
        from st_observation_point_points_snapshot
        where dimension_dept_tree_id = :tree_id
        and observation_on >= :started_on and observation_on < :ended_on
        and belongs_to_period_id = :period_id
        and owner_res_category = :establishment_assign
        and symbol_code = :points
        group by owner_res_id
        ),
        ppl as (
        select distinct n.*, sp.id, sp.name
        from owner n
        inner join st_establishment_assign_history sh on sh.id = n.establishment_assign_id
        inner join st_people sp on sp.id = sh.people_id
        union all
        select sa.id, 0, sp.id, sp.name
        from st_establishment se	
        inner join st_capacity sc on sc.id = se.capacity_id and sc.code = :student
        inner join st_establishment_assign sa on sa.establishment_id = se.id
        inner join st_people sp on sp.id = sa.people_id
        where se.dimension_dept_tree_id = :tree_id
        and not exists (select * from owner o where o.establishment_assign_id = sa.id)
        )
        select ppl.*, sl.public_link as avatar , rank() over(order by points desc, name) as seq
        from ppl
        inner join sv_file_relationship_public_link sl on sl.res_id = ppl.id and sl.res_category = :people
        and sl.relationship = :avatar
        """
        return self._fetch_all_to_model(
            model_cls=RankingItemViewModel,
            sql=sql,
            params={
                **params.dict(),
                "student": EnumCapacityCode.STUDENT.name,
                "establishment_assign": EnumPointsLogOwnerResCategory.ESTABLISHMENT_ASSIGN.name,
                "points": EnumSymbolCode.POINTS.name,
                "people": EnumBackboneResource.PEOPLE.name,
                "avatar": EnumFileRelationship.AVATAR.name,
            },
        )

    def fetch_observation_teacher(self, params: ClassReportQueryParams) -> List[PeopleModel]:
        """
        获取观察教师
        :return:
        """
        sql = """
        select distinct sp.id, sp.name
        from st_observation_point_points_snapshot ss
        inner join st_observation_action soa on soa.id = ss.observation_action_id
        inner join st_people sp on sp.id = soa.performer_res_id and soa.performer_res_category = :people
        where ss.dimension_dept_tree_id = :tree_id
        and ss.observation_on >= :started_on and ss.observation_on < :ended_on
        and ss.belongs_to_period_id = :period_id
        and ss.symbol_code = :points
        order by sp.name
        """
        return self._fetch_all_to_model(
            model_cls=PeopleModel,
            sql=sql,
            params={
                **params.dict(),
                "people": EnumPerformerResCategory.PEOPLE.name,
                "points": EnumSymbolCode.POINTS.name,
            },
        )

    def fetch_observation_log_page_list(
        self, params: ClassReportPageFilterParams
    ) -> PaginationCarrier[ObservationLogViewModel]:
        """
        获取观察日志
        :return:
        """
        sql = """
        select distinct observation_action_id, ss.handled_on as observation_on, observation_point_name,
        observation_point_icon, sol.comment,
        case when sol.observee_res_category = :dimension_dept_tree then '全班' else observee_name end as observee_name
        from st_observation_point_points_snapshot ss
        inner join st_observation_action soa on soa.id = ss.observation_action_id
        inner join st_observation_point_log sol on sol.id = ss.observation_point_log_id
        where ss.dimension_dept_tree_id = :tree_id
        and ss.observation_on >= :started_on and ss.observation_on < :ended_on
        and ss.belongs_to_period_id = :period_id
        and ss.symbol_code = :points
        and soa.performer_res_category = :people and soa.performer_res_id = :performer_res_id
        """
        page_init_params = PageInitParams(
            sql=sql,
            order_columns=[
                OrderCondition(column_name="observation_on", order="desc"),
            ],
            filter_columns=["observee_name", "observation_point_name"],
            params={
                **params.dict(),
                "icon": EnumFileRelationship.ICON.name,
                "people": EnumPerformerResCategory.PEOPLE.name,
                "points": EnumSymbolCode.POINTS.name,
                "dimension_dept_tree": EnumBackboneResource.DIMENSION_DEPT_TREE.name,
            },
        )
        return self._paginate(
            result_type=ObservationLogViewModel,
            total_params=page_init_params,
            page_params=params,
        )
