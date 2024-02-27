from datetime import datetime
from typing import List, Optional

from infra_basic.basic_repository import BasicRepository

from edu_binshi.model.view.evaluation_assignment_plan_vm import EvaluationAssignmentPlanViewModel
from edu_binshi.model.view.evaluation_criteria_tag_vm import EvaluationCriteriaTagViewModel
from edu_binshi.model.view.report_indicator_score_vm import (
    ReportIndicatorScoreViewModel,
    RootIndicatorScoreViewModel,
)


class ReportRepositoryV2(BasicRepository):
    def fetch_evaluation_assignment_plan(
        self, evaluation_assignment_id: str
    ) -> Optional[EvaluationAssignmentPlanViewModel]:
        """
        获取评价分配的计划
        """
        sql = """
        select sa.id as evaluation_assignment_id,sp.evaluation_criteria_id, sp.executed_finish_at,
        sh.name as criteria_name, sh.comments as criteria_comments, sdh.name as dept_name, sph.name as people_name
        from st_evaluation_assignment sa
        inner join st_evaluation_criteria_plan sp on sp.id = sa.evaluation_criteria_plan_id
        inner join st_evaluation_criteria_history sh on sh.id = sp.evaluation_criteria_id
        and sp.executed_finish_at between sh.begin_at and sh.end_at
        inner join st_establishment_assign sa2 on sa2.id = sa.effected_id and sa.effected_category = 'ESTABLISHMENT_ASSIGN'
        inner join st_people_history sph on sph.id = sa2.people_id
        and sp.executed_finish_at between sph.begin_at and sph.end_at
        inner join st_establishment se on se.id = sa2.establishment_id
        inner join st_dimension_dept_tree st on st.id = se.dimension_dept_tree_id
        inner join st_dept_history sdh on sdh.id = st.dept_id
        and sp.executed_finish_at between sdh.begin_at and sdh.end_at
        where sa.id = :evaluation_assignment_id
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=EvaluationAssignmentPlanViewModel,
            params={"evaluation_assignment_id": evaluation_assignment_id},
        )

    def fetch_report_indicator_data(
        self,
        evaluation_criteria_id: str,
        evaluation_assignment_id: str,
        executed_finish_at: datetime,
    ) -> List[ReportIndicatorScoreViewModel]:
        """
        获取报告指标相关数据
        这个sql比较长，查看思路：
        1.indicator_data：先找出哪些指标
        2.indicator_tree：构造树
        3.indicator_benchmark：找出指标相关的benchmark及得分
        """
        sql = """
        with recursive indicator_tree as (
        select i.id, i.name, i.parent_indicator_id, i.indicator_id, i.seq, array[i.seq] as seq_list, i.tag, 1 as level
        from indicator_data i
        where i.parent_indicator_id is null
        union all
        select i.id, i.name, i.parent_indicator_id, i.indicator_id, i.seq, array_append(it.seq_list, i.seq),
        i.tag, it.level + 1 
        from indicator_data i
        inner join indicator_tree it on i.parent_indicator_id = it.indicator_id
        ),
        indicator_data as (
        select st.*, sh.name, max(sth.name) as tag from st_evaluation_criteria_tree st
        inner join st_indicator_history sh on sh.id = st.indicator_id
        left join sv_tag_ownership_relationship_history sth on sth.resource_id = st.id
        and sth.resource_category = 'EVALUATION_CRITERIA_TREE' and sth.relationship = 'EVALUATION'
        and :executed_finish_at between sth.begin_at and sth.end_at
        where st.evaluation_criteria_id = :evaluation_criteria_id
        and :executed_finish_at between st.start_at and st.finish_at
        and :executed_finish_at between sh.begin_at and sh.end_at
        group by st.id, sh.name
        ),
        indicator_benchmark as (
        select it.indicator_id,
        array_to_json(array_agg(
        json_build_object('name', sb.name, 'numeric_score', ss.numeric_score, 'string_score', ss.string_score,
        'numericMaxScore', sb.benchmark_strategy_params ->> 'numericMaxScore', 'tag', sh.name,
        'source_category', sbs.source_category)
        )) as benchmark_list
        from indicator_tree it
        inner join st_benchmark sb on sb.indicator_id = it.indicator_id
        inner join st_benchmark_strategy sbs on sbs.id = sb.benchmark_strategy_id
        inner join sv_tag_ownership_relationship_history sh on sh.resource_id = sb.id
        and sh.resource_category = 'BENCHMARK' and sh.relationship = 'EVALUATION'
        left join st_benchmark_score ss on ss.evaluation_assignment_id = :evaluation_assignment_id
        and ss.benchmark_id = sb.id
        where sb.finish_at = 'infinity'
        and :executed_finish_at between sh.begin_at and sh.end_at
        group by it.indicator_id
        )
        select it.*, case when ib.benchmark_list is null then '[]' else ib.benchmark_list end as benchmark_list
        from indicator_tree it
        left join indicator_benchmark ib on it.indicator_id = ib.indicator_id
        where it.tag is not null
        order by seq_list
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=ReportIndicatorScoreViewModel,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
                "evaluation_assignment_id": evaluation_assignment_id,
                "executed_finish_at": executed_finish_at,
            },
        )

    def fetch_evaluation_criteria_tag(
        self, evaluation_criteria_id: str, executed_finish_at: datetime
    ) -> EvaluationCriteriaTagViewModel:
        """
        获取评价标准的标签
        """
        sql = """
        select count(st.*) as total_tag_count,
        count(st.*) filter (where st.parent_indicator_id is null) as root_tag_count
        from sv_tag_ownership_relationship_history sh
        inner join st_evaluation_criteria_tree st on sh.resource_id = st.id and sh.resource_category = 'EVALUATION_CRITERIA_TREE'
        and :executed_finish_at between st.start_at and st.finish_at
        and :executed_finish_at between sh.begin_at and sh.end_at
        and st.evaluation_criteria_id = :evaluation_criteria_id
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=EvaluationCriteriaTagViewModel,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
                "executed_finish_at": executed_finish_at,
            },
        )

    def fetch_criteria_tree_child_benchmark_tag(
        self, evaluation_criteria_id: str, executed_finish_at: datetime
    ) -> List[str]:
        """
        获取评价标准树下的基准标签
        """
        sql = """
        select distinct sh.name
        from st_evaluation_criteria_tree st
        inner join st_benchmark sb on sb.indicator_id = st.indicator_id and sb.finish_at = 'infinity'
        inner join sv_tag_ownership_relationship_history sh
        on sh.resource_id = sb.id and sh.resource_category = 'BENCHMARK'
        where st.evaluation_criteria_id = :evaluation_criteria_id
        and :executed_finish_at between st.start_at and st.finish_at
        and st.parent_indicator_id is not null
        """
        data_list = self._execute_sql(
            sql=sql,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
                "executed_finish_at": executed_finish_at,
            },
        )
        return [x["name"] for x in data_list]

    def fetch_root_indicator_benchmark_score(
        self,
        evaluation_assignment_id: str,
        evaluation_criteria_id: str,
        executed_finish_at: datetime,
    ) -> List[RootIndicatorScoreViewModel]:
        """
        获取根指标的基准得分
        """
        sql = """
        select si.name,
        array_to_json(array_agg(
        json_build_object('numeric_score', ss.numeric_score, 'string_score',ss.string_score,
        'name', sb.name, 'tag', sh.name)
        )) as benchmark_list
        from st_evaluation_criteria_tree st
        inner join st_indicator_history si on si.id = st.indicator_id
        inner join st_benchmark sb on sb.indicator_id = st.indicator_id and sb.finish_at = 'infinity'
        inner join sv_tag_ownership_relationship_history sh
        on sh.resource_id = sb.id and sh.resource_category = 'BENCHMARK'
        left join st_benchmark_score ss on ss.benchmark_id = sb.id
        and ss.evaluation_assignment_id = :evaluation_assignment_id
        where st.evaluation_criteria_id = :evaluation_criteria_id
        and :executed_finish_at between st.start_at and st.finish_at
        and :executed_finish_at between si.begin_at and si.end_at
        and st.parent_indicator_id is null
        group by si.name
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=RootIndicatorScoreViewModel,
            params={
                "evaluation_assignment_id": evaluation_assignment_id,
                "evaluation_criteria_id": evaluation_criteria_id,
                "executed_finish_at": executed_finish_at,
            },
        )
