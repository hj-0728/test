from typing import List

from infra_basic.basic_repository import BasicRepository

from biz_comprehensive.model.view.student_info_vm import StudentInfoViewModel
from infra_backbone.data.enum import EnumBackboneResource, EnumFileRelationship
from infra_backbone.model.capacity_model import EnumCapacityCode


class ParentRepository(BasicRepository):
    def fetch_child_list(self, parent_people_id: str) -> List[StudentInfoViewModel]:
        """
        获取孩子列表
        """
        sql = """
        select sl.public_link as avatar, sa.id as establishment_assign_id, sp.id, sp.name, st.name as dept_name
        from st_people_relationship sr
        inner join st_people sp on sp.id = sr.object_people_id
        inner join sv_file_relationship_public_link sl on sl.res_id = sp.id and sl.res_category = :people
        and sl.relationship = :avatar
        inner join st_establishment_assign sa on sa.people_id = sp.id
        inner join st_establishment se on se.id = sa.establishment_id
        inner join st_capacity sc on sc.id =  se.capacity_id and sc.code = :student
        inner join sv_k12_dept_tree st on st.dimension_dept_tree_id =  se.dimension_dept_tree_id
        where subject_people_id = :parent_people_id
        order by sp.name
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=StudentInfoViewModel,
            params={
                "parent_people_id": parent_people_id,
                "people": EnumBackboneResource.PEOPLE.name,
                "avatar": EnumFileRelationship.AVATAR.name,
                "student": EnumCapacityCode.STUDENT.name,
            },
        )
