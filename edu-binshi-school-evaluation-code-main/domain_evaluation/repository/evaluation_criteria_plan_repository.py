from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import OrderCondition, PageInitParams
from infra_basic.transaction import Transaction

from domain_evaluation.data.query_params.evaluation_criteria_plan_query_params import (
    EvaluationCriteriaPlanQueryParams,
)
from domain_evaluation.data.query_params.evaluation_criteria_plan_stats_query_params import (
    EvaluationCriteriaPlanStatsQueryParams,
)
from domain_evaluation.entity.evaluation_criteria_plan import EvaluationCriteriaPlanEntity
from domain_evaluation.model.evaluation_assignment_model import EvaluationAssignmentModel
from domain_evaluation.model.evaluation_criteria_plan_model import (
    EnumEvaluationCriteriaPlanStatus,
    EvaluationCriteriaPlanModel,
)
from domain_evaluation.model.evaluation_criteria_plan_scope_model import EnumGroupCategory
from domain_evaluation.model.view.evaluation_criteria_plan_detail_vm import (
    EvaluationCriteriaPlanDetailVm,
)
from domain_evaluation.model.view.evaluation_criteria_plan_scope_vm import EvaluationCriteriaPlanScopeViewModel
from domain_evaluation.model.view.evaluation_criteria_plan_vm import (
    EvaluationCriteriaPlanStatsViewModel,
    EvaluationCriteriaPlanViewModel,
)
from edu_binshi.model.report_model import EnumReportCategory


