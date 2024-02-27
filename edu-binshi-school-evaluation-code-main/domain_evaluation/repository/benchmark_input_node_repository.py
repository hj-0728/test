from typing import List, Optional

from infra_basic.basic_repository import BasicRepository

from domain_evaluation.model.benchmark_input_node_model import BenchmarkInputNodeSourceCategory, BenchmarkInputNodeModel
from domain_evaluation.model.view.benchmark_input_node_vm import BenchmarkInputNodeVm


class BenchmarkInputNodeRepository(BasicRepository):
    """
    基准的输入节点 repository
    """

    def get_benchmark_input_node_score_log(
        self, evaluation_assignment_id: str, people_id: str
    ) -> List[BenchmarkInputNodeVm]:
        """
        获取基准的输入节点的填写信息
        :param evaluation_assignment_id:
        :param people_id:
        :return:
        """
        sql = """
        with people_team as (
        SELECT team_id, people_id FROM sv_current_team_member 
        WHERE people_id = :people_id
        GROUP BY team_id, people_id
        ), current_input_score_log as (
        SELECT isl.benchmark_input_node_id, isl.id as input_score_log_id, 
        isl.version as input_score_log_version, isl.string_score, isl.numeric_score,
        isl.filler_id
        FROM st_input_score_log isl
        INNER JOIN st_establishment_assign se on se.id = isl.expected_filler_id
        and isl.expected_filler_category = 'ESTABLISHMENT_ASSIGN'
        WHERE se.people_id = :people_id
        and isl.evaluation_assignment_id = :evaluation_assignment_id
        UNION ALL
        SELECT isl.benchmark_input_node_id, isl.id as input_score_log_id, 
        isl.version as input_score_log_version, isl.string_score, isl.numeric_score,
        isl.filler_id
        FROM st_input_score_log isl
        INNER JOIN people_team pt on pt.team_id = isl.expected_filler_id
        and isl.expected_filler_category = 'TEAM'
        WHERE isl.evaluation_assignment_id = :evaluation_assignment_id
        ) SELECT DISTINCT bin.benchmark_id, bin.benchmark_name, bin.numeric_max_score,
        bin.numeric_min_score, bin.limited_string_options,
        bin.score_symbol_name, bin.score_symbol_code, bin.score_symbol_value_type, 
        bin.score_symbol_numeric_precision, bin.score_symbol_string_options,
        bin.indicator_id, bin.filler_calc_method, bin.benchmark_source_category,
        isl.input_score_log_id, 
        isl.input_score_log_version, isl.string_score, isl.numeric_score,
        CASE WHEN (bin.limited_string_options IS NOT NULL) THEN isl.string_score
        WHEN (bin.numeric_max_score IS NOT NULL OR bin.numeric_min_score IS NOT NULL) 
        THEN cast(round(isl.numeric_score, bin.score_symbol_numeric_precision) as VARCHAR)
        END AS score_result,
        CASE WHEN (isl.filler_id IS NOT NULL and isl.filler_id = :people_id) THEN TRUE
        WHEN (isl.filler_id IS NULL) THEN TRUE
        ELSE FALSE END AS can_view
        FROM mv_benchmark_input_node bin
        INNER JOIN current_input_score_log isl on isl.benchmark_input_node_id = bin.id
        WHERE bin.source_category = :source_category
        """
        return self._fetch_all_to_model(
            model_cls=BenchmarkInputNodeVm,
            sql=sql,
            params={
                "evaluation_assignment_id": evaluation_assignment_id,
                "source_category": BenchmarkInputNodeSourceCategory.INPUT.name,
                "people_id": people_id,
            },
        )

    def fetch_benchmark_input_node_source_category(self, benchmark_id: str) -> Optional[str]:
        """
        获取基准输入节点的来源类型
        """
        sql = """
        select distinct sin.source_category
        from st_benchmark_execute_node sen
        inner join st_benchmark_input_node sin on sen.id = sin.benchmark_execute_node_id
        where sen.benchmark_id = :benchmark_id
        """
        data = self._execute_sql(
            sql=sql, params={"benchmark_id": benchmark_id},
        )
        return data[0]["source_category"] if data else None

    def get_benchmark_input_node_by_evaluation_criteria_id(self, evaluation_criteria_id: str):
        """
        根据评价计划id获取输入节点信息
        :param evaluation_criteria_id:
        :return:
        """
        sql = """
        SELECT * FROM sv_current_benchmark_input_node 
        where evaluation_criteria_id = :evaluation_criteria_id
        and source_category = :source_category
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=BenchmarkInputNodeModel,
            params={
                "evaluation_criteria_id": evaluation_criteria_id,
                "source_category": BenchmarkInputNodeSourceCategory.INPUT.name,
            },
        )
