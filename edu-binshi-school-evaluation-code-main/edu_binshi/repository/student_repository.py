from typing import List, Tuple

from infra_basic.basic_repository import BasicRepository
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import OrderCondition, PageInitParams

from edu_binshi.data.query_params.student_query_params import StudentPageQueryParams
from edu_binshi.model.view.parent_vm import ParentVm
from edu_binshi.model.view.student_page_vm import StudentPageVm
from edu_binshi.model.view.student_user_page_vm import StudentUserPageVm
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.model.contact_info_model import EnumContactInfoCategory
from infra_backbone.model.resource_contact_info_model import EnumContactInfoResourceCategory
from infra_backbone.model.role_model import EnumRoleCode


class StudentRepository(BasicRepository):
    """
    学生 repository
    """

    @staticmethod
    def __get_student_sql(params: StudentPageQueryParams) -> Tuple[str, dict]:
        """
        获取学生 sql
        :param params:
        :return:
        """

        sql = """
        WITH RECURSIVE dept_tree AS (
        SELECT sdt.id AS dimension_dept_tree_id, sd.id, sd.id AS key, sd.name, NULL AS parent_dimension_dept_tree_id, 
        sdt.parent_dept_id AS parent_id, NULL AS parent_name, ARRAY[sdt.seq] AS seq_list,1 AS level,
        ARRAY[sd.id::character varying] AS path_list, sdt.seq, 
        ARRAY[sdt.id::character varying] AS dimension_dept_tree_id_path_list
        FROM cv_dimension_dept_tree sdt
        INNER JOIN cv_dept sd ON sd.id = sdt.dept_id
        INNER JOIN st_dimension sdn ON sdn.id = sdt.dimension_id
        WHERE sdt.parent_dept_id IS NULL AND sdn.id = :dimension_id
        UNION ALL
        SELECT sdt.id AS dimension_dept_tree_id, sd.id, sd.id AS key, sd.name,
        t.dimension_dept_tree_id::TEXT AS parent_dimension_dept_tree_id, sdt.parent_dept_id AS parent_id, 
        t.name::TEXT AS parent_name, 
        array_append(t.seq_list, sdt.seq) AS seq_list,t.level + 1 AS level,
        array_append(t.path_list, sd.id) AS path_list, sdt.seq, 
        array_append(t.dimension_dept_tree_id_path_list, sdt.id) AS dimension_dept_tree_id_path_list
        FROM cv_dimension_dept_tree sdt
        INNER JOIN cv_dept sd ON sd.id = sdt.dept_id
        INNER JOIN st_dimension sdn ON sdn.id = sdt.dimension_id
        JOIN dept_tree t ON t.id = sdt.parent_dept_id
        )
        """

        if params.get_duty_teacher_dept:
            sql += """
            , duty_dept AS (
            SELECT DISTINCT UNNEST(dt.dimension_dept_tree_id_path_list) AS dimension_dept_tree_id
            FROM cv_establishment e
            INNER JOIN cv_establishment_assign ea ON e.id = ea.establishment_id
            INNER JOIN st_people_user spu ON spu.people_id = ea.people_id
            INNER JOIN st_capacity c ON c.id = e.capacity_id
            INNER JOIN dept_tree dt ON e.dimension_dept_tree_id = ANY(dt.dimension_dept_tree_id_path_list)
            WHERE spu.user_id = :user_id
            AND (c.code = 'TEACHER' or c.code='HEAD_TEACHER')
            )
            """

        sql += """
        , dept_list AS (
        SELECT DISTINCT dt.*
        FROM dept_tree dt
        """

        if params.get_duty_teacher_dept:
            sql += """
            INNER JOIN duty_dept dd ON dd.dimension_dept_tree_id = dt.dimension_dept_tree_id
            """

        if params.dimension_dept_tree_id:
            sql += """
            WHERE :dimension_dept_tree_id = ANY(dt.dimension_dept_tree_id_path_list)
            """

        sql += """
        )
        , student as (
        SELECT DISTINCT sp.id AS people_id, ea.id AS establishment_assign_id, 
        dl.name AS school_class, sp.name AS student_name,
        dl.parent_name AS grade, seq_list FROM cv_establishment_assign ea
        INNER JOIN cv_establishment se ON se.id = ea.establishment_id
        INNER JOIN st_capacity sc ON sc.id = se.capacity_id AND sc.code = :STUDENT
        INNER JOIN cv_dimension_dept_tree dt ON dt.id = se.dimension_dept_tree_id
        INNER JOIN cv_dept sd ON sd.id = dt.dept_id
        INNER JOIN st_people sp ON sp.id = ea.people_id and sp.is_available is true
        INNER JOIN dept_list dl ON dl.dimension_dept_tree_id = se.dimension_dept_tree_id
        )
        """

        sql_params = {
            "dimension_dept_tree_id": params.dimension_dept_tree_id,
            "user_id": params.user_id,
            "dimension_id": params.dimension_id,
            "STUDENT": EnumCapacityCode.STUDENT.name,
        }

        return sql, sql_params

    def get_student_page(
        self,
        params: StudentPageQueryParams,
    ) -> PaginationCarrier[StudentPageVm]:
        """
        获取学生 分页
        :param params:
        :return:
        """

        sql, sql_params = self.__get_student_sql(params=params)

        sql += " select * from student "

        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["student_name"],
            order_columns=[
                OrderCondition(column_name="student_name", order="asc"),
            ],
            params=sql_params,
        )
        return self._paginate(
            result_type=StudentPageVm,
            total_params=page_init_params,
            page_params=params,
        )

    def get_student_info_list_by_establishment_assign_id_list(
        self,
        establishment_assign_id_list: List[str],
        dimension_id: str,
    ) -> List[StudentPageVm]:
        """
        根据编制分配id列表获取学生信息
        :param establishment_assign_id_list:
        :param dimension_id:
        :return:
        """
        sql = """
        WITH RECURSIVE dept_tree AS (
        SELECT sdt.id AS dimension_dept_tree_id, sd.id, sd.id AS key, sd.name, NULL AS parent_dimension_dept_tree_id, 
        sdt.parent_dept_id AS parent_id, NULL AS parent_name, ARRAY[sdt.seq] AS seq_list,1 AS level,
        ARRAY[sd.id::character varying] AS path_list, sdt.seq, 
        ARRAY[sdt.id::character varying] AS dimension_dept_tree_id_path_list
        FROM st_dimension_dept_tree sdt
        INNER JOIN st_dept sd ON sd.id = sdt.dept_id
        INNER JOIN st_dimension sdn ON sdn.id = sdt.dimension_id
        WHERE sdt.parent_dept_id IS NULL AND sdn.id = :dimension_id
        UNION ALL
        SELECT sdt.id AS dimension_dept_tree_id, sd.id, sd.id AS key, sd.name,
        t.dimension_dept_tree_id::TEXT AS parent_dimension_dept_tree_id, sdt.parent_dept_id AS parent_id, 
        t.name::TEXT AS parent_name, 
        array_append(t.seq_list, sdt.seq) AS seq_list,t.level + 1 AS level,
        array_append(t.path_list, sd.id) AS path_list, sdt.seq, 
        array_append(t.dimension_dept_tree_id_path_list, sdt.id) AS dimension_dept_tree_id_path_list
        FROM st_dimension_dept_tree sdt
        INNER JOIN st_dept sd ON sd.id = sdt.dept_id
        INNER JOIN st_dimension sdn ON sdn.id = sdt.dimension_id
        JOIN dept_tree t ON t.id = sdt.parent_dept_id
        ), dept_list AS (
        SELECT DISTINCT dt.*
        FROM dept_tree dt
        )
        SELECT ea.id AS establishment_assign_id, sp.id AS people_id, dl.name AS school_class,
        sp.name AS student_name, dl.parent_name AS grade
        FROM st_establishment_assign ea 
        INNER JOIN st_establishment se ON se.id = ea.establishment_id
        INNER JOIN st_capacity sc ON sc.id = se.capacity_id AND sc.code = :STUDENT
        INNER JOIN st_dimension_dept_tree dt ON dt.id = se.dimension_dept_tree_id
        INNER JOIN dept_list dl ON dl.dimension_dept_tree_id = se.dimension_dept_tree_id
        INNER JOIN st_people sp ON sp.id = ea.people_id
        WHERE ea.id = ANY(:establishment_assign_id_list) 
        """

        return self._fetch_all_to_model(
            model_cls=StudentPageVm,
            sql=sql,
            params={
                "STUDENT": EnumCapacityCode.STUDENT.name,
                "dimension_id": dimension_id,
                "establishment_assign_id_list": establishment_assign_id_list,
            },
        )

    def get_student_parent(self, people_id: str) -> List[ParentVm]:
        """
        获取学生家长信息
        :param people_id:
        :return:
        """
        sql = """
        select p.*,ci.detail as phone_detail 
        from st_people_relationship pr
        INNER JOIN st_people p on pr.object_people_id=p.id
        LEFT JOIN st_resource_contact_info rci on rci.resource_id=p.id 
        and rci.resource_category=:resource_category
        LEFT JOIN st_contact_info ci on ci.id=rci.contact_info_id and category=:category
        where subject_people_id=:people_id
        """

        return self._fetch_all_to_model(
            model_cls=ParentVm,
            sql=sql,
            params={
                "people_id": people_id,
                "category": EnumContactInfoCategory.PHONE.name,
                "resource_category": EnumContactInfoResourceCategory.PEOPLE.name,
            },
        )

    def get_student_user_page(
        self, params: StudentPageQueryParams
    ) -> PaginationCarrier[StudentUserPageVm]:
        """
        获取学生用户 分页
        :param params:
        :return:
        """

        sql, sql_params = self.__get_student_sql(params=params)

        sql += """
        ,result as (
        select people_id, student_name, string_agg(grade, '；') as grade,
        string_agg(grade || '/' ||school_class, '；') as school_class,
        array_agg(seq_list) as seq_list from student
        GROUP BY people_id, student_name
         )
        select s.*,row_to_json(u.*) as user from result s
        LEFT JOIN (select u.*,pu.people_id from st_people_user pu
        INNER JOIN st_user u on u.id=pu.user_id
        inner join st_user_role sur on sur.user_id = u.id
        inner join st_role sr on sr.id = sur.role_id
        and sr.code = :student_role
        ) u on u.people_id=s.people_id
        order by seq_list, student_name
        """

        sql_params["student_role"] = EnumRoleCode.STUDENT.name
        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["student_name"],
            params=sql_params,
        )
        return self._paginate(
            result_type=StudentUserPageVm,
            total_params=page_init_params,
            page_params=params,
        )
