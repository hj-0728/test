"""
k12部门 repository
"""
from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_dingtalk.entity.dingtalk_k12_dept import DingtalkK12DeptEntity
from infra_dingtalk.model.dingtalk_k12_dept_model import (
    DingtalkK12DeptModel,
    EnumDingtalkK12DeptCategory,
)
from infra_dingtalk.model.view.dingtalk_k12_dept_vm import DingtalkK12DeptListVm
from infra_dingtalk.model.view.dingtalk_k12_dept_with_admins_vm import (
    DingtalkK12DeptWithAdminsViewModel,
)


class DingtalkK12DeptRepository(BasicRepository):
    """
    k12部门 repository
    """

    def get_dingtalk_k12_dept_tree_list_parent_id(
        self,
        parent_id: str = None,
    ) -> Optional[List[DingtalkK12DeptListVm]]:
        """
        获取k12部门列表
        """
        sql = """
        WITH RECURSIVE dept_tree(id,name,parent_id,level,seq,sort_info,parent_list,category) AS(
        SELECT id,name,parent_dingtalk_k12_dept_id AS parent_id,1 as level ,swkd.seq,
        ARRAY[swkd.seq] AS sort_info,
        ARRAY[swkd.id]::text[] AS parent_list,
        swkd.category
        FROM st_dingtalk_k12_dept swkd
        """
        if parent_id is None:
            sql += """
            WHERE swkd.parent_dingtalk_k12_dept_id IS NULL
            """
        else:
            sql += """
            WHERE swkd.parent_dingtalk_k12_dept_id=:parent_id
            """
        sql += """
        UNION
        SELECT child.id,child.name,child.parent_dingtalk_k12_dept_id AS parent_id,parent.level+1 as level,child.seq,
        array_append(parent.sort_info, child.seq) AS sort_info,
        array_append(parent.parent_list, child.id::text) AS parent_list,
        child.category
        FROM st_dingtalk_k12_dept child
        INNER JOIN dept_tree parent ON parent.id=child.parent_dingtalk_k12_dept_id)
        SELECT * FROM dept_tree dt
        ORDER BY dt.sort_info
        """
        return self._fetch_all_to_model(
            model_cls=DingtalkK12DeptListVm,
            sql=sql,
            params={
                "parent_id": parent_id,
            },
        )

    def fetch_dingtalk_k12_dept_with_admins(
        self,
        dingtalk_corp_id: str,
    ) -> List[DingtalkK12DeptWithAdminsViewModel]:
        """
        获取k12的部门及负责人
        """

        sql = """with dept as (
        select skd.*, skd2.remote_dept_id as parent_remote_dept_id
        from st_dingtalk_k12_dept skd
        left join st_dingtalk_k12_dept skd2 on skd.parent_dingtalk_k12_dept_id = skd2.id
        where skd.dingtalk_corp_id = :dingtalk_corp_id
        ),
        dept_user as (
        select d.id,array_agg(json_build_object('id', sud.id, 'version', sud."version",
        'duty', sud.duty, 'subject', sud.subject,'dingtalk_user_id', sud.dingtalk_user_id,
        'dingtalk_k12_dept_id', sud.dingtalk_k12_dept_id,
        'remote_user_id', su.remote_user_id)) as admins  from dept d
        inner join st_dingtalk_user_k12_dept_duty sud on sud.dingtalk_k12_dept_id = d.id
        inner join st_dingtalk_user su on su.id = sud.dingtalk_user_id
        group by d.id
        )
        select d.*, coalesce(du.admins, array[]::json[]) as admins
        from dept d left join dept_user du on d.id = du.id"""
        return self._fetch_all_to_model(
            model_cls=DingtalkK12DeptWithAdminsViewModel,
            sql=sql,
            params={"dingtalk_corp_id": dingtalk_corp_id},
        )

    def insert_dingtalk_k12_dept(self, dept: DingtalkK12DeptModel, transaction: Transaction) -> str:
        """
        插入钉钉k12部门
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=DingtalkK12DeptEntity, entity_model=dept, transaction=transaction
        )

    def update_dingtalk_k12_dept(self, dept: DingtalkK12DeptModel, transaction: Transaction):
        """
        更新钉钉k12部门
        """
        self._update_versioned_entity_by_model(
            entity_cls=DingtalkK12DeptEntity, update_model=dept, transaction=transaction
        )

    def delete_dingtalk_k12_dept(self, dept_id: str, transaction: Transaction):
        """
        删除钉钉k12部门
        """
        self._delete_versioned_entity_by_id(
            entity_cls=DingtalkK12DeptEntity,
            entity_id=dept_id,
            transaction=transaction,
        )

    def get_max_level_managed_k12_dept_by_dingtalk_user_id(
        self, dingtalk_user_id: str
    ) -> Optional[DingtalkK12DeptModel]:
        """
        获取管理的k12部门
        :param dingtalk_user_id:
        :return:
        """
        sql = """
        select wkd.*,
        case when wkd.category = :school_class then 3 
        when wkd.category = :campus then 1 else 2 end as level,
        1 as seq
        from st_dingtalk_k12_dept wkd
        inner join st_dingtalk_user_k12_dept_duty swukdd on wkd.id = swukdd.dingtalk_k12_dept_id
        where swukdd.dingtalk_user_id = :dingtalk_user_id
        order by level
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=DingtalkK12DeptModel,
            params={
                "dingtalk_user_id": dingtalk_user_id,
                "school_class": EnumDingtalkK12DeptCategory.SCHOOL_CLASS.name,
                "campus": EnumDingtalkK12DeptCategory.CAMPUS.name,
            },
        )

    def get_dingtalk_k12_dept_tree(self, period_id: str, dingtalk_user_id: str, get_all: bool):
        """
        获取k12部门树
        """
        sql = """
        with class_dept as (
        select wkd.id, wkd.name, wkd.parent_dingtalk_k12_dept_id as parent_id, 2 as level,  wkd.category,
        ARRAY[wkd2.id, wkd.id]::text[] as parent_list,
        ARRAY[wkd2.name, wkd.name] as parent_name_list,
        case when ds.seq is null then 1000 else ds.seq end as seq, ss.id as scope_id
        from st_dingtalk_k12_dept wkd
        join st_dingtalk_k12_dept wkd2 on wkd.parent_dingtalk_k12_dept_id = wkd2.id
        join st_scope ss on wkd.id = ss.resource_id and ss.resource_category = 'dingtalk_K12_DEPT'
        """

        if not get_all:
            sql += """
            join st_dingtalk_user_k12_dept_duty  wukdd on (wukdd.duty = 'HEAD_TEACHER' or wukdd.duty = 'TEACHER')
            AND wukdd.dingtalk_k12_dept_id = wkd.id
            """

        sql += """
        left join st_dingtalk_k12_dept_seq ds on wkd.name like '%'||ds.name||'%' and ds.category = wkd.category
        where ss.period_id = :period_id and wkd.category = 'SCHOOL_CLASS'
        """

        if not get_all:
            sql += """
            AND wukdd.dingtalk_user_id = :dingtalk_user_id
            """

        sql += """
        ), result as (
        select * from class_dept cd 
        union ALL
        select wkd.id, wkd.name, 'root'  as parent_id, 1 as level, wkd.category,
        ARRAY[wkd.id]::text[] as parent_list,
        ARRAY[wkd.name]::text[] as parent_name_list,
        ds.seq, NULL AS scope_id
        from st_dingtalk_k12_dept wkd
        join class_dept cd on wkd.id = cd.parent_id
        left join st_dingtalk_k12_dept_seq ds on wkd.name like '%'||ds.name||'%' and ds.category = wkd.category
        )
        SELECT distinct *,id as key from result r order by level,seq, name
        """
        return self._fetch_all_to_model(
            model_cls=DingtalkK12DeptListVm,
            sql=sql,
            params={
                "period_id": period_id,
                "dingtalk_user_id": dingtalk_user_id,
            },
        )

    def get_root_dingtalk_k12_dept(self):
        """

        :return:
        """

        sql = """
        select * from st_dingtalk_k12_dept where category=:category
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=DingtalkK12DeptModel,
            params={
                "category": EnumDingtalkK12DeptCategory.ROOT.name,
            },
        )

    def get_dingtalk_k12_dept_by_corp_id(self, dingtalk_corp_id: str) -> List[DingtalkK12DeptModel]:
        """
        获取所有的钉钉k12部门
        :param dingtalk_corp_id:
        :return:
        """

        sql = """
        select * from st_dingtalk_k12_dept where dingtalk_corp_id=:dingtalk_corp_id
        """

        return self._fetch_all_to_model(
            model_cls=DingtalkK12DeptModel, sql=sql, params={"dingtalk_corp_id": dingtalk_corp_id}
        )
