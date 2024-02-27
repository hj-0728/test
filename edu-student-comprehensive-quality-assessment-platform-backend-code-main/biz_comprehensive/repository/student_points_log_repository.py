from typing import List

from infra_basic.basic_repository import BasicRepository

from biz_comprehensive.model.points_log_model import (
    EnumPointsLogOwnerResCategory,
    EnumPointsLogStatus,
)
from biz_comprehensive.model.symbol_model import EnumSymbolCode
from biz_comprehensive.model.view.class_student_vm import ClassStudentViewModel
from infra_backbone.data.enum import EnumBackboneResource, EnumFileRelationship
from infra_backbone.model.capacity_model import EnumCapacityCode


class StudentPointsLogRepository(BasicRepository):
    def fetch_class_student_with_points(
        self, tree_id: str, period_id: str
    ) -> List[ClassStudentViewModel]:
        """
        获取班级学生列表
        :param tree_id:
        :param period_id:
        :return:
        """
        sql = """
        with people as (
        select sa.id, sa.id as establishment_assign_id, sp.name, sr.public_link as avatar
        from st_establishment se
        inner join st_capacity sc on sc.id = se.capacity_id and sc.code = :student
        inner join st_establishment_assign sa on sa.establishment_id = se.id
        inner join st_people sp on sp.id = sa.people_id
        inner join sv_file_relationship_public_link sr on sr.res_id = sp.id and sr.res_category = :people
        and sr.relationship = :avatar
        where se.dimension_dept_tree_id = :tree_id
        ),
        points as (
        select * from (
        select p.id, balanced_addition, balanced_subtraction ,
        rank() over (partition by sl.owner_res_id order by sl.handled_on desc) as seq
        from people p
        inner join st_points_log sl on sl.owner_res_category = :establishment_assign
        and sl.owner_res_id = p.establishment_assign_id
        and sl.status = :confirmed and sl.belongs_to_period_id = :period_id
        inner join st_symbol ss on ss.id = sl.symbol_id and ss.code = :symbol_code
        ) aa where seq = 1
        )
        select p1.*, coalesce(p2.balanced_addition, 0) as balanced_addition,
        coalesce(p2.balanced_subtraction, 0) as balanced_subtraction
        from people p1
        left join points p2 on p1.id = p2.id
        order by balanced_addition + balanced_subtraction desc nulls last, name
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=ClassStudentViewModel,
            params={
                "tree_id": tree_id,
                "confirmed": EnumPointsLogStatus.CONFIRMED.name,
                "student": EnumCapacityCode.STUDENT.name,
                "symbol_code": EnumSymbolCode.POINTS.name,
                "establishment_assign": EnumPointsLogOwnerResCategory.ESTABLISHMENT_ASSIGN.name,
                "people": EnumBackboneResource.PEOPLE.name,
                "period_id": period_id,
                "avatar": EnumFileRelationship.AVATAR.name,
            },
        )
