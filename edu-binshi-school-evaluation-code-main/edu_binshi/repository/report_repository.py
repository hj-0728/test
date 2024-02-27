from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import OrderCondition, PageInitParams
from infra_basic.transaction import Transaction

from domain_evaluation.model.evaluation_assignment_model import (
    EnumEvaluationAssignmentEffectedCategory,
)
from domain_evaluation.model.evaluation_criteria_plan_model import EvaluationCriteriaPlanModel
from edu_binshi.data.query_params.evaluation_report_assignment_query_params import (
    EvaluationReportAssignmentQueryParams,
)
from edu_binshi.entity.report_record import ReportRecordEntity
from edu_binshi.entity.report_record_eval_assign_map import \
    ReportRecordEvalAssignMapEntity
from edu_binshi.model.edit.evaluation_report_dept_tree_em import EvaluationReportDeptTreeEditModel
from edu_binshi.model.report_model import (
    GrowthRecordReportEstablishmentAssignInfoModel,
    GrowthRecordReportEstablishmentAssignModel,
)
from edu_binshi.model.report_record_eval_assign_map_model import \
    ReportRecordEvalAssignMapModel
from edu_binshi.model.report_record_model import EnumReportRecordStatus, \
    ReportRecordModel
from edu_binshi.model.view.dept_tree_vm import DeptTreeViewModel
from edu_binshi.model.view.evaluation_report_assignment_vm import (
    EvaluationReportAssignmentViewModel,
)
from edu_binshi.model.view.report_record_vm import ReportRecordViewModel
from edu_binshi.model.view.report_vm import (
    DimensionDeptTreeReportInfoVm,
    ExistEstablishmentAssignReportVm,
    OrganizationReportInfoVm,
)
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.model.dimension_model import EnumDimensionCategory
from infra_backbone.model.role_model import EnumRoleCode


