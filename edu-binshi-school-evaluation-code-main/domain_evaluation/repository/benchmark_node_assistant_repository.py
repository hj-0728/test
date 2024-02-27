from typing import Optional

from infra_basic.basic_repository import BasicRepository

from domain_evaluation.model.view.benchmark_filler_vm import BenchmarkFillerViewModel
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.model.team_goal_model import EnumTeamGoalActivity, EnumTeamGoalCategory


class BenchmarkNodeAssistantRepository(BasicRepository):
    def fetch_student_teacher(
        self, subject_id: str, establishment_assign_id: str
    ) -> Optional[BenchmarkFillerViewModel]:
        """
        获取学生的任课老师
        """
        sql = """
        with dept as (
        select st.dimension_dept_tree_id, st.display_name as dept_name
        from cv_establishment_assign sa
        inner join cv_establishment se on sa.establishment_id = se.id
        inner join sv_dimension_dept_tree st on st.dimension_dept_tree_id = se.dimension_dept_tree_id
        where sa.id = :establishment_assign_id
        ),
        filler as (
        select sa2.id as filler_id from dept d
        inner join cv_k12_teacher_subject ss on ss.dimension_dept_tree_id = d.dimension_dept_tree_id
        and subject_id = :subject_id
        inner join cv_establishment se2 on se2.dimension_dept_tree_id = d.dimension_dept_tree_id
        inner join st_capacity sc on sc.id = se2.capacity_id and sc.code = any(array[:capacity_list])
        inner join cv_establishment_assign sa2 on sa2.establishment_id = se2.id
        and sa2.people_id = ss.people_id
        )
        select * from dept d left join filler on true
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=BenchmarkFillerViewModel,
            params={
                "subject_id": subject_id,
                "establishment_assign_id": establishment_assign_id,
                "capacity_list": [
                    EnumCapacityCode.HEAD_TEACHER.name,
                    EnumCapacityCode.TEACHER.name,
                ],
            },
        )

    def fetch_student_head_teacher(
        self, establishment_assign_id: str
    ) -> Optional[BenchmarkFillerViewModel]:
        """
        获取学生的班主任
        """
        sql = """
        with dept as (
        select st.dimension_dept_tree_id, st.display_name as dept_name
        from cv_establishment_assign sa
        inner join cv_establishment se on sa.establishment_id = se.id
        inner join sv_dimension_dept_tree st on st.dimension_dept_tree_id = se.dimension_dept_tree_id
        where sa.id = :establishment_assign_id
        ),
        filler as (
        select sa2.id as filler_id from dept d
        inner join cv_establishment se2 on se2.dimension_dept_tree_id = d.dimension_dept_tree_id
        inner join st_capacity sc on sc.id = se2.capacity_id and sc.code = :capacity
        inner join cv_establishment_assign sa2 on sa2.establishment_id = se2.id
        )
        select * from dept d left join filler on true
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=BenchmarkFillerViewModel,
            params={
                "establishment_assign_id": establishment_assign_id,
                "capacity": EnumCapacityCode.HEAD_TEACHER.name,
            },
        )

    def fetch_student_evaluation_team(
        self, establishment_assign_id: str, team_category_id: str
    ) -> Optional[BenchmarkFillerViewModel]:
        """
        获取学生的评价小组
        """
        sql = """
        select st.display_name as dept_name, sct.team_id as filler_id
        from cv_establishment_assign sa
        inner join cv_establishment se on sa.establishment_id = se.id
        inner join sv_dimension_dept_tree st on st.dimension_dept_tree_id = se.dimension_dept_tree_id
        left join sv_current_team sct on sct.goal_id = st.dimension_dept_tree_id and sct.goal_category = :goal_category
        and sct.activity = :activity and sct.team_category_id = :team_category_id
        where sa.id = :establishment_assign_id
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=BenchmarkFillerViewModel,
            params={
                "establishment_assign_id": establishment_assign_id,
                "team_category_id": team_category_id,
                "goal_category": EnumTeamGoalCategory.DIMENSION_DEPT_TREE.name,
                "activity": EnumTeamGoalActivity.EVALUATION.name,
            },
        )
