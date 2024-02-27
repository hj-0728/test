from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import OrderCondition, PageInitParams
from infra_basic.transaction import Transaction

from domain_evaluation.data.query_params.evaluation_assignment_query_params import (
    EvaluationAssignmentQueryParams,
)
from domain_evaluation.entity.evaluation_assignment import EvaluationAssignmentEntity
from domain_evaluation.model.benchmark_input_node_model import \
    BenchmarkInputNodeFillerCalcMethod
from domain_evaluation.model.benchmark_model import BenchmarkModel
from domain_evaluation.model.evaluation_assignment_model import (
    EnumEvaluationAssignmentEffectedCategory,
    EvaluationAssignmentModel,
)
from domain_evaluation.model.evaluation_criteria_plan_model import \
    EnumEvaluationCriteriaPlanStatus
from domain_evaluation.model.view.evaluation_assignment_vm import \
    EvaluationAssignmentViewModel


class EvaluationAssignmentRepository(BasicRepository):
    """
    评价分配 repository
    """

    def insert_evaluation_assignment(
        self,
        data: EvaluationAssignmentModel,
        transaction: Transaction = None,
    ) -> str:
        """
        插入评价分配
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=EvaluationAssignmentEntity,
            entity_model=data,
            transaction=transaction,
        )

    def update_evaluation_assignment(
        self,
        data: EvaluationAssignmentModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新评价分配
        :param data:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        return self._update_versioned_entity_by_model(
            entity_cls=EvaluationAssignmentEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def get_evaluation_assignment_todo_list(
        self, params: EvaluationAssignmentQueryParams
    ) -> PaginationCarrier[EvaluationAssignmentViewModel]:
        """
        获取评价分配需要做的列表
        :param params:
        :return:
        """
        sql = """
        with evaluation_assignment as (
        SELECT DISTINCT ea.id, ea.evaluation_criteria_plan_id, bin.plan_name, 
        bin.executed_start_at, bin.executed_finish_at, bin.plan_status,
        bin.evaluation_criteria_name, bin.evaluation_object_category,
        ea.effected_id, ea.effected_category, bin.evaluation_criteria_id,
        isl.id as input_score_log_id, isl.filler_id, isl.expected_filler_category,
        isl.expected_filler_id, bin.benchmark_id, bin.benchmark_name
        FROM mv_benchmark_input_node bin
        INNER JOIN st_input_score_log isl on isl.benchmark_input_node_id = bin.id 
        INNER JOIN cv_evaluation_assignment ea on ea.id = isl.evaluation_assignment_id
        and bin.plan_id = ea.evaluation_criteria_plan_id
        INNER JOIN st_establishment_assign se on se.id = isl.expected_filler_id
        and isl.expected_filler_category = 'ESTABLISHMENT_ASSIGN'
        WHERE se.people_id = :people_id
        and bin.focus_period_id = :focus_period_id
        and bin.plan_id = :evaluation_criteria_plan_id
        UNION ALL
        SELECT DISTINCT ea.id, ea.evaluation_criteria_plan_id, bin.plan_name, 
        bin.executed_start_at, bin.executed_finish_at, bin.plan_status,
        bin.evaluation_criteria_name, bin.evaluation_object_category,
        ea.effected_id, ea.effected_category, bin.evaluation_criteria_id,
        isl.id as input_score_log_id, isl.filler_id, isl.expected_filler_category,
        isl.expected_filler_id, bin.benchmark_id, bin.benchmark_name
        FROM mv_benchmark_input_node bin
        INNER JOIN st_input_score_log isl on bin.id = isl.benchmark_input_node_id
        INNER JOIN cv_evaluation_assignment ea on ea.id = isl.evaluation_assignment_id
        and bin.plan_id = ea.evaluation_criteria_plan_id
        INNER JOIN st_team_history st on st.id = isl.expected_filler_id
        and isl.expected_filler_category = 'TEAM'
        and bin.compare_at BETWEEN st.begin_at and st.end_at
        INNER JOIN st_team_member tm on st.id = tm.team_id
        and bin.compare_at BETWEEN tm.start_at and tm.finish_at
        WHERE bin.focus_period_id = :focus_period_id
        and bin.plan_id = :evaluation_criteria_plan_id
        and tm.people_id = :people_id
        ), evaluation_assignment_effected as (
        SELECT DISTINCT ea.*, sp.name as people_name, parent.name || '/' || sd.name as dept_name,
        sp.name || '（' || parent.name || '/' || sd.name || '）' as effected_name,
        sr.bucket_name as avatar_bucket_name, sr.object_name as avatar_object_name
        FROM evaluation_assignment ea 
        inner join ( select *,LEAST(handled_at, executed_finish_at) as least_time 
        from st_evaluation_criteria_plan) cp on cp.id=ea.evaluation_criteria_plan_id
        INNER JOIN st_establishment_assign sea on ea.effected_id = sea.id 
        and ea.effected_category = 'ESTABLISHMENT_ASSIGN'
        INNER JOIN st_people_history sp on sea.people_id = sp.id and (
        ((cp.status=:ABOLISHED or (cp.status!=:DRAFT and cp.executed_finish_at<now())
        ) and (least_time BETWEEN sp.begin_at and sp.end_at)) or 
        ((cp.status=:DRAFT or (cp.status!=:ABOLISHED and cp.executed_finish_at>now())
        ) and sp.end_at>now()))
        INNER JOIN st_establishment se on sea.establishment_id = se.id 
        INNER JOIN st_capacity sc on se.capacity_id = sc.id
        INNER JOIN st_dimension_dept_tree ddt on se.dimension_dept_tree_id = ddt.id 
        INNER JOIN st_dept_history sd on ddt.dept_id = sd.id and (
        ((cp.status=:ABOLISHED or (cp.status!=:DRAFT and cp.executed_finish_at<now())
        ) and (least_time BETWEEN sd.begin_at and sd.end_at)) or 
        ((cp.status=:DRAFT or (cp.status!=:ABOLISHED and cp.executed_finish_at>now())
        ) and sd.end_at>now()))
        INNER JOIN st_dept_history parent on ddt.parent_dept_id = parent.id and (
        ((cp.status=:ABOLISHED or (cp.status!=:DRAFT and cp.executed_finish_at<now())
        ) and (least_time BETWEEN parent.begin_at and parent.end_at)) or 
        ((cp.status=:DRAFT or (cp.status!=:ABOLISHED and cp.executed_finish_at>now())
        ) and parent.end_at>now()))
        INNER JOIN st_file_relationship fr on sp.id = fr.res_id and fr.res_category = 'PEOPLE'
        INNER JOIN st_file_info fi on fr.file_id = fi.id 
        INNER JOIN st_object_storage_raw sr on sr.id = fi.storage_info_id
        ), input_score_log_fill_info as (
        SELECT ea.id as evaluation_assignment_id,
        COUNT(isl.id) FILTER (WHERE isl.filler_id IS NULL) AS not_fill_count,
        COUNT(isl.id) FILTER (WHERE isl.filler_id = :people_id) AS fill_count 
        FROM evaluation_assignment ea 
        INNER JOIN st_input_score_log isl on ea.input_score_log_id = isl.id
        GROUP BY ea.id
        ) SELECT DISTINCT eae.id, eae.evaluation_criteria_plan_id, eae.plan_name, eae.executed_start_at, 
        eae.executed_finish_at, eae.evaluation_criteria_id, eae.evaluation_criteria_name,
        eae.effected_name, eae.evaluation_object_category, eae.people_name, 
        eae.dept_name, eae.avatar_bucket_name, eae.avatar_object_name, 
        fi.not_fill_count, fi.fill_count, eae.plan_status,
        cast(fi.not_fill_count as VARCHAR) as not_fill_count_text,
        cast(fi.fill_count as VARCHAR) as fill_count_text
        FROM evaluation_assignment_effected eae 
        INNER JOIN input_score_log_fill_info fi on eae.id = fi.evaluation_assignment_id
        """
        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=[
                "people_name",
                "dept_name",
                "not_fill_count_text",
                "fill_count_text",
            ],
            order_columns=[
                OrderCondition(column_name="not_fill_count", order="desc"),
                OrderCondition(column_name="effected_name"),
            ],
            params={
                "effected_category": EnumEvaluationAssignmentEffectedCategory.ESTABLISHMENT_ASSIGN.name,
                "people_id": params.people_id,
                "evaluation_criteria_plan_id": params.evaluation_criteria_plan_id,
                "focus_period_id": params.focus_period_id,
                "ABOLISHED": EnumEvaluationCriteriaPlanStatus.ABOLISHED.name,
                "DRAFT": EnumEvaluationCriteriaPlanStatus.DRAFT.name,
            },
        )
        return self._paginate(
            result_type=EvaluationAssignmentViewModel,
            total_params=page_init_params,
            page_params=params,
        )

    def get_evaluation_assignment_about_me_list(
        self, params: EvaluationAssignmentQueryParams
    ) -> PaginationCarrier[EvaluationAssignmentViewModel]:
        """
        获取自评的评价分配列表
        :param params:
        :return:
        """
        sql = """
        with people_team as (
        SELECT team_id, people_id FROM sv_current_team_member 
        WHERE people_id = :people_id
        GROUP BY team_id, people_id
        ), evaluation_assignment as (
        SELECT DISTINCT ea.id, ea.evaluation_criteria_plan_id, bin.plan_name, 
        bin.executed_start_at, bin.executed_finish_at, bin.plan_status,
        bin.evaluation_criteria_name, bin.evaluation_object_category,
        ea.effected_id, ea.effected_category, bin.evaluation_criteria_id,
        isl.id as input_score_log_id, isl.filler_id, isl.expected_filler_category,
        isl.expected_filler_id, bin.benchmark_id, bin.benchmark_name
        FROM mv_benchmark_input_node bin
        INNER JOIN st_input_score_log isl on isl.benchmark_input_node_id = bin.id 
        INNER JOIN cv_evaluation_assignment ea on ea.id = isl.evaluation_assignment_id
        and bin.plan_id = ea.evaluation_criteria_plan_id
        INNER JOIN st_establishment_assign se on se.id = isl.expected_filler_id
        and isl.expected_filler_category = 'ESTABLISHMENT_ASSIGN'
        WHERE se.people_id = :people_id
        and bin.focus_period_id = :focus_period_id
        and bin.filler_calc_method = :filler_calc_method
        UNION ALL
        SELECT DISTINCT ea.id, ea.evaluation_criteria_plan_id, bin.plan_name, 
        bin.executed_start_at, bin.executed_finish_at, bin.plan_status,
        bin.evaluation_criteria_name, bin.evaluation_object_category,
        ea.effected_id, ea.effected_category, bin.evaluation_criteria_id,
        isl.id as input_score_log_id, isl.filler_id, isl.expected_filler_category,
        isl.expected_filler_id, bin.benchmark_id, bin.benchmark_name
        FROM mv_benchmark_input_node bin
        INNER JOIN st_input_score_log isl on bin.id = isl.benchmark_input_node_id
        INNER JOIN cv_evaluation_assignment ea on ea.id = isl.evaluation_assignment_id
        and bin.plan_id = ea.evaluation_criteria_plan_id
        INNER JOIN st_team_history st on st.id = isl.expected_filler_id
        and isl.expected_filler_category = 'TEAM'
        and bin.compare_at BETWEEN st.begin_at and st.end_at
        INNER JOIN st_team_member tm on st.id = tm.team_id
        and bin.compare_at BETWEEN tm.start_at and tm.finish_at
        WHERE bin.focus_period_id = :focus_period_id
        and bin.filler_calc_method = :filler_calc_method
        and tm.people_id = :people_id
        ), current_evaluation_assignment as (
        SELECT DISTINCT ea.id, ea.evaluation_criteria_plan_id, ea.plan_name, 
        ea.executed_start_at, ea.executed_finish_at, bin.plan_status,
        ea.evaluation_criteria_name, ea.evaluation_object_category,
        ea.effected_id, ea.effected_category, ea.evaluation_criteria_id,
        isl.id as input_score_log_id, isl.filler_id
        FROM evaluation_assignment ea 
        INNER JOIN st_input_score_log isl on ea.id = isl.evaluation_assignment_id
        INNER JOIN st_establishment_assign se on se.id = isl.expected_filler_id
        and isl.expected_filler_category = 'ESTABLISHMENT_ASSIGN'
        INNER JOIN mv_benchmark_input_node bin on isl.benchmark_input_node_id = bin.id 
        and bin.plan_id = ea.evaluation_criteria_plan_id
        WHERE se.people_id = :people_id
        and bin.filler_calc_method = :filler_calc_method
        UNION ALL
        SELECT DISTINCT ea.id, ea.evaluation_criteria_plan_id, ea.plan_name, 
        ea.executed_start_at, ea.executed_finish_at, bin.plan_status,
        ea.evaluation_criteria_name, ea.evaluation_object_category,
        ea.effected_id, ea.effected_category, ea.evaluation_criteria_id,
        isl.id as input_score_log_id, isl.filler_id
        FROM evaluation_assignment ea 
        INNER JOIN st_input_score_log isl on ea.id = isl.evaluation_assignment_id
        INNER JOIN people_team pt on pt.team_id = isl.expected_filler_id
        and isl.expected_filler_category = 'TEAM'
        INNER JOIN mv_benchmark_input_node bin on isl.benchmark_input_node_id = bin.id 
        and bin.plan_id = ea.evaluation_criteria_plan_id
        WHERE bin.filler_calc_method = :filler_calc_method
        ), evaluation_assignment_effected as (
        SELECT ea.*, sp.name as people_name, sd.name as dept_name,
        sp.name || '（' || parent.name || '/' || sd.name || '）' as effected_name  
        FROM current_evaluation_assignment ea 
        inner join ( select *,LEAST(handled_at, executed_finish_at) as least_time 
        from st_evaluation_criteria_plan) cp on cp.id=ea.evaluation_criteria_plan_id
        INNER JOIN st_establishment_assign sea on ea.effected_id = sea.id 
        and ea.effected_category = :effected_category
        INNER JOIN st_people_history sp on sea.people_id = sp.id and (
        ((cp.status=:ABOLISHED or (cp.status!=:DRAFT and cp.executed_finish_at<now())
        ) and (least_time BETWEEN sp.begin_at and sp.end_at)) or 
        ((cp.status=:DRAFT or (cp.status!=:ABOLISHED and cp.executed_finish_at>now())
        ) and sp.end_at>now()))
        INNER JOIN st_establishment se on sea.establishment_id = se.id 
        INNER JOIN st_capacity sc on se.capacity_id = sc.id
        INNER JOIN st_dimension_dept_tree ddt on se.dimension_dept_tree_id = ddt.id 
        INNER JOIN st_dept_history sd on ddt.dept_id = sd.id and (
        ((cp.status=:ABOLISHED or (cp.status!=:DRAFT and cp.executed_finish_at<now())
        ) and (least_time BETWEEN sd.begin_at and sd.end_at)) or 
        ((cp.status=:DRAFT or (cp.status!=:ABOLISHED and cp.executed_finish_at>now())
        ) and sd.end_at>now()))
        INNER JOIN st_dept_history parent on ddt.parent_dept_id = parent.id and (
        ((cp.status=:ABOLISHED or (cp.status!=:DRAFT and cp.executed_finish_at<now())
        ) and (least_time BETWEEN parent.begin_at and parent.end_at)) or 
        ((cp.status=:DRAFT or (cp.status!=:ABOLISHED and cp.executed_finish_at>now())
        ) and parent.end_at>now()))
        ) SELECT eae.id, eae.evaluation_criteria_plan_id, eae.plan_name, eae.executed_start_at, 
        eae.executed_finish_at, eae.evaluation_criteria_id, eae.evaluation_criteria_name,
        eae.effected_name, eae.evaluation_object_category, eae.people_name, eae.dept_name,
        eae.plan_status,
        COUNT(isl.id) FILTER (WHERE isl.filler_id IS NULL) AS not_fill_count,
        cast(COUNT(isl.id) FILTER (WHERE isl.filler_id IS NULL) as VARCHAR) as not_fill_count_text,
        COUNT(isl.id) FILTER (WHERE isl.filler_id = :people_id) AS fill_count,
        cast(COUNT(isl.id) FILTER (WHERE isl.filler_id = :people_id) as VARCHAR) as fill_count_text
        FROM evaluation_assignment_effected eae 
        INNER JOIN st_input_score_log isl on eae.input_score_log_id = isl.id
        where 1=1
        """
        if len(params.evaluation_object_category_list) > 0:
            sql += (
                " and eae.evaluation_object_category = any(array[:evaluation_object_category_list])"
            )
        if len(params.plan_status_list) > 0:
            sql += (
                " and eae.plan_status = any(array[:plan_status_list])"
            )
        sql += """
        GROUP BY eae.id, eae.evaluation_criteria_plan_id, eae.plan_name, eae.executed_start_at, 
        eae.executed_finish_at, eae.evaluation_criteria_id, eae.evaluation_criteria_name,
        eae.effected_name, eae.evaluation_object_category, eae.people_name, eae.dept_name,
        eae.plan_status
        """
        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=[
                "plan_name",
                "evaluation_criteria_name",
                "effected_name",
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
                "filler_calc_method": BenchmarkInputNodeFillerCalcMethod.SELF_BENCHMARK.value,
                "effected_category": EnumEvaluationAssignmentEffectedCategory.ESTABLISHMENT_ASSIGN.name,
                "people_id": params.people_id,
                "evaluation_object_category_list": params.evaluation_object_category_list,
                "focus_period_id": params.focus_period_id,
                "ABOLISHED": EnumEvaluationCriteriaPlanStatus.ABOLISHED.name,
                "DRAFT": EnumEvaluationCriteriaPlanStatus.DRAFT.name,
            },
        )
        return self._paginate(
            result_type=EvaluationAssignmentViewModel,
            total_params=page_init_params,
            page_params=params,
        )

    def get_evaluation_assignment_list_by_plan_id(
        self, evaluation_criteria_plan_id: str
    ) -> List[EvaluationAssignmentModel]:
        """
        根据评价标准计划id获取评价分配列表
        :param evaluation_criteria_plan_id:
        :return:
        """
        sql = """
        SELECT * FROM st_evaluation_assignment 
        WHERE finish_at > now() and evaluation_criteria_plan_id = :evaluation_criteria_plan_id
        """
        return self._fetch_all_to_model(
            model_cls=EvaluationAssignmentModel,
            sql=sql,
            params={"evaluation_criteria_plan_id": evaluation_criteria_plan_id},
        )

    def get_affected_benchmark_by_evaluation_assignment_id_and_benchmark_id(
        self, evaluation_assignment_id: str, benchmark_id: str
    ) -> List[BenchmarkModel]:
        """
        获取影响到的 benchmark 通过评价分配id和 改变的benchmark id
        :param evaluation_assignment_id:
        :param benchmark_id:
        :return:
        """
        sql = """
        select b.* from st_evaluation_assignment ea 
        INNER JOIN st_evaluation_criteria_plan cp on cp.id=ea.evaluation_criteria_plan_id
        INNER JOIN sv_current_evaluation_criteria_tree ct 
        on ct.evaluation_criteria_id=cp.evaluation_criteria_id
        INNER JOIN st_benchmark b on b.indicator_id=ct.id
        INNER JOIN st_benchmark_execute_node en on en.benchmark_id=b.id
        INNER JOIN st_benchmark_input_node io on en.id=io.benchmark_execute_node_id
        where b.finish_at >= now() and io.finish_at>=now() 
        and ea.id=:evaluation_assignment_id and io.source_benchmark_id=:benchmark_id 
        """
        return self._fetch_all_to_model(
            model_cls=BenchmarkModel,
            sql=sql,
            params={
                "evaluation_assignment_id": evaluation_assignment_id,
                "benchmark_id": benchmark_id,
            },
        )

    def fetch_evaluation_assignment_by_plan_ids(self, plan_ids: List[str]) -> List[EvaluationAssignmentModel]:
        """
        获取某个benchmark还在执行中的评价分配
        """
        sql = """
        select * from st_evaluation_assignment
        where evaluation_criteria_plan_id = any(array[:plan_ids])
        and now() between start_at and finish_at
        """
        return self._fetch_all_to_model(
            model_cls=EvaluationAssignmentModel,
            sql=sql,
            params={
                "plan_ids": plan_ids,
            },
        )
