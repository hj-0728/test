"""
上下文部门关联 repository
"""
from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from context_sync.entity.context_dept_map import ContextDeptMapEntity
from context_sync.model.context_dept_map_model import (
    ContextDeptMapModel,
    EnumContextDeptMapResCategory,
)
from context_sync.model.view.context_dept_detail_vm import ContextDeptDetailViewModel
from infra_backbone.data.enum import EnumBackboneResource
from infra_backbone.model.dept_category_model import EnumDeptCategoryCode
from infra_backbone.model.dept_model import DeptModel
from infra_backbone.model.dimension_model import EnumDimensionCategory, EnumDimensionCode


class ContextDeptMapRepository(BasicRepository):
    """
    上下文部门关联 repository
    """

    def insert_context_dept_map(
        self,
        context_dept_map: ContextDeptMapModel,
        transaction: Transaction,
    ) -> str:
        """
        添加上下文部门关联
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=ContextDeptMapEntity, entity_model=context_dept_map, transaction=transaction
        )

    def delete_context_dept_map(self, context_dept_map_id: str, transaction: Transaction):
        """
        根据id删除context_dept_map
        """
        return self._delete_versioned_entity_by_id(
            entity_cls=ContextDeptMapEntity,
            entity_id=context_dept_map_id,
            transaction=transaction,
        )

    def get_context_k12_dept_detail_by_res_category(
        self, dingtalk_corp_id: str
    ) -> List[ContextDeptDetailViewModel]:
        """
        根据类型获取上下文部门关联
        :param dingtalk_corp_id:
        :return:
        """

        sql = """
        with dept as (
        select dm.*,d.version as dept_version,d.name,d.comments,
        dt.parent_dept_id,dt.id as dimension_dept_tree_id,
        dt.version as dimension_dept_tree_version,
        di.organization_id,dc.code as category_code
        from st_context_dept_map dm 
        inner join st_dept d on d.id=dm.dept_id
        inner join st_dimension_dept_tree dt on dt.dept_id=d.id
        inner join st_dimension di on di.id=dt.dimension_id
        left join st_dept_dept_category_map cm on cm.dept_id=d.id 
        left join st_dept_category dc on dc.id=cm.dept_category_id
        where di.category=:edu and dm.res_category=:res_category
        ),
        result as (
        select id,dept_version,dept_id,res_id as res_dept_id,name,comments,
        dimension_dept_tree_id, parent_dept_id,organization_id,
        array_agg(category_code) as category_code_list,dimension_dept_tree_version
        from dept
        group by id,dept_id,res_id,dept_version,name,comments,dimension_dept_tree_id,
        parent_dept_id,organization_id,dimension_dept_tree_version
        )
        select  id,dept_version,dept_id,res_dept_id,name,comments,
        dimension_dept_tree_id, parent_dept_id, organization_id,
        array_remove(category_code_list, NULL) AS category_code_list,dimension_dept_tree_version
        from result
        """

        return self._fetch_all_to_model(
            model_cls=ContextDeptDetailViewModel,
            sql=sql,
            params={
                "res_category": EnumContextDeptMapResCategory.DINGTALK_K12_DEPT.name,
                "edu": EnumDimensionCategory.EDU.name,
                "dingtalk_corp_id": dingtalk_corp_id,
            },
        )

    def get_context_dept_detail_by_res_category(
        self, dingtalk_corp_id: str
    ) -> List[ContextDeptDetailViewModel]:
        """
        根据类型获取上下文部门关联
        :param dingtalk_corp_id:
        :return:
        """

        sql = """
        with dept as (
        select dm.*,d.version as dept_version,d.name,d.comments,
        dt.parent_dept_id,dt.id as dimension_dept_tree_id,
        dt.version as dimension_dept_tree_version,
        di.organization_id,dc.code as category_code
        FROM st_context_dept_map dm 
        inner join st_dingtalk_dept kd on kd.id=dm.res_id
        INNER JOIN st_dept d on d.id=dm.dept_id
        INNER JOIN st_dimension_dept_tree dt on dt.dept_id=d.id
        INNER JOIN st_dimension di on di.id=dt.dimension_id
        LEFT JOIN st_dept_dept_category_map cm on cm.dept_id=d.id 
        left join st_dept_category dc on dc.id=cm.dept_category_id
        where di.code=:dimension_code and kd.dingtalk_corp_id=:dingtalk_corp_id
        and dm.res_category=:res_category
        )
        select id,dept_version,dept_id,res_id as res_dept_id,name,comments,
        dimension_dept_tree_id,parent_dept_id,organization_id,
        array_agg(category_code)::text[] as category_code_list,dimension_dept_tree_version
        from dept
        GROUP BY id,dept_id,res_id,dept_version,name,comments,dimension_dept_tree_id,
        parent_dept_id,organization_id,dimension_dept_tree_version
        """

        return self._fetch_all_to_model(
            model_cls=ContextDeptDetailViewModel,
            sql=sql,
            params={
                "res_category": EnumContextDeptMapResCategory.DINGTALK_DEPT.name,
                "dingtalk_corp_id": dingtalk_corp_id,
                "dimension_code": EnumDimensionCode.INNER.name,
            },
        )

    def get_no_avatar_class_list(self) -> List[DeptModel]:
        sql = """
        select sd.*
        from st_dept sd
        inner join st_dept_dept_category_map sm on sm.dept_id = sd.id
        inner join st_dept_category sc on sc.id = sm.dept_category_id
        and sc.code = :class
        left join st_file_relationship sr on sr.res_category = :dept and sr.res_id = sd.id
        where sr.file_id is null
        group by sd.id
        """
        return self._fetch_all_to_model(
            model_cls=DeptModel,
            sql=sql,
            params={
                "class": EnumDeptCategoryCode.CLASS.name,
                "dept": EnumBackboneResource.DEPT.name,
            },
        )
