from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import PageInitParams, OrderCondition

from backend.data.query_params.plan_progress_detail_query_params import \
    PlanProgressDetailQueryParams
from backend.data.query_params.plan_ranking_query_params import PlanRankingQueryParams
from backend.model.edit.plan_statistics_filter_dept_tree_em import \
    PlanStatisticsFilterDeptTreeEditModel
from backend.model.view.benchmark_vm import BenchmarkVm
from backend.model.view.dimension_dept_tree_info_vm import DimensionDeptTreeInfoVm
from backend.model.view.indicator_tree_vm import IndicatorTreeVm
from backend.model.view.plan_benchmark_statistics_vm import \
    PlanClassBenchmarkStatisticsVm, PlanStudentBenchmarkStatisticsVm, \
    PlanRankingBenchmarkStatisticsVm, PlanProgressDetailVm
from backend.model.view.plan_statistics_vm import PlanStatusCountVm
from context_sync.data.enum import EnumFileRelationship
from domain_evaluation.model.evaluation_assignment_model import \
    EnumEvaluationAssignmentEffectedCategory
from domain_evaluation.model.evaluation_criteria_plan_model import \
    EnumEvaluationCriteriaPlanStatus
from domain_evaluation.model.evaluation_criteria_plan_scope_model import \
    EnumGroupCategory
from domain_evaluation.model.todo_task_model import EnumTodoTaskTriggerCategory
from edu_binshi.model.view.dept_tree_vm import DeptTreeViewModel
from infra_backbone.model.dept_model import DeptModel
from infra_backbone.model.people_model import PeopleModel


