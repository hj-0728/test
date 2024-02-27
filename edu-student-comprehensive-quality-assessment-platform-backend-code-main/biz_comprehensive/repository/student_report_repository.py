from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import OrderCondition, PageInitParams

from biz_comprehensive.model.param.student_report_query_params import (
    StudentReportPageFilterParams,
    StudentReportQueryParams,
)
from biz_comprehensive.model.scene_model import SceneModel
from biz_comprehensive.model.symbol_model import EnumSymbolCode
from biz_comprehensive.model.view.student_comprehensive_radar_vm import StudentScenePointsViewModel
from biz_comprehensive.model.view.student_growth_trend_vm import ObservationPointsViewModel
from biz_comprehensive.model.view.student_info_vm import StudentInfoViewModel
from biz_comprehensive.model.view.student_observation_point_log_vm import (
    StudentObservationPointLogViewModel,
)
from biz_comprehensive.model.view.student_statistics_vm import StudentStatisticsViewModel
from infra_backbone.data.enum import EnumBackboneResource, EnumFileRelationship


class StudentReportRepository(BasicRepository):
    def fetch_student_info(self, establishment_assign_id: str) -> Optional[StudentInfoViewModel]:
        """
        获取学生信息
        """
        sql = """
        select sp.id, sa.id as establishment_assign_id, sp.name, sr.public_link as avatar
        from st_establishment_assign sa
        inner join st_people sp on sp.id = sa.people_id
        inner join sv_file_relationship_public_link sr on sr.res_id = sp.id and sr.res_category = :people
        and sr.relationship = :avatar
        where sa.id = :establishment_assign_id
        """
        return self._fetch_first_to_model(
            model_cls=StudentInfoViewModel,
            sql=sql,
            params={
                "establishment_assign_id": establishment_assign_id,
                "people": EnumBackboneResource.PEOPLE.name,
                "avatar": EnumFileRelationship.AVATAR.name,
            },
        )

    def fetch_student_statistics(
        self, params: StudentReportQueryParams
    ) -> Optional[StudentStatisticsViewModel]:
        """
        获取学生统计信息
        """
        sql = """
        with stu_score as (
        select owner_res_id, sum(gained_points)  filter (where symbol_code = :points) as total_points,
        sum(gained_points)  filter (where symbol_code = :bright_spot) as total_bright_spot
        from st_establishment_assign sa
        inner join st_establishment se on se.id = sa.establishment_id
        inner join st_observation_point_points_snapshot ss on ss.dimension_dept_tree_id = se.dimension_dept_tree_id
        where sa.id = :establishment_assign_id
        and ss.owner_res_category = :establishment_assign
        and ss.observation_on >= :started_on and ss.observation_on < :ended_on
        and belongs_to_period_id = :period_id
        and symbol_code = any(array[:points, :bright_spot])
        group by owner_res_id
        ),
        rankings as (
        select *, rank() over (order by total_points desc) as rank
        from stu_score
        ),
        total_stu as (
        select count(*) as total_students from stu_score 
        ),
        cur_stu as (
        select * from rankings where owner_res_id = :establishment_assign_id
        )
        select sr.*, (sr.rank::decimal / ts.total_students) * 100 as percentage
        from cur_stu sr, total_stu ts
        """
        return self._fetch_first_to_model(
            model_cls=StudentStatisticsViewModel,
            sql=sql,
            params={
                **params.dict(),
                "establishment_assign": EnumBackboneResource.ESTABLISHMENT_ASSIGN.name,
                "points": EnumSymbolCode.POINTS.name,
                "bright_spot": EnumSymbolCode.BRIGHT_SPOT.name,
            },
        )

    def fetch_student_comprehensive_radar_data(
        self, params: StudentReportQueryParams
    ) -> List[StudentScenePointsViewModel]:
        """
        获取学生综合雷达图数据
        """
        sql = """
        with snapshot as (
        select owner_res_id, gained_points, unnest(scene_ids) as scene_id
        from st_establishment_assign sa
        inner join st_establishment se on se.id = sa.establishment_id
        inner join st_observation_point_points_snapshot ss on ss.dimension_dept_tree_id = se.dimension_dept_tree_id
        where sa.id = :establishment_assign_id
        and ss.owner_res_category = :establishment_assign
        and ss.observation_on >= :started_on and ss.observation_on < :ended_on
        and belongs_to_period_id = :period_id
        and symbol_code = :points
        ),
        res as (
        select owner_res_id, scene_id, sum(gained_points) as total_points
        from snapshot
        group by owner_res_id, scene_id
        ),
        scene_info as (
        select * from (
        select p.scene_id, sh.name, rank() over(partition by sh.id order by sh.ceased_on desc) as seq
        from res p
        inner join st_scene_history sh on sh.id = p.scene_id
        )aa where seq = 1
        ),
        class_data as (
        select scene_id, round(avg(total_points), 1) as total_points
        from res
        group by scene_id
        ),
        cur_stu as (
        select scene_id, total_points
        from res where owner_res_id = :establishment_assign_id
        )
        select distinct si.scene_id, si.name as scene_name, cd.total_points as class_avg_points,
        cs.total_points as student_total_points
        from class_data cd
        inner join cur_stu cs on cs.scene_id = cd.scene_id
        inner join scene_info si on si.scene_id = cd.scene_id
        order by si.name
        """
        return self._fetch_all_to_model(
            model_cls=StudentScenePointsViewModel,
            sql=sql,
            params={
                **params.dict(),
                "establishment_assign": EnumBackboneResource.ESTABLISHMENT_ASSIGN.name,
                "points": EnumSymbolCode.POINTS.name,
            },
        )

    def fetch_student_growth_trend_data(
        self, params: StudentReportQueryParams
    ) -> List[ObservationPointsViewModel]:
        """
        获取学生成长趋势数据
        """
        sql = """
        with res as (
        select owner_res_id, date_trunc('d', ss.observation_on) as observation_on, sum(gained_points) as total_points
        from st_establishment_assign sa
        inner join st_establishment se on se.id = sa.establishment_id
        inner join st_observation_point_points_snapshot ss on ss.dimension_dept_tree_id = se.dimension_dept_tree_id
        where sa.id = :establishment_assign_id
        and ss.owner_res_category = :establishment_assign
        and ss.observation_on >= :started_on and ss.observation_on < :ended_on
        and belongs_to_period_id = :period_id
        and symbol_code = :points
        group by owner_res_id, date_trunc('d', ss.observation_on)
        ),
        class_data as (
        select observation_on, round(avg(total_points), 1) as class_avg_points
        from res
        group by observation_on
        ),
        cur_stu as (
        select observation_on, total_points as student_total_points
        from res where owner_res_id = :establishment_assign_id
        )
        select cd.observation_on, cd.class_avg_points, cs.student_total_points
        from class_data cd
        inner join cur_stu cs on cd.observation_on = cs.observation_on
        order by cd.observation_on
        """
        return self._fetch_all_to_model(
            model_cls=ObservationPointsViewModel,
            sql=sql,
            params={
                **params.dict(),
                "establishment_assign": EnumBackboneResource.ESTABLISHMENT_ASSIGN.name,
                "points": EnumSymbolCode.POINTS.name,
            },
        )

    def fetch_student_observation_scene_list(
        self, params: StudentReportQueryParams
    ) -> List[SceneModel]:
        """
        获取学生观察场景列表
        """
        sql = """
        with snapshot as (
        select distinct sh.id, sh.name, rank() over(partition by sh.id order by sh.ceased_on desc) as seq
        from st_observation_point_points_snapshot ss
        inner join st_scene_history sh on sh.id = any(ss.scene_ids)
        where ss.owner_res_id = :establishment_assign_id
        and ss.owner_res_category = :establishment_assign
        and ss.observation_on >= :started_on and ss.observation_on < :ended_on
        and belongs_to_period_id = :period_id
        and symbol_code = :points
        )
        select * from snapshot where seq = 1
        order by name
        """
        return self._fetch_all_to_model(
            model_cls=SceneModel,
            sql=sql,
            params={
                **params.dict(),
                "establishment_assign": EnumBackboneResource.ESTABLISHMENT_ASSIGN.name,
                "points": EnumSymbolCode.POINTS.name,
            },
        )

    def fetch_student_observation_point_log_page_list(
        self, params: StudentReportPageFilterParams
    ) -> PaginationCarrier[StudentObservationPointLogViewModel]:
        """
        获取学生观察点日志分页列表
        """
        sql = """
        select ss.id, ss.observation_point_icon, ss.observation_action_performer_name, ss.observation_on,
        ss.observation_point_name, ss.observation_point_icon, opl.comment
        from st_observation_point_points_snapshot ss
        inner join st_observation_point_log opl on opl.id = ss.observation_point_log_id
        where ss.owner_res_id = :establishment_assign_id
        and ss.owner_res_category = :establishment_assign
        and ss.observation_on >= :started_on and ss.observation_on < :ended_on
        and belongs_to_period_id = :period_id
        and symbol_code = :points
        and :scene_id = any(ss.scene_ids)
        order by ss.observation_on desc
        """
        page_init_params = PageInitParams(
            sql=sql,
            order_columns=[
                OrderCondition(column_name="observation_on", order="desc"),
            ],
            params={
                **params.dict(),
                "establishment_assign": EnumBackboneResource.ESTABLISHMENT_ASSIGN.name,
                "points": EnumSymbolCode.POINTS.name,
            },
        )
        return self._paginate(
            result_type=StudentObservationPointLogViewModel,
            total_params=page_init_params,
            page_params=params,
        )
