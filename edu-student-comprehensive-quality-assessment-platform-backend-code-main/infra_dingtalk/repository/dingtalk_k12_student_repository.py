"""
k12学生
"""

from typing import List

from infra_basic.basic_repository import (
    BasicRepository,
    OrderCondition,
    PageInitParams,
    PaginationCarrier,
)
from infra_basic.transaction import Transaction

from infra_backbone.model.role_model import EnumRoleCode
from infra_dingtalk.data.query_params.dingtalk_k12_student_query_params import (
    DingtalkK12StudentQueryParams,
)
from infra_dingtalk.entity.dingtalk_k12_student import DingtalkK12StudentEntity
from infra_dingtalk.model.dingtalk_k12_dept_model import EnumDingtalkK12DeptCategory
from infra_dingtalk.model.dingtalk_k12_student_model import (
    DingtalkK12StudentModel,
    DingtalkK12StudentViewModel,
)
from infra_dingtalk.model.dingtalk_user_k12_dept_duty_model import EnumDingtalkUserK12DeptDutyMap
from infra_dingtalk.model.view.dingtalk_k12_student_detail_vm import (
    DingtalkK12StudentDetailViewModel,
)
from infra_dingtalk.model.view.dingtalk_k12_student_info_vm import DingtalkK12StudentInfoViewModel


