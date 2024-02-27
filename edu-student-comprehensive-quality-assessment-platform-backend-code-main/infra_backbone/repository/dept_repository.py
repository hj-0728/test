from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.dept import DeptEntity
from infra_backbone.model.dept_model import DeptModel
from infra_backbone.model.dept_tree_model import DeptTreeModel, DeptTreeNodeModel
from infra_backbone.model.params.dept_tree_query_params import DeptTreeQueryParams
from infra_backbone.model.view.dept_vm import DeptInfoVm


class DeptRepository(BasicRepository):
    def insert_dept(self, data: DeptModel, transaction: Transaction) -> str:
        """
        插入部门
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DeptEntity, entity_model=data, transaction=transaction
        )

    def get_dept_by_name(self, name: str) -> Optional[DeptModel]:
        """
        根据name获取部门
        :param name:
        :return:
        """

        sql = """select * from st_dept where name = :name"""
        return self._fetch_first_to_model(model_cls=DeptModel, sql=sql, params={"name": name})

    def get_exist_dept(
        self,
        name: str,
        parent_id: str,
        dimension_id: str,
        organization_id: str,
        dept_id: Optional[str] = None,
    ) -> Optional[DeptModel]:
        """
        获取部门
        :param dept_id:
        :param name:
        :param parent_id:
        :param dimension_id:
        :param organization_id:
        :return:
        """

        sql = """
        select sd.*
        from st_dept sd
        inner join st_dimension_dept_tree st on st.dept_id = sd.id
        where sd.name = :name
        and sd.organization_id = :organization_id
        and st.dimension_id = :dimension_id
        and st.parent_dept_id = :parent_id
        """
        if dept_id:
            sql += """
            and sd.id != :dept_id
            """
        return self._fetch_first_to_model(
            model_cls=DeptModel,
            sql=sql,
            params={
                "dept_id": dept_id,
                "name": name,
                "parent_id": parent_id,
                "dimension_id": dimension_id,
                "organization_id": organization_id,
            },
        )

    def get_all_dept(self) -> List[DeptModel]:
        """
        获取所有部门
        :return:
        """

        sql = """select * from st_dept"""
        return self._fetch_all_to_model(model_cls=DeptModel, sql=sql)

    def get_dept_tree(
        self,
        dimension_id: str,
        organization_id: str,
        search_text: Optional[str] = None,
        is_activated: Optional[bool] = None,
    ) -> List[DeptTreeNodeModel]:
        """
        根据维度id和组织id获取部门树列表
        :param dimension_id:
        :param organization_id:
        :param search_text:
        :param is_activated:
        :return:
        """
        if search_text:
            sql = """with filter_id as (
            select distinct unnest(path_list) as id
            from sv_dimension_dept_tree 
            where name like '%' || :search_text || '%'
            and organization_id = :organization_id and dimension_id = :dimension_id)
            select st.* from sv_dimension_dept_tree st
            inner join filter_id fi on fi.id = st.id
            and dimension_id = :dimension_id
            """
        else:
            sql = """
            select * from sv_dimension_dept_tree where organization_id = :organization_id 
            and dimension_id = :dimension_id
            """
        if is_activated is not None:
            sql += """ and is_activated is :is_activated"""
        sql += """ order by sort_info"""
        return self._fetch_all_to_model(
            sql=sql,
            params={
                "dimension_id": dimension_id,
                "organization_id": organization_id,
                "search_text": search_text,
                "is_activated": is_activated,
            },
            model_cls=DeptTreeNodeModel,
        )

    def get_child_dept_list(
        self, dept_id: str, organization_id: str, dimension_id: str
    ) -> List[DeptModel]:
        """
        :param dept_id:
        :param organization_id:
        :param dimension_id:
        :return:
        """
        sql = """
        SELECT st.*, sd.version
        FROM sv_dimension_dept_tree st
        inner join st_dept sd ON sd.id = st.id AND sd.organization_id = st.organization_id
        WHERE :dept_id = ANY(st.path_list)
        AND st.dimension_id = :dimension_id
        AND st.organization_id = :organization_id
        AND st.id != :dept_id
        """
        return self._fetch_all_to_model(
            model_cls=DeptModel,
            sql=sql,
            params={
                "dept_id": dept_id,
                "organization_id": organization_id,
                "dimension_id": dimension_id,
            },
        )

    def get_dept_by_tree_id(self, tree_id: str) -> Optional[DeptModel]:
        """
        根据id获取部门
        :param tree_id:
        :return:
        """

        sql = """select sd.*
        from st_dept sd
        inner join st_dimension_dept_tree st on st.dept_id = sd.id
        where st.id = :tree_id"""
        return self._fetch_first_to_model(model_cls=DeptModel, sql=sql, params={"tree_id": tree_id})

    def update_dept(
        self,
        data: DeptModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新部门
        :param data:
        :param transaction:
        :param limited_col_list:
        :return:
        """

        return self._update_versioned_entity_by_model(
            entity_cls=DeptEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def get_dept_info(
        self, dimension_dept_tree_id: str, organization_id: str
    ) -> Optional[DeptInfoVm]:
        """
        根据id获取部门
        :param dimension_dept_tree_id:
        :param organization_id:
        :return:
        """

        sql = """
        WITH not_available_count AS (
        SELECT COUNT((st2.is_activated IS FALSE) OR NULL) AS parent_not_available_count
        FROM sv_dimension_dept_tree st
        INNER JOIN sv_dimension_dept_tree st2 ON st2.id = ANY(st.path_list)
        INNER JOIN st_dept sd ON st2.id = sd.id
        WHERE st.dimension_dept_tree_id = :dimension_dept_tree_id
        AND st2.dimension_id = st.dimension_id
        AND st2.level < st.level
        AND st2.organization_id = :organization_id
        )
        SELECT nc.*, st.*
        FROM sv_dimension_dept_tree st
        INNER JOIN st_dept sd ON st.id = sd.id
        CROSS JOIN not_available_count nc
        WHERE st.dimension_dept_tree_id = :dimension_dept_tree_id
        AND sd.organization_id = :organization_id
        """
        return self._fetch_first_to_model(
            model_cls=DeptInfoVm,
            sql=sql,
            params={
                "dimension_dept_tree_id": dimension_dept_tree_id,
                "organization_id": organization_id,
            },
        )

    def get_dept_tree_list(self, params: DeptTreeQueryParams) -> List[DeptTreeModel]:
        """
        获取部门树
        :return:
        """

        sql = """
        WITH RECURSIVE dept_tree AS (
        SELECT sdt.id AS dimension_dept_tree_id, sd.id, sd.id AS key,sd.name,
        sd2.name AS parent_name,
        sdt.parent_dept_id AS parent_id,
        ARRAY[sdt.seq] AS seq_list,1 AS level,ARRAY[sdt.id::character varying] AS path_list,
        sdt.seq, sc.code AS dept_category_code
        FROM cv_dimension_dept_tree sdt
        INNER JOIN cv_dept sd ON sd.id = sdt.dept_id
        INNER JOIN st_dimension sdn ON sdn.id = sdt.dimension_id
        left join st_dept sd2 on sd2.id = sdt.parent_dept_id
        LEFT JOIN st_dept_dept_category_map sm ON sm.dept_id = sd.id
        LEFT JOIN st_dept_category sc ON sc.id = sm.dept_category_id
        WHERE sdt.parent_dept_id IS NULL AND sdn.id = :dimension_id
        UNION ALL
        SELECT sdt.id AS dimension_dept_tree_id, sd.id, sd.id AS key, sd.name,
        sd2.name AS parent_name,
        sdt.parent_dept_id AS parent_id,
        array_append(t.seq_list, sdt.seq) AS seq_list,t.level + 1 AS level,
        array_append(t.path_list, sdt.id) AS path_list, sdt.seq,
        sc.code AS dept_category_code
        FROM cv_dimension_dept_tree sdt
        INNER JOIN cv_dept sd ON sd.id = sdt.dept_id
        left join st_dept sd2 on sd2.id = sdt.parent_dept_id
        INNER JOIN st_dimension sdn ON sdn.id = sdt.dimension_id
        JOIN dept_tree t ON t.id = sdt.parent_dept_id
        LEFT JOIN st_dept_dept_category_map sm ON sm.dept_id = sd.id
        LEFT JOIN st_dept_category sc ON sc.id = sm.dept_category_id
        )
        """

        if params.get_duty_teacher_dept:
            sql += """
            , duty_dept AS (
            SELECT DISTINCT UNNEST(dt.path_list) AS dimension_dept_tree_id
            FROM cv_establishment e
            INNER JOIN cv_establishment_assign ea ON e.id = ea.establishment_id
            INNER JOIN st_people_user spu ON spu.people_id = ea.people_id
            INNER JOIN st_capacity c ON c.id = e.capacity_id
            INNER JOIN dept_tree dt ON e.dimension_dept_tree_id = ANY(dt.path_list)
            WHERE spu.user_id = :user_id
            AND (c.code = 'TEACHER' or c.code='HEAD_TEACHER')
            )
            """

        sql += """
        SELECT dt.* 
        FROM dept_tree dt
        """

        if params.get_duty_teacher_dept:
            sql += """
            INNER JOIN duty_dept dd ON dd.dimension_dept_tree_id = dt.dimension_dept_tree_id
            """

        return self._fetch_all_to_model(
            model_cls=DeptTreeModel,
            sql=sql,
            params={
                "dimension_id": params.dimension_id,
                "user_id": params.user_id,
            },
        )

    def get_current_dept_by_ids(self, dept_ids: List[str]) -> List[DeptModel]:
        """
        获取未删除的部门根据部门ids
        :param dept_ids:
        :return:
        """

        sql = """
        select distinct * from st_dept 
        where id=any(array[:dept_ids]) and ended_on>now()
        """

        return self._fetch_all_to_model(
            model_cls=DeptModel,
            sql=sql,
            params={
                "dept_ids": dept_ids,
            },
        )

    def delete_dept_by_id(self, dept_id: str, transaction: Transaction):
        """
        删除部门
        :param dept_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=DeptEntity, entity_id=dept_id, transaction=transaction
        )
