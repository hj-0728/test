from typing import List

from infra_basic.basic_repository import BasicRepository

from backend.model.edit.command_generate_input_score_log_em import EnumTriggerCategory
from backend.model.view.assignment_input_score_log_vm import AssignmentInputScoreLogViewModel
from backend.model.view.benchmark_plan_vm import BenchmarkPlanViewModel
from domain_evaluation.model.evaluation_criteria_plan_model import EnumEvaluationCriteriaPlanStatus


class AppInputScoreLogRepository(BasicRepository):
    def fetch_benchmark_plan_list(
        self, trigger_category: str, trigger_ids: List[str]
    ) -> List[BenchmarkPlanViewModel]:
        """
        获取基准计划列表
        :param trigger_category: 过滤的名称，如team_category_id，subject_id
        :param trigger_ids: 过滤的值，team_category_id、subject_id对应的值具体是什么
        :return:
        """
        if trigger_category == EnumTriggerCategory.CONTEXT_SYNC.name:
            # 上下文同步之需要更新班主任填写的那部分基准
            filler_calc_sql = """ and sin.filler_calc_method = 'HeadTeacherBenchmark'"""
        else:
            filler_calc_sql = """ and filler_calc_context ->> :trigger_category = any(array[:trigger_ids])"""
        sql = f"""
        select benchmark_id, sin.id as benchmark_input_node_id, sin.filler_calc_method,
        json_agg(row_to_json(sp.*)) as plan_list
        from st_benchmark_input_node sin
        inner join st_benchmark_execute_node sen on sen.id = sin.benchmark_execute_node_id
        inner join st_benchmark sb on sb.id = sen.benchmark_id
        inner join st_evaluation_criteria_tree st on st.indicator_id = sb.indicator_id
        inner join st_evaluation_criteria_plan sp on sp.evaluation_criteria_id = st.evaluation_criteria_id
        and sp.status = :published and executed_finish_at > now()
        where sin.finish_at = 'infinity'
        {filler_calc_sql}
        and st.finish_at = 'infinity'
        group by benchmark_id, sin.id
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=BenchmarkPlanViewModel,
            params={
                "trigger_category": trigger_category,
                "trigger_ids": trigger_ids,
                "published": EnumEvaluationCriteriaPlanStatus.PUBLISHED.name,
            },
        )

    def fetch_evaluation_assignment(
        self, plan_ids: List[str], input_node_id: str
    ) -> List[AssignmentInputScoreLogViewModel]:
        """
        获取评价分配
        """
        sql = """
        select row_to_json(sa.*) as evaluation_assignment, row_to_json(sl.*) as input_score_log
        from st_evaluation_assignment sa
        left join st_input_score_log sl on sl.evaluation_assignment_id = sa.id
        and sl.benchmark_input_node_id = :input_node_id
        where evaluation_criteria_plan_id = any(array[:plan_ids])
        and sa.finish_at = 'infinity'
        and (sl.id is null or sl.filled_at is null)
        """
        return self._fetch_all_to_model(
            model_cls=AssignmentInputScoreLogViewModel,
            sql=sql,
            params={"plan_ids": plan_ids, "input_node_id": input_node_id},
        )
