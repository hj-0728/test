from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.dimension_dept_tree import DimensionDeptTreeEntity
from infra_backbone.model.dimension_dept_tree_model import DimensionDeptTreeModel
from infra_backbone.model.view.dept_vm import DeptCategoryInfoVm


class DimensionDeptTreeRepository(BasicRepository):
    def insert_dimension_dept_tree(
        self, data: DimensionDeptTreeModel, transaction: Transaction
    ) -> str:
        """
        插入维度部门树
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DimensionDeptTreeEntity,
            entity_model=data,
            transaction=transaction,
        )

    def update_dimension_dept_tree(
        self,
        data: DimensionDeptTreeModel,
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
            entity_cls=DimensionDeptTreeEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def get_dimension_dept_tree_by_dimension_id_and_dept_name(
        self, dimension_id: str, dept_name: str
    ) -> Optional[DimensionDeptTreeModel]:
        """
        根据dimension_id、dept_name获取维度部门树
        :param dimension_id:
        :param dept_name:
        :return:
        """

        sql = """
        select sddt.* from st_dimension_dept_tree sddt 
        inner join st_dept sd on sddt.dept_id = sd.id
        where sddt.dimension_id = :dimension_id 
        and sd.name = :dept_name
        """
        return self._fetch_first_to_model(
            model_cls=DimensionDeptTreeModel,
            sql=sql,
            params={"dimension_id": dimension_id, "dept_name": dept_name},
        )

    def get_dimension_dept_tree_max_seq(self, dimension_id: str, parent_dept_id: str) -> int:
        """
        :param dimension_id:
        :param parent_dept_id:
        :return:
        """

        sql = """
        SELECT COALESCE(max(seq), 0) AS max_seq
        FROM st_dimension_dept_tree st
        WHERE st.parent_dept_id = :parent_dept_id
        AND st.dimension_id = :dimension_id
        """
        data = self._execute_sql(
            sql=sql,
            params={"dimension_id": dimension_id, "parent_dept_id": parent_dept_id},
        )
        return data[0].get("max_seq")

    def get_dimension_dept_tree_by_dimension_id_and_dept_id(
        self, dimension_id: str, dept_id: str
    ) -> Optional[DimensionDeptTreeModel]:
        """
        根据dimension_id、dept_id获取维度部门树
        :param dimension_id:
        :param dept_id:
        :return:
        """

        sql = """
        select * from st_dimension_dept_tree
        where dimension_id = :dimension_id 
        and dept_id = :dept_id
        """
        return self._fetch_first_to_model(
            model_cls=DimensionDeptTreeModel,
            sql=sql,
            params={"dimension_id": dimension_id, "dept_id": dept_id},
        )

    def get_dept_info_by_dimension_dept_tree_id(
        self, dimension_dept_tree_id: str
    ) -> Optional[DeptCategoryInfoVm]:
        """
        获取部门详情，通过 dimension_dept_tree_id
        :param dimension_dept_tree_id:
        :return:
        """

        sql = """
        select d.*,dc.code as category_code from st_dimension_dept_tree dt 
        INNER JOIN st_dept d on dt.dept_id=d.id
        INNER JOIN st_dept_dept_category_map cm on cm.dept_id=d.id
        INNER JOIN st_dept_category dc on dc.id=cm.dept_category_id
        where dt.id=:dimension_dept_tree_id
        """

        return self._fetch_first_to_model(
            model_cls=DeptCategoryInfoVm,
            sql=sql,
            params={"dimension_dept_tree_id": dimension_dept_tree_id},
        )

    def delete_dimension_dept_tree(self, tree_id: str, transaction: Transaction):
        """
        删除维度部门树
        :param tree_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=DimensionDeptTreeEntity, entity_id=tree_id, transaction=transaction
        )