class EvaluationCriteriaPlanRepository(BasicRepository):
    """
    评价标准计划 repository
    """

    def insert_evaluation_criteria_plan(
        self,
        evaluation_criteria_plan: EvaluationCriteriaPlanModel,
        transaction: Transaction = None,
    ) -> str:
        """
        插入评价标准计划
        :param evaluation_criteria_plan:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=EvaluationCriteriaPlanEntity,
            entity_model=evaluation_criteria_plan,
            transaction=transaction,
        )

    def update_evaluation_criteria_plan(
        self,
        evaluation_criteria_plan: EvaluationCriteriaPlanModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新评价标准计划
        :param evaluation_criteria_plan:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        return self._update_versioned_entity_by_model(
            entity_cls=EvaluationCriteriaPlanEntity,
            update_model=evaluation_criteria_plan,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def delete_evaluation_criteria_plan(
        self,
        evaluation_criteria_plan_id: str,
        transaction: Transaction = None,
    ):
        """
        删除评价标准计划
        :param evaluation_criteria_plan_id:
        :param transaction:
        :return:
        """
        self._delete_versioned_entity_by_id(
            entity_cls=EvaluationCriteriaPlanEntity,
            entity_id=evaluation_criteria_plan_id,
            transaction=transaction,
        )

    def get_evaluation_criteria_plan_list(
            self, params: EvaluationCriteriaPlanQueryParams
    ) -> PaginationCarrier[EvaluationCriteriaPlanViewModel]:
        """
        获取评价计划列表
        """

        sql = """
        WITH evaluation_criteria_plan AS (
        SELECT sp.id, sp.handler_category, sp.handler_id, sp.handled_at, sp.version, sp.evaluation_criteria_id, 
        sp.focus_period_id,  sp.name, sp.executed_start_at, sp.executed_finish_at,
        CASE WHEN (sp.status = :PUBLISHED and sp.executed_finish_at < now()) THEN :ARCHIVED
        ELSE sp.status END AS status
        FROM st_evaluation_criteria_plan sp
        )
        SELECT cp.*,
        sc.name AS evaluation_criteria_name, sc.status AS evaluation_criteria_status,
        sc.evaluation_object_category AS evaluation_object_category,
        CASE WHEN cp.status = :DRAFT THEN 1
        WHEN cp.status = :PUBLISHED THEN 2
        WHEN cp.status = :ARCHIVED THEN 3
        ELSE 4
        END AS status_order
        FROM evaluation_criteria_plan cp
        JOIN st_evaluation_criteria sc ON cp.evaluation_criteria_id = sc.id
         """

        if params.status_list:
            sql += """
            AND cp.status = ANY(:status_list)
            """

        if params.finished:
            sql += """
            AND cp.executed_finish_at<=now()
            """

        if params.is_current_period and params.period_id:
            sql += " and cp.focus_period_id=:period_id "

        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["name", "evaluation_criteria_name"],
            order_columns=[
                OrderCondition(column_name="status_order"),
                OrderCondition(column_name="handled_at", order="desc"),
            ],
            params={
                "status_list": params.status_list,
                "period_id": params.period_id,
                "ARCHIVED": EnumEvaluationCriteriaPlanStatus.ARCHIVED.name,
                "PUBLISHED": EnumEvaluationCriteriaPlanStatus.PUBLISHED.name,
                "DRAFT": EnumEvaluationCriteriaPlanStatus.DRAFT.name
            },
        )
        return self._paginate(
            result_type=EvaluationCriteriaPlanViewModel,
            total_params=page_init_params,
            page_params=params,
        )

    def fetch_evaluation_criteria_plan_by_id(
        self, evaluation_criteria_plan_id: str
    ) -> Optional[EvaluationCriteriaPlanModel]:
        """
        通过 id 获取评价标准计划
        :param evaluation_criteria_plan_id:
        :return:
        """

        sql = """
        select *,
        CASE WHEN COUNT(*) > 0 THEN :GROWTH_RECORD ELSE :GOOD_CONDUCT_EVALUATION_RECORD END AS report_category  
        from st_evaluation_criteria_plan
        where id = :evaluation_criteria_plan_id
        GROUP BY id
        """

        return self._fetch_first_to_model(
            model_cls=EvaluationCriteriaPlanModel,
            params={
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
                "GROWTH_RECORD": EnumReportCategory.GROWTH_RECORD.name,
                "GOOD_CONDUCT_EVALUATION_RECORD": EnumReportCategory.GOOD_CONDUCT_EVALUATION_RECORD.name
            },
            sql=sql,
        )

    def fetch_plan_evaluation_assignment_by_plan_id(
        self, evaluation_criteria_plan_id: str
    ) -> List[EvaluationAssignmentModel]:
        """
        通过计划 id 获取评价分配
        :param evaluation_criteria_plan_id:
        :return:
        """

        sql = """
        select a.* 
        from st_evaluation_criteria_plan p 
        INNER JOIN st_evaluation_assignment a on p.id=a.evaluation_criteria_plan_id
        where p.id=:evaluation_criteria_plan_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=EvaluationAssignmentModel,
            params={"evaluation_criteria_plan_id": evaluation_criteria_plan_id},
        )

    def delete_evaluation_criteria(
        self,
        evaluation_criteria_plan_id: str,
        transaction: Transaction = None,
    ):
        """
        删除评价标准
        :param evaluation_criteria_plan_id:
        :param transaction:
        :return:
        """
        self._delete_versioned_entity_by_id(
            entity_cls=EvaluationCriteriaPlanEntity,
            entity_id=evaluation_criteria_plan_id,
            transaction=transaction,
        )

    def get_evaluation_criteria_plan_detail(
        self, evaluation_criteria_plan_id: str
    ) -> Optional[EvaluationCriteriaPlanDetailVm]:
        """
        获取评价标准计划详情
        :param evaluation_criteria_plan_id:
        :return:
        """

        sql = """
        SELECT scp.*, spc.code AS period_category_code, ps.scope_category, 
        CASE
            WHEN ps.scope_category = :PERSONAL THEN 
                JSONB_AGG ( JSONB_BUILD_OBJECT ( 'id', ps.scope_id, 'name', sp2.name ) )
            WHEN ps.scope_category = :DEPT THEN
                JSONB_AGG ( JSONB_BUILD_OBJECT ( 'id', ps.scope_id, 'name', sd.name ) )
            ELSE 
                '[]'::jsonb
        END AS scope_info, ec.name AS evaluation_criteria_name 
        FROM st_evaluation_criteria_plan scp
        INNER JOIN st_period sp ON sp.id = scp.focus_period_id
        INNER JOIN st_period_category spc ON spc.id = sp.period_category_id
        INNER JOIN st_evaluation_criteria ec ON ec.id = scp.evaluation_criteria_id
        LEFT JOIN st_evaluation_criteria_plan_scope ps ON ps.evaluation_criteria_plan_id = scp.id
        and ps.finish_at = 'infinity'
        LEFT JOIN st_dept sd ON ps.scope_id = sd.ID AND ps.scope_category = :DEPT
        LEFT JOIN st_establishment_assign ea on ea.id = ps.scope_id AND ps.scope_category = :PERSONAL
        LEFT JOIN st_people sp2 ON sp2.id = ea.people_id
        WHERE scp.id = :evaluation_criteria_plan_id
        GROUP BY scp.id, spc.code, ps.scope_category, ec.name
        """

        return self._fetch_first_to_model(
            model_cls=EvaluationCriteriaPlanDetailVm,
            params={
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
                "PERSONAL": EnumGroupCategory.PERSONAL.name,
                "DEPT": EnumGroupCategory.DEPT.name,
            },
            sql=sql,
        )

    def get_evaluation_criteria_plan_vm_by_plan_id(
        self, evaluation_criteria_plan_id: str
    ) -> Optional[EvaluationCriteriaPlanViewModel]:
        """
        通过计划 id 获取评价计划标准的相关信息
        :param evaluation_criteria_plan_id:
        :return:
        """

        sql = """
        select * from sv_evaluation_criteria_plan
        where id =:evaluation_criteria_plan_id
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=EvaluationCriteriaPlanViewModel,
            params={"evaluation_criteria_plan_id": evaluation_criteria_plan_id},
        )

    def get_evaluation_criteria_plan_todo_page_list(
        self,
        params: EvaluationCriteriaPlanStatsQueryParams,
    ) -> PaginationCarrier[EvaluationCriteriaPlanStatsViewModel]:
        """
        获取评价标准计划列表
        :param params:
        :return:
        """
        sql = """
        with evaluation_assignment as (
        SELECT DISTINCT ea.evaluation_criteria_plan_id, bin.plan_name, 
        bin.executed_start_at, bin.executed_finish_at, bin.plan_status,
        bin.evaluation_criteria_name, bin.evaluation_object_category,
        isl.id as input_score_log_id, isl.filler_id
        FROM mv_benchmark_input_node bin
        INNER JOIN st_input_score_log isl on isl.benchmark_input_node_id = bin.id 
        INNER JOIN cv_evaluation_assignment ea on ea.id = isl.evaluation_assignment_id
        and bin.plan_id = ea.evaluation_criteria_plan_id
        INNER JOIN st_establishment_assign se on se.id = isl.expected_filler_id
        and isl.expected_filler_category = 'ESTABLISHMENT_ASSIGN'
        WHERE se.people_id = :people_id
        and bin.focus_period_id = :focus_period_id
        UNION ALL
        SELECT DISTINCT ea.evaluation_criteria_plan_id, bin.plan_name,
        bin.executed_start_at, bin.executed_finish_at, bin.plan_status,
        bin.evaluation_criteria_name, bin.evaluation_object_category,
        isl.id as input_score_log_id, isl.filler_id
        FROM mv_benchmark_input_node bin
        INNER JOIN st_input_score_log isl on isl.benchmark_input_node_id = bin.id 
        INNER JOIN cv_evaluation_assignment ea on ea.id = isl.evaluation_assignment_id
        and bin.plan_id = ea.evaluation_criteria_plan_id
        INNER JOIN st_team_history st on st.id = isl.expected_filler_id
        and isl.expected_filler_category = 'TEAM'
        and bin.compare_at BETWEEN st.begin_at and st.end_at
        INNER JOIN st_team_member tm on st.id = tm.team_id
        and bin.compare_at BETWEEN tm.start_at and tm.finish_at
        where bin.focus_period_id = :focus_period_id
        and tm.people_id = :people_id
        ) SELECT evaluation_criteria_plan_id, plan_name, executed_start_at, executed_finish_at,
        evaluation_criteria_name, evaluation_object_category, plan_status,
        COUNT(input_score_log_id) FILTER (WHERE filler_id IS NULL) AS not_fill_count,
        cast(COUNT(input_score_log_id) FILTER (WHERE filler_id IS NULL) as VARCHAR) AS not_fill_count_text,
        COUNT(input_score_log_id) FILTER (WHERE filler_id = :people_id) AS fill_count,
        cast(COUNT(input_score_log_id) FILTER (WHERE filler_id = :people_id) as VARCHAR) AS fill_count_text 
        FROM evaluation_assignment
        where 1=1
        """

        if len(params.evaluation_object_category_list) > 0:
            sql += " and evaluation_object_category = any(array[:evaluation_object_category_list])"
        if len(params.plan_status_list) > 0:
            sql += " and plan_status = any(array[:plan_status_list])"
        sql += """
        GROUP BY evaluation_criteria_plan_id, plan_name, executed_start_at, executed_finish_at,
        plan_status, evaluation_criteria_name, evaluation_object_category
        """
        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=[
                "plan_name",
                "evaluation_criteria_name",
                "not_fill_count_text",
                "fill_count_text",
            ],
            order_columns=[
                OrderCondition(column_name="plan_status", order="desc"),
                OrderCondition(column_name="executed_start_at", order="desc"),
                OrderCondition(column_name="plan_name"),
                OrderCondition(column_name="evaluation_criteria_name"),
            ],
            params={
                "people_id": params.people_id,
                "focus_period_id": params.focus_period_id,
                "evaluation_object_category_list": params.evaluation_object_category_list,
                "plan_status_list": params.plan_status_list,
            },
        )
        return self._paginate(
            result_type=EvaluationCriteriaPlanStatsViewModel,
            total_params=page_init_params,
            page_params=params,
        )

    def get_evaluation_criteria_plan_by_name(
        self, name: str
    ) -> Optional[EvaluationCriteriaPlanModel]:
        """
        根据name获取评价标准计划
        :param name:
        :return:
        """
        sql = """
        select * from st_evaluation_criteria_plan where name=:name
        """
        return self._fetch_first_to_model(
            sql=sql, model_cls=EvaluationCriteriaPlanModel, params={"name": name}
        )

    def get_finished_evaluation_criteria_plan(self) -> List[EvaluationCriteriaPlanModel]:
        """
        获取已执行完成的评价计划
        """
        sql = """
        SELECT * FROM st_evaluation_criteria_plan cp 
        WHERE cp.executed_finish_at < now()
        AND cp.status = :PUBLISHED
        """

        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaPlanModel,
            sql=sql,
            params={"PUBLISHED": EnumEvaluationCriteriaPlanStatus.PUBLISHED.name},
        )

    def fetch_executing_plan_by_benchmark_id(
        self, benchmark_id: str
    ) -> List[EvaluationCriteriaPlanModel]:
        """
        根据基准id获取正在执行的计划
        """
        sql = """select sp.*
        from st_benchmark sb
        inner join st_indicator si on si.id = sb.indicator_id
        inner join st_evaluation_criteria_tree st on st.indicator_id = si.id
        inner join st_evaluation_criteria_plan sp on sp.evaluation_criteria_id = st.evaluation_criteria_id
        where sb.id = :benchmark_id
        and now() between st.start_at and st.finish_at
        and now() between sp.executed_start_at and sp.executed_finish_at
        and sp.status = :published
        """
        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaPlanModel,
            sql=sql,
            params={
                "benchmark_id": benchmark_id,
                "published": EnumEvaluationCriteriaPlanStatus.PUBLISHED.name,
            },
        )

    def fetch_executing_plan_scope(self) -> List[EvaluationCriteriaPlanScopeViewModel]:
        """
        获取计划的执行范围
        """
        sql = """
        select row_to_json(sp.*) as plan,
        array_to_json(array_agg(row_to_json(sc.*))) as scope_list
        from st_evaluation_criteria_plan sp
        inner join st_evaluation_criteria_plan_scope sc on sp.id = sc.evaluation_criteria_plan_id
        and now() between sc.start_at and sc.finish_at
        where status = :published
        and now() between executed_start_at and executed_finish_at
        group by sp.id
        """
        return self._fetch_all_to_model(
            model_cls=EvaluationCriteriaPlanScopeViewModel,
            sql=sql,
            params={"published": EnumEvaluationCriteriaPlanStatus.PUBLISHED.name},
        )