class DingtalkK12StudentRepository(BasicRepository):
    """
    k12学生
    """

    def fetch_dingtalk_k12_student_with_parents(
        self,
        dingtalk_corp_id: str,
    ) -> List[DingtalkK12StudentDetailViewModel]:
        """
        获取学生和家长信息
        """
        sql = """with student as (
        select sks.*, array_agg(json_build_object('id', skds.id, 'version',
        skds."version", 'remote_dept_id', skd.remote_dept_id)) as dept_list,
        array_agg(skd.remote_dept_id) as remote_dept_ids
        from st_dingtalk_k12_student sks
        inner join st_dingtalk_k12_dept_student skds on sks.id = skds.dingtalk_k12_student_id
        inner join st_dingtalk_k12_dept skd on skd.id = skds.dingtalk_k12_dept_id
        where sks.dingtalk_corp_id = :dingtalk_corp_id
        group by sks.id),
        parent as (
        select s.id, array_agg(json_build_object('id', sr.id, 'version', 
        sr.version, 'relationship_code', sr.relationship_code,'relationship_name', sr.relationship_name,
        'dingtalk_k12_student_id', sr.dingtalk_k12_student_id,
        'dingtalk_k12_parent_id', sr.dingtalk_k12_parent_id,
        'parent_remote_user_id', sp.remote_user_id)) as relationship_list,
        array_agg(json_build_object('id', sp.id, 'version', sp.version,
        'dingtalk_corp_id',sp.dingtalk_corp_id, 'remote_user_id', sp.remote_user_id,
        'unionid', sp.unionid, 'feature', sp.feature, 'mobile', sp.mobile)) as parent_list
        from student s
        inner join st_dingtalk_k12_family_relationship sr on sr.dingtalk_k12_student_id = s.id
        inner join st_dingtalk_k12_parent sp on sr.dingtalk_k12_parent_id = sp.id
        group by s.id
        )
        select s.*, 
        coalesce(p.relationship_list, array[]::json[]) as relationship_list,
        coalesce(p.parent_list, array[]::json[]) as parent_list
        from student s
        left join parent p on s.id = p.id"""
        return self._fetch_all_to_model(
            model_cls=DingtalkK12StudentDetailViewModel,
            sql=sql,
            params={"dingtalk_corp_id": dingtalk_corp_id},
        )

    def insert_dingtalk_k12_student(
        self, student: DingtalkK12StudentModel, transaction: Transaction
    ) -> str:
        """
        插入钉钉k12学生
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DingtalkK12StudentEntity,
            entity_model=student,
            transaction=transaction,
        )

    def update_dingtalk_k12_student(
        self, student: DingtalkK12StudentModel, transaction: Transaction
    ):
        """
        更新钉钉k12学生
        只可能更新学生的名字
        """

        self._update_versioned_entity_by_model(
            entity_cls=DingtalkK12StudentEntity,
            update_model=student,
            transaction=transaction,
        )

    def delete_dingtalk_k12_student(self, dingtalk_k12_student_id: str, transaction: Transaction):
        """
        删除钉钉k12学生
        """

        self._delete_versioned_entity_by_id(
            entity_cls=DingtalkK12StudentEntity,
            entity_id=dingtalk_k12_student_id,
            transaction=transaction,
        )

    def get_dingtalk_k12_student_list_page(
        self, query_params: DingtalkK12StudentQueryParams, role_code: str
    ) -> PaginationCarrier[DingtalkK12StudentViewModel]:
        """
        获取学生列表页
        :param query_params:
        :param role_code:
        :return:
        """

        sql = """
        WITH student_dept_list AS (
        SELECT ms.student_id AS id, ms.student_name AS name, array_agg(DISTINCT dt.id) as dingtalk_k12_dept_id_list,
        ARRAY_AGG(DISTINCT ms.student_dept_name) AS dept_name_list, COALESCE(MIN(dsg.seq), 1000) AS grade_seq, 
        COALESCE(min(dss.seq), 1000) as class_seq
        from mv_student ms
        join sv_dingtalk_k12_dept_tree dt on ms.dingtalk_k12_dept_id = dt.id
        """

        if role_code == EnumRoleCode.TEACHER.name and not query_params.get_all:
            sql += """
            INNER JOIN st_dingtalk_user_k12_dept_duty  wukdd on (wukdd.duty = :head_teacher OR wukdd.duty = :teacher)
            AND wukdd.dingtalk_k12_dept_id = dt.id AND wukdd.dingtalk_user_id = :dingtalk_user_id
            """

        sql += """
        left join st_dingtalk_k12_dept_seq dsg on dt.parent_name like '%'||dsg.name||'%' 
        and dsg.category = :grade
        left join st_dingtalk_k12_dept_seq dss on dt.name like '%'||dss.name||'%' 
        and dss.category = :school_class
        WHERE ms.period_id = :period_id
        """

        if query_params.dingtalk_k12_dept_id:
            sql += """
            AND :dingtalk_k12_dept_id = ANY(dt.dept_sort_info)
            """

        sql += """
        GROUP BY ms.student_id, ms.student_name
        )
        SELECT sl.id, sl.name, sl.dingtalk_k12_dept_id_list, sl.dept_name_list, 
        ARRAY_TO_STRING(sl.dept_name_list, ' ') AS dept_name_string, sl.grade_seq, sl.class_seq,
        ARRAY_AGG(json_build_object('id', pcl.id, 'version', pcl.version, 'total_points', pcl.total_points,
        'points_balance', pcl.points_balance, 'points_category_code', pc.code)) AS points_conversion_log_list, 
        json_object_agg(lower(pc.code), pcl.total_points) ->> 'lucky_coin' AS lucky_coin_points,
        json_object_agg(lower(pc.code), pcl.total_points) ->> 'sticker' AS sticker_points
        FROM student_dept_list sl
        INNER JOIN st_points_conversion_log pcl on pcl.belong_to_resource_id = sl.id
        AND pcl.belong_to_resource_category = 'STUDENT'
        INNER JOIN st_points_category pc ON pc.id = pcl.points_category_id
        GROUP BY sl.id, sl.name, sl.dingtalk_k12_dept_id_list, sl.dept_name_list, sl.grade_seq, sl.class_seq
        """

        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["name", "dept_name_string"],
            order_columns=[
                OrderCondition(column_name="grade_seq"),
                OrderCondition(column_name="class_seq"),
                OrderCondition(column_name="name"),
                OrderCondition(column_name="sticker_points", order="desc"),
            ],
            params={
                "dingtalk_k12_dept_id": query_params.dingtalk_k12_dept_id,
                "period_id": query_params.period_id,
                "dingtalk_user_id": query_params.dingtalk_user_id,
                "head_teacher": EnumDingtalkUserK12DeptDutyMap.HEAD_TEACHER.name,
                "teacher": EnumDingtalkUserK12DeptDutyMap.TEACHER.name,
                "grade": EnumDingtalkK12DeptCategory.GRADE.name,
                "school_class": EnumDingtalkK12DeptCategory.SCHOOL_CLASS.name,
            },
        )
        return self._paginate(
            result_type=DingtalkK12StudentViewModel,
            total_params=page_init_params,
            page_params=query_params,
        )

    def fetch_dingtalk_k12_student_info(
        self, dingtalk_corp_id: str
    ) -> List[DingtalkK12StudentInfoViewModel]:
        """

        :param dingtalk_corp_id:
        :return:
        """
        sql = """
        select ks.*,array_agg(ds.dingtalk_k12_dept_id) as dingtalk_k12_dept_id_list, 
        json_agg(json_build_object('parent_id',fr.dingtalk_k12_parent_id,
        'relationship_name', fr.relationship_name)) as family_relationship
        from st_dingtalk_k12_student ks
        LEFT JOIN st_dingtalk_k12_family_relationship fr on fr.dingtalk_k12_student_id=ks.id
        INNER JOIN st_dingtalk_k12_dept_student ds on ds.dingtalk_k12_student_id=ks.id
        where ks.dingtalk_corp_id =:dingtalk_corp_id
        GROUP BY ks.id
        """

        return self._fetch_all_to_model(
            model_cls=DingtalkK12StudentInfoViewModel,
            sql=sql,
            params={"dingtalk_corp_id": dingtalk_corp_id},
        )