class EvaluationCriteriaPlanStatisticsRepository(BasicRepository):
    """
    评价标准计划统计 repository
    """

    def get_evaluation_criteria_plan_indicator_by_plan_id(
        self, evaluation_criteria_plan_id: str
    ) -> List[IndicatorTreeVm]:
        """
        通过计划 id 获取评价计划标准指标tree
        :param evaluation_criteria_plan_id:
        :return:
        """

        sql = """
        select i.*,ct.parent_indicator_id,ct.seq
        from st_evaluation_criteria_plan cp
        INNER JOIN st_evaluation_criteria ec on ec.id=cp.evaluation_criteria_id
        INNER JOIN st_evaluation_criteria_tree ct on ct.evaluation_criteria_id=ec.id
        and cp.executed_finish_at <= ct.finish_at and cp.executed_finish_at>ct.start_at
        INNER JOIN st_indicator i on i.id=ct.indicator_id
        where cp.id=:evaluation_criteria_plan_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=IndicatorTreeVm,
            params={"evaluation_criteria_plan_id": evaluation_criteria_plan_id},
        )

    def get_evaluation_criteria_plan_indicator_benchmark(
        self, evaluation_criteria_plan_id: str, indicator_id: str
    ) -> List[BenchmarkVm]:
        """
        获取评价计划标准指标的基准值
        :param evaluation_criteria_plan_id:
        :param indicator_id:
        :return:
        """

        sql = """
        select b.* , ss.name as score_symbol_name,value_type,string_options
        from st_indicator i 
        INNER JOIN st_benchmark b on i.id=b.indicator_id
        INNER JOIN st_evaluation_criteria_plan cp 
        on cp.executed_finish_at<=b.finish_at and cp.executed_finish_at>b.start_at
        INNER JOIN st_score_symbol ss on b.benchmark_strategy_params->>'scoreSymbolId'=ss.id
        where i.id=:indicator_id and cp.id=:evaluation_criteria_plan_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=BenchmarkVm,
            params={
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
                "indicator_id": indicator_id,
            },
        )

    def get_evaluation_criteria_plan_dept_grade_scope(
        self, evaluation_criteria_plan_id: str, dimension_id: str
    ) -> List[DimensionDeptTreeInfoVm]:
        """
        获取评价计划标准的部门年级范围
        :param evaluation_criteria_plan_id:
        :param dimension_id:
        :return:
        """

        sql = """
        select DISTINCT dp.*,dtp.parent_dept_id,dtp.seq,dtp.id as dimension_dept_tree_id
        from st_evaluation_criteria_plan_scope s 
        INNER JOIN st_evaluation_criteria_plan p on p.id=s.evaluation_criteria_plan_id
        and s.finish_at>=p.executed_finish_at
        INNER JOIN st_dept d on d.id=s.scope_id
        INNER JOIN st_dimension_dept_tree dt on dt.dept_id=d.id 
        and (dt.finish_at>=p.executed_finish_at and dt.start_at<p.executed_finish_at)
        INNER JOIN st_dept dp on dp.id=dt.parent_dept_id
        LEFT JOIN st_dimension_dept_tree dtp on dtp.dept_id=dp.id 
        and (dtp.finish_at>=p.executed_finish_at and dtp.start_at<=p.executed_finish_at)
        where scope_category=:scope_category and p.id=:evaluation_criteria_plan_id 
        and dt.dimension_id=:dimension_id and dtp.dimension_id=:dimension_id
        ORDER BY dtp.parent_dept_id,dtp.seq
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=DimensionDeptTreeInfoVm,
            params={
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
                "dimension_id": dimension_id,
                "scope_category": EnumGroupCategory.DEPT.name,
            },
        )

    def get_evaluation_criteria_plan_grade_class_scope(
        self, evaluation_criteria_plan_id: str, grade_dept_id: str, dimension_id: str
    ) -> List[DimensionDeptTreeInfoVm]:
        """
        获取评价计划部门年级下的班级范围
        :param evaluation_criteria_plan_id:
        :param grade_dept_id:
        :param dimension_id:
        :return:
        """

        sql = """
        select DISTINCT d.*,dt.parent_dept_id,dt.seq,dt.id as dimension_dept_tree_id
        from st_evaluation_criteria_plan_scope s 
        INNER JOIN st_evaluation_criteria_plan p on p.id=s.evaluation_criteria_plan_id
        and s.finish_at>=p.executed_finish_at
        INNER JOIN st_dept d on d.id=s.scope_id
        INNER JOIN st_dimension_dept_tree dt on dt.dept_id=d.id 
        and (dt.finish_at>=p.executed_finish_at and dt.start_at<p.executed_finish_at)
        where scope_category=:scope_category and p.id=:evaluation_criteria_plan_id 
        and dt.dimension_id=:dimension_id and dt.parent_dept_id=:grade_dept_id
        ORDER BY dt.parent_dept_id,dt.seq
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=DimensionDeptTreeInfoVm,
            params={
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
                "grade_dept_id": grade_dept_id,
                "dimension_id": dimension_id,
                "scope_category": EnumGroupCategory.DEPT.name,
            },
        )

    def get_evaluation_criteria_plan_class_student_scope(
        self, evaluation_criteria_plan_id: str, class_dept_id: str
    ) -> List[PeopleModel]:
        """
        获取评价计划班级下的学生范围
        :param evaluation_criteria_plan_id:
        :param class_dept_id:
        :return:
        """

        sql = """
        select sp.*
        from st_evaluation_criteria_plan p 
        INNER JOIN st_evaluation_assignment ea on ea.evaluation_criteria_plan_id=p.id
        and ea.finish_at>=p.executed_finish_at
        INNER JOIN st_establishment_assign a on a.id=ea.effected_id
        INNER JOIN st_establishment e on e.id=a.establishment_id
        INNER JOIN st_dimension_dept_tree dt on dt.id=e.dimension_dept_tree_id
        INNER JOIN st_people sp on sp.id=a.people_id
        where dt.dept_id=:class_dept_id_list
        and p.id=:evaluation_criteria_plan_id
        order by sp.name
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=PeopleModel,
            params={
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
                "class_dept_id_list": class_dept_id,
            },
        )

    def get_plan_class_benchmark_statistics(
        self,
        evaluation_criteria_plan_id: str,
        dimension_dept_tree_id_list: Optional[List[str]],
        benchmark_id: str,
        dimension_id: str,
    ) -> List[PlanClassBenchmarkStatisticsVm]:
        """
        获取评价计划班级基准值统计
        :param evaluation_criteria_plan_id:
        :param dimension_dept_tree_id_list:
        :param benchmark_id:
        :param dimension_id:
        :return:
        """

        sql = """
        WITH RECURSIVE dept_tree AS (
        SELECT sdt.id AS dimension_dept_tree_id, sd.id, sd.name,sdt.seq
        FROM st_dimension_dept_tree sdt
        INNER JOIN st_dept sd ON sd.id = sdt.dept_id
        INNER JOIN st_dimension sdn ON sdn.id = sdt.dimension_id
        INNER JOIN st_evaluation_criteria_plan cp on cp.executed_finish_at>sdt.start_at
        and cp.executed_finish_at<=sdt.finish_at
        WHERE sdn.id =:dimension_id
        and cp.id=:evaluation_criteria_plan_id
        """
        if dimension_dept_tree_id_list:
            sql += " and sdt.id=any(array[:dimension_dept_tree_id_list]) "
        else:
            sql += " and sdt.parent_dept_id IS NULL "
        sql += """ UNION ALL
        SELECT sdt.id AS dimension_dept_tree_id, sd.id, sd.name,sdt.seq
        FROM st_dimension_dept_tree sdt
        INNER JOIN st_dept sd ON sd.id = sdt.dept_id
        INNER JOIN st_dimension sdn ON sdn.id = sdt.dimension_id
        JOIN dept_tree t ON t.id = sdt.parent_dept_id
        INNER JOIN st_evaluation_criteria_plan cp on cp.executed_finish_at>sdt.start_at
        and cp.executed_finish_at<=sdt.finish_at
        where cp.id=:evaluation_criteria_plan_id
        )
        , dept_score as (
        select d.*,t.seq,ea.id as evaluation_assignment_id,bs.numeric_score,bs.string_score
        from st_evaluation_criteria_plan p 
        INNER JOIN st_evaluation_assignment ea on ea.evaluation_criteria_plan_id=p.id
        and ea.finish_at>=p.executed_finish_at
        INNER JOIN st_establishment_assign a on a.id=ea.effected_id
        INNER JOIN st_establishment e on e.id=a.establishment_id
        INNER JOIN st_dimension_dept_tree dt on dt.id=e.dimension_dept_tree_id
        INNER JOIN st_dept d on d.id=dt.dept_id
        INNER JOIN st_benchmark_score bs on bs.evaluation_assignment_id=ea.id
        INNER JOIN dept_tree t on t.id=d.id
        where p.id=:evaluation_criteria_plan_id and bs.benchmark_id=:benchmark_id
        )
        , numeric_avg as (
        select id,seq,avg( COALESCE(numeric_score,0)) as numeric_avg 
        from dept_score 
        GROUP BY id,seq
        )
        , numeric_distributed as (
        select id,seq,json_agg(json_build_object('numeric_score',nd.numeric_score, 'count',nd.count)) as numeric_distributed
        from (select id,seq,numeric_score,count(evaluation_assignment_id) from dept_score GROUP BY id,seq,numeric_score) nd
        GROUP BY id,seq
        )
        ,string_distributed as (
        select id,seq,json_agg(json_build_object('string_score',sd.string_score, 'count',sd.count)) as string_distributed
        from (
        select id,seq,string_score,count(evaluation_assignment_id) from dept_score GROUP BY id,seq,string_score) sd
        GROUP BY id,seq
        )
        , dept as (
        select id,seq,name,count(evaluation_assignment_id) as all_student from dept_score GROUP BY id,name,seq
        )
        select d.id,d.seq,d.name,d.all_student,na.numeric_avg,
        nd.numeric_distributed,sd.string_distributed
        from dept d 
        left JOIN numeric_avg na on na.id=d.id
        left join numeric_distributed nd on nd.id=d.id
        left join string_distributed sd on sd.id=d.id
        order by d.seq desc,d.name desc
        """

        return self._fetch_all_to_model(
            sql=sql,
            params={
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
                "dimension_dept_tree_id_list": dimension_dept_tree_id_list,
                "benchmark_id": benchmark_id,
                "dimension_id": dimension_id,
            },
            model_cls=PlanClassBenchmarkStatisticsVm,
        )

    def get_plan_ranking_benchmark_statistics(
        self,
        params: PlanRankingQueryParams,
        string_options: Optional[List[str]],
    ) -> PaginationCarrier[PlanRankingBenchmarkStatisticsVm]:
        """
        获取评价计划基准值排行榜 根据班级
        :param params:
        :param string_options:
        :return:
        """

        sql = """
        with score as (
        select sp.*,ea.id as evaluation_assignment_id,bs.numeric_score,bs.string_score,
        dp.name||'/'||d.name as dept_name, r.file_id
        from st_evaluation_criteria_plan p 
        INNER JOIN st_evaluation_assignment ea on ea.evaluation_criteria_plan_id=p.id
        and ea.finish_at>=p.executed_finish_at
        INNER JOIN st_establishment_assign a on a.id=ea.effected_id
        INNER JOIN st_establishment e on e.id=a.establishment_id
        INNER JOIN st_dimension_dept_tree dt on dt.id=e.dimension_dept_tree_id
        INNER JOIN st_dept d on d.id=dt.dept_id
        INNER JOIN st_dept dp on dp.id=dt.parent_dept_id
        INNER JOIN st_benchmark_score bs on bs.evaluation_assignment_id=ea.id
        INNER JOIN st_people sp on sp.id=a.people_id
        left join st_file_relationship r on r.res_id=sp.id and relationship=:relationship
        where p.id=:evaluation_criteria_plan_id and bs.benchmark_id=:benchmark_id
        """

        if params.dimension_dept_tree_id_list:
            sql += " and dt.id=any(array[:dimension_dept_tree_id_list]) "

        sql += ")"

        if string_options:
            sql += """
            select s.* from score s 
            left join (select unnest(array[:string_options]) AS string_score,
            generate_series(1, array_length(array[:string_options], 1)) AS array_index) o
            on s.string_score=o.string_score
            order by o.array_index,s.dept_name,s.name
            """
        else:
            sql += " select * from score order by numeric_score desc,dept_name,name "

        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["people_name"],
            params={
                "evaluation_criteria_plan_id": params.evaluation_criteria_plan_id,
                "dimension_dept_tree_id_list": params.dimension_dept_tree_id_list,
                "benchmark_id": params.benchmark_id,
                "string_options": string_options,
                "relationship": EnumFileRelationship.AVATAR.name,
            },
        )
        return self._paginate(
            result_type=PlanRankingBenchmarkStatisticsVm,
            total_params=page_init_params,
            page_params=params,
        )

    def get_plan_student_benchmark_statistics(
        self,
        evaluation_criteria_plan_id: str,
        benchmark_id: str,
    ) -> List[PlanStudentBenchmarkStatisticsVm]:
        """
        获取评价计划学生基准值统计 根据学生id
        :param evaluation_criteria_plan_id:
        :param benchmark_id:
        :return:
        """

        sql = """
        select bs.numeric_score,bs.string_score,count(ea.id)
        from st_evaluation_criteria_plan p 
        INNER JOIN st_evaluation_assignment ea on ea.evaluation_criteria_plan_id=p.id
        and ea.finish_at>=p.executed_finish_at
        INNER JOIN st_benchmark_score bs on bs.evaluation_assignment_id=ea.id
        where p.id=:evaluation_criteria_plan_id and bs.benchmark_id=:benchmark_id
        group by bs.numeric_score,bs.string_score
        """

        return self._fetch_all_to_model(
            sql=sql,
            params={
                "evaluation_criteria_plan_id": evaluation_criteria_plan_id,
                "benchmark_id": benchmark_id,
            },
            model_cls=PlanStudentBenchmarkStatisticsVm,
        )

    def get_in_progress_plan_progress_detail(
        self, params: PlanProgressDetailQueryParams
    ) -> PaginationCarrier[PlanProgressDetailVm]:
        """
        获取进行中计划进展详情
        :param params:
        :return:
        """

        sql = """
        with evaluation_criteria_plan as (
        SELECT id, :published_status as plan_status
        FROM st_evaluation_criteria_plan
        WHERE status = :published_status AND now() > executed_start_at
        and now() <= executed_finish_at
        and focus_period_id=:period_id
        ), progress as (
        select ea.evaluation_criteria_plan_id, ecp.plan_status,
        COUNT(*) FILTER (WHERE filled_at IS NULL) AS unfinished_count,
        COUNT(*) FILTER (WHERE filled_at IS NOT NULL) AS finished_count,
        COUNT(*) as input_count,
        count(DISTINCT ea.id) as all_student,
        count(DISTINCT ea.id) FILTER (WHERE filled_at IS NULL) as unfinished_student_count
        from  sv_current_evaluation_assignment ea
        INNER JOIN evaluation_criteria_plan ecp on ea.evaluation_criteria_plan_id = ecp.id
        INNER JOIN st_input_score_log sl on sl.evaluation_assignment_id=ea.id
        INNER JOIN mv_benchmark_input_node bin on sl.benchmark_input_node_id = bin.id 
        and bin.plan_id = ecp.id
        GROUP BY ea.evaluation_criteria_plan_id, ecp.plan_status
        ), plan_todo as (
        select trigger_id as plan_id,count(distinct title) as todo_count
        from st_todo_task
        where completed_at is null and trigger_category=:trigger_category
        GROUP BY trigger_id
        )
        select cp.id, cp.name, cp.executed_start_at, p.plan_status as status, 
        coalesce(finished_count, 0) as finished_count,
        coalesce(unfinished_count, 0) as unfinished_count,
        coalesce(input_count, 0) as input_count,coalesce(all_student, 0) as all_student,
        coalesce(unfinished_student_count, 0) as unfinished_student_count,
        coalesce(todo_count, 0) as todo_count
        from st_evaluation_criteria_plan cp 
        inner join progress p on cp.id=p.evaluation_criteria_plan_id
        left join plan_todo pd on pd.plan_id=cp.id
        """

        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["name"],
            order_columns=[OrderCondition(
                column_name="executed_start_at",
                order="desc",
            )],
            params={
                "period_id": params.period_id,
                "published_status": EnumEvaluationCriteriaPlanStatus.PUBLISHED.name,
                "trigger_category": EnumTodoTaskTriggerCategory.EVALUATION_CRITERIA_PLAN.name,
            },
        )
        return self._paginate(
            result_type=PlanProgressDetailVm,
            total_params=page_init_params,
            page_params=params,
        )

    def get_to_be_started_plan_progress_detail(
        self, params: PlanProgressDetailQueryParams
    ) -> PaginationCarrier[PlanProgressDetailVm]:
        """
        获取待开始计划进展详情
        :param params:
        :return:
        """

        sql = """
        with evaluation_criteria_plan as (
        SELECT id, :published_status as plan_status
        FROM st_evaluation_criteria_plan
        WHERE status = :published_status AND now() < executed_start_at
        and focus_period_id=:period_id
        ), plan_todo as (
        select trigger_id as plan_id,count(distinct title) as todo_count
        from st_todo_task
        where completed_at is null and trigger_category=:trigger_category
        GROUP BY trigger_id
        )
        select cp.id, cp.name, cp.executed_start_at, p.plan_status as status,
        coalesce(todo_count, 0) as todo_count
        from st_evaluation_criteria_plan cp 
        inner join evaluation_criteria_plan p on p.id=cp.id
        left join plan_todo pd on pd.plan_id=cp.id
        """

        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["name"],
            order_columns=[OrderCondition(
                column_name="executed_start_at",
                order="desc",
            )],
            params={
                "period_id": params.period_id,
                "published_status": EnumEvaluationCriteriaPlanStatus.PUBLISHED.name,
                "trigger_category": EnumTodoTaskTriggerCategory.EVALUATION_CRITERIA_PLAN.name,
            },
        )
        return self._paginate(
            result_type=PlanProgressDetailVm,
            total_params=page_init_params,
            page_params=params,
        )

    def get_plan_status_count(self, period_id: str) -> List[PlanStatusCountVm]:
        """
        获取计划状态统计 暂时先统计已归档、已发布
        :param period_id:
        :return:
        """

        sql = """
        with evaluation_criteria_plan as (
        SELECT id, :archived_status AS status
        FROM st_evaluation_criteria_plan
        WHERE ((status = :published_status and executed_finish_at < now())
        or status = :archived_status)
        and focus_period_id=:period_id
        UNION ALL
        SELECT id, :published_status as status
        FROM st_evaluation_criteria_plan
        WHERE status = :published_status AND now() > executed_start_at
        and now() <= executed_finish_at
        and focus_period_id=:period_id
        )
        select status,count(*) from evaluation_criteria_plan GROUP BY status
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=PlanStatusCountVm,
            params={
                "period_id": period_id,
                "published_status": EnumEvaluationCriteriaPlanStatus.PUBLISHED.name,
                "archived_status": EnumEvaluationCriteriaPlanStatus.ARCHIVED.name,
            },
        )

    def get_plan_ranking_filter_dept(
        self, params: PlanStatisticsFilterDeptTreeEditModel
    ) -> List[DeptTreeViewModel]:
        """
        获取评价排行过滤部门
        :param params:
        :return:
        """

        sql = f"""
        with tree as (
        select distinct sp2.* from st_evaluation_assignment sa1
        inner join st_establishment_assign sa2 
        on sa1.effected_category = :effected_category and sa1.effected_id = sa2.id
        inner join st_establishment se on se.id = sa2.establishment_id
        inner join st_dimension_dept_tree st on st.id = se.dimension_dept_tree_id
        inner join sv_k12_dimension_dept_tree_path sp on st.id = any(sp.tree_path)
        inner join sv_k12_dimension_dept_tree_path sp2 on sp2.id = any(sp.tree_path)
        where evaluation_criteria_plan_id = :plan_id
        and sa1.finish_at = 'infinity'
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
                "effected_category": EnumEvaluationAssignmentEffectedCategory.ESTABLISHMENT_ASSIGN.name,
            },
        )
