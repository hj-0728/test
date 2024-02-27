from typing import List

from infra_basic.basic_repository import BasicRepository

from infra_backbone.model.establishment_assignment_model import EstablishmentAssignmentModel

DEPT_PEOPLE = """
RECURSIVE dept_tree AS(
SELECT sd.id as dept_id, sd.name as dept_name, dt.id as dimension_dept_tree_id 
FROM cv_dept sd
INNER JOIN cv_dimension_dept_tree dt on sd.id = dt.dept_id
INNER JOIN (SELECT UNNEST(ARRAY[:dept_id_list]) as dept_id) dl on dl.dept_id = sd.id
UNION
SELECT child.id as dept_id, child.name as dept_name, dt.id as dimension_dept_tree_id 
FROM cv_dept child
INNER JOIN cv_dimension_dept_tree dt on child.id = dt.dept_id
INNER JOIN dept_tree parent ON parent.dept_id=dt.parent_dept_id
), dept_people as (
SELECT ea.* FROM dept_tree dt
INNER JOIN sv_current_establishment_assign ea on ea.dimension_dept_tree_id = dt.dimension_dept_tree_id
INNER JOIN st_people sp on ea.people_id = sp.id
WHERE ea.capacity_code = 'STUDENT'
)
"""
PERSONAL = """
personal as (
SELECT ea.* 
FROM sv_current_establishment_assign ea
INNER JOIN (SELECT UNNEST(ARRAY[:personal_id_list]) as establishment_assign_id) pl 
on pl.establishment_assign_id = ea.id 
WHERE ea.capacity_code = 'STUDENT'
)
"""


class AppEstablishmentAssignmentRepository(BasicRepository):
    """
    编制分配 repository
    """

    def get_establishment_assignment_list_by_plan_scope(
        self,
        evaluation_object_category: str,
        dept_id_list: List[str],
        personal_id_list: List[str],
    ):
        """
        根据评价标准计划适用的集合获取编制分配信息
        :param evaluation_object_category:
        :param dept_id_list:
        :param personal_id_list:
        :return:
        """
        if len(dept_id_list) == 0 and len(personal_id_list) > 0:
            sql = f"""
            with { PERSONAL } SELECT * FROM personal
            """
        elif len(dept_id_list) > 0 and len(personal_id_list) == 0:
            sql = f"""
            with { DEPT_PEOPLE } SELECT * FROM dept_people
            """
        else:
            sql = f"""
            with {DEPT_PEOPLE}, {PERSONAL}
            SELECT * FROM dept_people
            UNION
            SELECT * FROM personal
            """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=EstablishmentAssignmentModel,
            params={
                "evaluation_object_category": evaluation_object_category,
                "dept_id_list": dept_id_list,
                "personal_id_list": personal_id_list,
            },
        )