class ReportRepository(BasicRepository):
    """
    报告 repository
    """

    def insert_report_record(
        self,
        report_record: ReportRecordModel,
        transaction: Transaction,
    ):
        """
        添加word表格样式配置
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=ReportRecordEntity,
            entity_model=report_record,
            transaction=transaction
        )

    def update_report_record(
        self,
        report_record: ReportRecordModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新word表格样式配置
        """
        return self._update_versioned_entity_by_model(
            entity_cls=ReportRecordEntity,
            update_model=report_record,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_report_record(
        self,
        report_record_id: str,
        transaction: Transaction,
    ):
        """
        删除word表格样式配置
        """
        return self._delete_versioned_entity_by_id(
            entity_cls=ReportRecordEntity,
            entity_id=report_record_id,
            transaction=transaction,
        )

    def insert_report_record_eval_assign_map(
        self,
        report_record_eval_assign_map: ReportRecordEvalAssignMapModel,
        transaction: Transaction,
    ):
        """
        添加 报告记录评价分配map
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=ReportRecordEvalAssignMapEntity,
            entity_model=report_record_eval_assign_map,
            transaction=transaction
        )

    def get_dimension_dept_tree_report_info(
        self,
        dimension_dept_tree_id: str,
        evaluation_criteria_plan_id: str,
    ) -> Optional[DimensionDeptTreeReportInfoVm]:
        """

        :param dimension_dept_tree_id:
        :param evaluation_criteria_plan_id:
        :return:
        """
        sql = """
        SELECT secp.name AS evaluation_criteria_plan_name, sd.name AS dept_name,
        sp.name AS period_name, secp.name AS evaluation_criteria_name
        FROM st_dimension_dept_tree sdt
        INNER JOIN st_evaluation_criteria_plan secp 
        ON secp.executed_finish_at <= sdt.finish_at AND secp.executed_finish_at >= sdt.start_at
        INNER JOIN st_dept_history sd ON sd.id = sdt.dept_id
        and secp.executed_finish_at between sd.begin_at and sd.end_at
        INNER JOIN st_period sp ON sp.id = secp.focus_period_id
        WHERE secp.id = :evaluation_criteria_plan_id AND sdt.id = :dimension_dept_tree_id
        """
        return self._fetch_first_to_model(
            model_cls=DimensionDeptTreeReportInfoVm,
            sql=sql,
            params={
                "dimension_dept_tree_id": dimension_dept_tree_id,
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
            },
        )

    def get_evaluation_criteria_plan_by_id(
        self, evaluation_criteria_plan_id: str
    ) -> Optional[EvaluationCriteriaPlanModel]:
        """
        通过 id 获取评价标准计划
        :param evaluation_criteria_plan_id:
        :return:
        """

        sql = """
        select * from st_evaluation_criteria_plan where id = :evaluation_criteria_plan_id
        """

        return self._fetch_first_to_model(
            model_cls=EvaluationCriteriaPlanModel,
            params={"evaluation_criteria_plan_id": evaluation_criteria_plan_id},
            sql=sql,
        )

    def get_exist_report_file(
        self,
        args: ReportRecordModel,
    ) -> Optional[ExistEstablishmentAssignReportVm]:
        """
        通过 id 获取评价标准计划
        :param args:
        :return:
        """

        sql = """
        WITH report_record AS (
        SELECT *
        FROM st_report_record srr
        WHERE srr.evaluation_criteria_plan_id = :evaluation_criteria_plan_id 
        AND srr.user_role_id = :user_role_id
        AND srr.target_id = :target_id 
        AND srr.target_category = :target_category AND srr.error IS NULL
        and srr.status=:status
        ORDER BY srr.created_at DESC
        LIMIT 1
        )
        SELECT sr.object_name, sr.bucket_name, sfr.file_id,
        sfr.relationship AS file_relationship_relationship
        FROM report_record rr
        INNER JOIN st_file_relationship sfr 
        ON sfr.res_id = rr.id AND sfr.res_category = 'REPORT_RECORD'
        INNER JOIN st_file_info sfi ON sfi.id = sfr.file_id
        INNER JOIN st_object_storage_raw sr ON sr.id = sfi.storage_info_id
        """

        return self._fetch_first_to_model(
            model_cls=ExistEstablishmentAssignReportVm,
            params={
                "evaluation_criteria_plan_id": args.evaluation_criteria_plan_id,
                "user_role_id": args.user_role_id,
                "target_id": args.target_id,
                "target_category": args.target_category,
                "status": EnumReportRecordStatus.SUCCEED.name,
            },
            sql=sql,
        )

    def get_evaluation_report_dept(
        self, params: EvaluationReportDeptTreeEditModel
    ) -> List[DeptTreeViewModel]:
        """
        获取评价报告页需要展示的部门
        """

        only_capacity_sql = ""
        if params.current_role_code == EnumRoleCode.TEACHER.name:
            # 仅捞取职责内的 下面这段sql，其实有一个隐含条件，目前从钉钉同步过来的数据，老师只会出现在班级内，没有年级主任这些
            only_capacity_sql = """
            and st.id = any(
            select distinct se.dimension_dept_tree_id from cv_establishment_assign sa
            inner join cv_establishment se on se.id = sa.establishment_id
            inner join st_capacity sc on sc.id = se.capacity_id
            and sc.code = any(array[:capacity])
            where sa.people_id = :people_id
            )
            """
        dimension_tree_sql = """"""
        if params.dimension_dept_tree_id:
            # 用户选中了某个部门，则捞取该部门下的参评学生
            dimension_tree_sql = """and :dimension_dept_tree_id = ANY(sp2.tree_path)"""
        sql = f"""
        with tree as (
        select distinct sp2.* from st_evaluation_assignment sa1
        inner join st_establishment_assign sa2 on sa1.effected_category = :effected_category and sa1.effected_id = sa2.id
        inner join st_establishment se on se.id = sa2.establishment_id
        inner join st_dimension_dept_tree st on st.id = se.dimension_dept_tree_id
        inner join sv_k12_dimension_dept_tree_path sp on st.id = any(sp.tree_path)
        inner join sv_k12_dimension_dept_tree_path sp2 on sp2.id = any(sp.tree_path)
        where evaluation_criteria_plan_id = :plan_id
        and sa1.finish_at = 'infinity'
        {only_capacity_sql}
        {dimension_tree_sql}
        ),
        dept_name as (
        select t.id, sh.name from tree t
        inner join st_dept_history sh on sh.id = t.dept_id
        and :compared_time between sh.begin_at and sh.end_at
        )
        select tree.*, dn.name, sc.code as dept_category_code from tree
        inner join dept_name dn on tree.id = dn.id
        inner join st_dept_dept_category_map sm on sm.dept_id = tree.dept_id
        inner join st_dept_category sc on sc.id = sm.dept_category_id
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=DeptTreeViewModel,
            params={
                "plan_id": params.evaluation_criteria_plan_id,
                "dimension_dept_tree_id": params.dimension_dept_tree_id,
                "compared_time": params.compared_time,
                "people_id": params.current_people_id,
                "effected_category": EnumEvaluationAssignmentEffectedCategory.ESTABLISHMENT_ASSIGN.name,
                "capacity": [EnumCapacityCode.HEAD_TEACHER.name, EnumCapacityCode.TEACHER.name],
            },
        )

    def fetch_evaluation_report_assignment(
        self, params: EvaluationReportAssignmentQueryParams
    ) -> PaginationCarrier[EvaluationReportAssignmentViewModel]:
        """
        获取评价报告页的分配列表
        """
        only_capacity_sql = ""
        if params.current_role_code == EnumRoleCode.TEACHER.name:
            # 仅捞取职责内的 下面这段sql，其实有一个隐含条件，目前从钉钉同步过来的数据，老师只会出现在班级内，没有年级主任这些
            only_capacity_sql = """
            and sp.id = any(
            select distinct se.dimension_dept_tree_id from cv_establishment_assign sa
            inner join cv_establishment se on se.id = sa.establishment_id
            inner join st_capacity sc on sc.id = se.capacity_id
            and sc.code = any(array[:capacity])
            where sa.people_id = :people_id
            )
            """
        if params.dimension_dept_tree_id:
            # 用户选中了某个部门，则捞取该部门下的参评学生
            dimension_tree_sql = """ st.id = :dimension_dept_tree_id"""
        else:
            # 如果用户没选中具体的部门，则默认捞全部参评学生
            dimension_tree_sql = """ st.parent_dept_id is null """
        sql = f"""
        WITH report_list AS (
        SELECT sfr.res_id, rank() OVER (PARTITION BY sfr.res_id ORDER BY sfr.handled_at DESC) AS report_seq,
        sr.object_name, sr.bucket_name, sfr.relationship AS file_relationship_relationship,
        sfr.file_id
        FROM st_file_relationship sfr
        inner join st_evaluation_assignment sea on sea.id=sfr.res_id
        INNER JOIN st_file_info sfi ON sfi.id = sfr.file_id
        INNER JOIN st_object_storage_raw sr ON sr.id = sfi.storage_info_id
        WHERE sea.evaluation_criteria_plan_id = :plan_id and 
        sfr.relationship = 'REPORT_PDF' and sfr.res_category = 'EVALUATION_ASSIGNMENT'
        )
        , evaluation_assignment as (
        select sea.id as evaluation_assignment_id, sp.dept_id, sp.seq_list, p.id as people_id,
        p.name as people_name, sa.id AS establishment_assign_id, rl.file_id as report_file_id, rl.*,
        sp.parent_dept_id
        from st_dimension_dept_tree st
        inner join sv_k12_dimension_dept_tree_path sp on st.id = any(sp.tree_path)
        inner join st_establishment se on se.dimension_dept_tree_id = sp.id
        inner join st_establishment_assign sa on sa.establishment_id = se.id 
        and sa.finish_at>=:compared_time
        inner join st_people p on p.id =  sa.people_id
        inner join st_evaluation_assignment sea on sea.effected_category = :effected_category 
        and sea.effected_id = sa.id
        left join report_list rl on rl.res_id = sea.id and rl.report_seq=1
        where {dimension_tree_sql}
        and sea.evaluation_criteria_plan_id = :plan_id
        AND sea.finish_at > now()
        {only_capacity_sql}
        ),
        dept_name as (
        select evaluation_assignment_id,
        sh.name as class_name,sh2.name as grade_name,
        case when sh2.name is null then sh.name else sh2.name || '/' || sh.name end as name
        from evaluation_assignment ea
        inner join st_dept_history sh on sh.id = ea.dept_id
        and :compared_time between sh.begin_at and sh.end_at
        left join st_dept_history sh2 on sh2.id = ea.parent_dept_id
        and :compared_time between sh2.begin_at and sh2.end_at
        )
        select ea.*, dn.name as dept_name,dn.grade_name,dn.class_name
        from evaluation_assignment ea
        inner join dept_name dn on dn.evaluation_assignment_id = ea.evaluation_assignment_id
        """
        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["people_name"],
            order_columns=[
                OrderCondition(column_name="seq_list"),
                OrderCondition(column_name="people_name"),
            ],
            params={
                "effected_category": EnumEvaluationAssignmentEffectedCategory.ESTABLISHMENT_ASSIGN.name,
                "plan_id": params.evaluation_criteria_plan_id,
                "compared_time": params.compared_time,
                "dimension_dept_tree_id": params.dimension_dept_tree_id,
                "people_id": params.current_people_id,
                "capacity": [EnumCapacityCode.HEAD_TEACHER.name, EnumCapacityCode.TEACHER.name],
                "EDU": EnumDimensionCategory.EDU.name,
            },
        )
        return self._paginate(
            result_type=EvaluationReportAssignmentViewModel,
            total_params=page_init_params,
            page_params=params,
        )

    def get_organization_report_info(
        self,
        organization_id: str,
        evaluation_criteria_plan_id: str,
    ) -> Optional[OrganizationReportInfoVm]:
        """
        获取组织报告信息
        :param organization_id:
        :param evaluation_criteria_plan_id:
        :return:
        """

        sql = """
        WITH data_info AS (
        SELECT secp.name AS evaluation_criteria_plan_name, secp.executed_finish_at,
        sp.name AS period_name, secp.name AS evaluation_criteria_name
        FROM st_evaluation_criteria_plan secp 
        INNER JOIN st_period sp ON sp.id = secp.focus_period_id
        WHERE secp.id = :evaluation_criteria_plan_id
        )
        ,organization_info AS (
        SELECT DISTINCT ON (sh.id) ROW_NUMBER() OVER (PARTITION BY sh.id ORDER BY sh.end_at DESC) AS date_seq,
        sh.*, di.executed_finish_at
        FROM st_organization_history sh
        INNER JOIN data_info di ON di.executed_finish_at <= sh.end_at AND di.executed_finish_at >= sh.begin_at
        WHERE sh.id = :organization_id
        ORDER BY sh.id, sh.end_at DESC
        )
        SELECT di.*, oi.name AS organization_name
        FROM organization_info oi
        CROSS JOIN data_info di
        """
        return self._fetch_first_to_model(
            model_cls=OrganizationReportInfoVm,
            sql=sql,
            params={
                "organization_id": organization_id,
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
            },
        )

    def get_report_record_by_report_record_id_and_status(
        self, report_record_id: str, status: str,
    ) -> List[ReportRecordModel]:
        """
        获取报告记录根据报告记录id及状态，包括自己
        :param report_record_id:
        :param status:
        :return:
        """
        sql = """
        SELECT srr.*
        FROM st_report_record srr 
        inner join st_report_record rr on srr.created_at<=rr.created_at
        WHERE rr.id=:report_record_id 
        and srr.evaluation_criteria_plan_id = rr.evaluation_criteria_plan_id
        AND srr.user_role_id = rr.user_role_id
        AND srr.target_id = rr.target_id
        AND srr.target_category = rr.target_category AND srr.error IS NULL
        and srr.status=:status
        ORDER BY srr.created_at DESC
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=ReportRecordModel,
            params={
                "status": status,
                "report_record_id": report_record_id,
            }
        )

    def get_report_record_by_status(self, status: str) -> List[ReportRecordModel]:
        """
        获取评价记录通过状态
        :param status:
        :return:
        """

        sql = """
        select * from st_report_record where status=:status
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=ReportRecordModel,
            params={
                "status": status,
            }
        )
