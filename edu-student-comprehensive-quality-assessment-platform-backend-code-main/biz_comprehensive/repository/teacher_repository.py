from datetime import datetime
from typing import List

from infra_basic.basic_repository import BasicRepository

from backend.model.view.grade_class_vm import GradeClassViewModel
from backend.model.view.teacher_class_vm import TeacherClassViewModel
from backend.model.view.teacher_info_vm import TeacherInfoViewModel
from biz_comprehensive.model.param.teacher_observation_query_params import (
    TeacherObservationQueryParams,
)
from biz_comprehensive.model.points_log_model import (
    EnumPointsLogOwnerResCategory,
    EnumPointsLogStatus,
)
from biz_comprehensive.model.symbol_model import EnumSymbolCode
from biz_comprehensive.model.view.observation_class_vm import ObservationClassViewModel
from biz_comprehensive.model.view.student_info_vm import StudentInfoViewModel
from infra_backbone.data.enum import EnumBackboneResource, EnumFileRelationship
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.model.dept_category_model import EnumDeptCategoryCode


class TeacherRepository(BasicRepository):
    def fetch_teacher_class_list(
        self, people_id, points_due_on: datetime, period_id: str
    ) -> List[TeacherClassViewModel]:
        """
        获取老师的班级列表
        """
        sql = """with dept as (
        select distinct sd1.id, st.id as dimension_dept_tree_id, sd2.name || '/' || sd1.name as name,
        sr.public_link as avatar
        from st_establishment_assign sa
        inner join st_establishment se on se.id = sa.establishment_id
        inner join st_capacity sc on sc.id = se.capacity_id and sc.code = any(array[:teacher_capacity_list])
        inner join st_dimension_dept_tree st on st.id = se.dimension_dept_tree_id
        inner join st_dept sd1 on sd1.id = st.dept_id
        inner join st_dept sd2 on sd2.id = st.parent_dept_id
        inner join sv_file_relationship_public_link sr on sr.res_id = sd1.id and sr.res_category = :dept
        and sr.relationship = :avatar
        where sa.people_id = :people_id
        ), 
        stat_data as (
        select se.dimension_dept_tree_id, count(distinct sa.people_id) as student_count,
        sum(gained_points) as points_count
        from st_establishment se 
        inner join dept d on se.dimension_dept_tree_id = d.dimension_dept_tree_id
        inner join st_capacity sc on sc.id = se.capacity_id and sc.code = :student
        inner join st_establishment_assign sa on sa.establishment_id = se.id
        left join st_points_log sl on sl.owner_res_category = :establishment_assign and sl.owner_res_id = sa.id
        and sl.status= :confirmed and sl.handled_on >= :points_due_on
        and sl.belongs_to_period_id = :period_id
        left join st_symbol ss on ss.id = sl.symbol_id and ss.code = :symbol_code
        group by se.dimension_dept_tree_id
        )
        select d.*, coalesce(sd.student_count, 0) as student_count, coalesce(sd.points_count, 0) as points_count
        from dept d
        inner join stat_data sd on d.dimension_dept_tree_id = sd.dimension_dept_tree_id
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=TeacherClassViewModel,
            params={
                "people_id": people_id,
                "confirmed": EnumPointsLogStatus.CONFIRMED.name,
                "dept": EnumBackboneResource.DEPT.name,
                "establishment_assign": EnumPointsLogOwnerResCategory.ESTABLISHMENT_ASSIGN.name,
                "student": EnumCapacityCode.STUDENT.name,
                "teacher_capacity_list": [
                    EnumCapacityCode.TEACHER.name,
                    EnumCapacityCode.HEAD_TEACHER.name,
                ],
                "points_due_on": points_due_on,
                "symbol_code": EnumSymbolCode.POINTS.name,
                "avatar": EnumFileRelationship.AVATAR.name,
                "period_id": period_id,
            },
        )

    def fetch_grade_class_list(self) -> List[GradeClassViewModel]:
        """
        获取年级和年级内的班级列表
        """
        sql = """
        select st.parent_dept_id, st.parent_name, st.id, st.name, sr.public_link as avatar, st.dimension_dept_tree_id
        from sv_k12_dept_tree st
        inner join st_dept_dept_category_map sm on sm.dept_id = st.id
        inner join st_dept_category sc on sc.id = sm.dept_category_id
        and sc.code = :class
        inner join sv_file_relationship_public_link sr on sr.res_category = :dept and sr.res_id = st.id
        and sr.relationship = :avatar
        order by st.seq_list
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=GradeClassViewModel,
            params={
                "class": EnumDeptCategoryCode.CLASS.name,
                "dept": EnumBackboneResource.DEPT.name,
                "avatar": EnumFileRelationship.AVATAR.name,
            },
        )

    def fetch_student_by_name_keyword(self, search_text: str) -> List[StudentInfoViewModel]:
        """
        搜索学生
        """
        sql = """
        select sp.id, sp.name, sr.public_link as avatar, sd.name as dept_name, sea.id as establishment_assign_id
        from st_people sp
        inner join st_establishment_assign sea on sea.people_id = sp.id
        inner join st_establishment se on se.id = sea.establishment_id
        inner join st_capacity sc on sc.id = se.capacity_id and sc.code = :student
        inner join st_dimension_dept_tree sddt on sddt.id = se.dimension_dept_tree_id
        inner join st_dept sd on sd.id = sddt.dept_id
        inner join sv_file_relationship_public_link sr on sr.res_id = sp.id and sr.res_category = :people
        and sr.relationship = :avatar
        where sp.name like :search_text
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=StudentInfoViewModel,
            params={
                "search_text": f"%{search_text}%",
                "people": EnumBackboneResource.PEOPLE.name,
                "student": EnumCapacityCode.STUDENT.name,
                "avatar": EnumFileRelationship.AVATAR.name,
            },
        )

    def fetch_teacher_info(self, people_id: str) -> TeacherInfoViewModel:
        """
        获取老师信息
        """
        sql = """
        select sp.id, sp.name, sr.public_link as avatar, count(sa.id) > 0 as is_taught
        from st_people sp
        left join sv_file_relationship_public_link sr on sr.res_id = sp.id and sr.res_category = :people
        and sr.relationship = :avatar
        left join st_establishment_assign sa on sa.people_id = sp.id
        left join st_establishment se on se.id = sa.establishment_id
        left join st_capacity sc on sc.id = se.capacity_id and sc.code = any(array[:capacity_code_list])
        where sp.id = :people_id
        group by sp.id, sr.public_link
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=TeacherInfoViewModel,
            params={
                "people_id": people_id,
                "people": EnumBackboneResource.PEOPLE.name,
                "capacity_code_list": [
                    EnumCapacityCode.TEACHER.name,
                    EnumCapacityCode.HEAD_TEACHER.name,
                ],
                "avatar": EnumFileRelationship.AVATAR.name,
            },
        )

    def fetch_observation_class_list(
        self, params: TeacherObservationQueryParams
    ) -> List[ObservationClassViewModel]:
        """
        获取老师观察的班级列表
        """
        sql = """
        with tree as (
        select distinct ss.dimension_dept_tree_id
        from st_observation_point_points_snapshot ss
        inner join st_observation_action sa on ss.observation_action_id = sa.id
        where ss.belongs_to_period_id = :period_id
        and ss.observation_on >= :started_on and ss.observation_on < :ended_on
        and sa.performer_res_id = :people_id and sa.performer_res_category = :people
        )
        select t.dimension_dept_tree_id, sd.name, max(sd.ceased_on)
        from tree t
        inner join st_dimension_dept_tree_history sh on sh.id = t.dimension_dept_tree_id
        inner join st_dept_history sd on sd.id = sh.dept_id
        left join sv_dept_sort ss on sd.name like '%' || ss.name || '%'
        group by t.dimension_dept_tree_id, sd.name, ss.seq
        order by ss.seq nulls last, sd.name
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=ObservationClassViewModel,
            params={
                **params.dict(),
                "people": EnumBackboneResource.PEOPLE.name,
            },
        )
