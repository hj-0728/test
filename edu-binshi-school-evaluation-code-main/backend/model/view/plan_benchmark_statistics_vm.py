from typing import Optional, List

from infra_utility.base_plus_model import BasePlusModel

from domain_evaluation.model.view.benchmark_score_symbol_model import \
    BenchmarkScoreSymbolViewModel


class PlanBenchmarkStatisticsBasicVm(BasePlusModel):

    id: Optional[str]
    name: Optional[str]


class PlanBenchmarkClassNumericDistributedVm(PlanBenchmarkStatisticsBasicVm):

    numeric_score: Optional[float]
    count: int


class PlanBenchmarkClassStringDistributedVm(PlanBenchmarkStatisticsBasicVm):

    string_score: Optional[str]
    count: int


class PlanClassBenchmarkStatisticsVm(PlanBenchmarkStatisticsBasicVm):

    all_student: int
    numeric_avg: Optional[float]
    numeric_distributed: Optional[List[PlanBenchmarkClassNumericDistributedVm]]
    string_distributed: Optional[List[PlanBenchmarkClassStringDistributedVm]]


class PlanRankingBenchmarkStatisticsVm(PlanBenchmarkStatisticsBasicVm):

    evaluation_assignment_id: str
    numeric_score: Optional[float]
    string_score: Optional[str]
    dept_name: Optional[str]
    file_id: Optional[str]
    file_url: Optional[str]


class PlanStudentBenchmarkStatisticsVm(PlanBenchmarkStatisticsBasicVm):

    numeric_score: Optional[float]
    string_score: Optional[str]
    count: int


class PlanBenchmarkStatisticsVm(BasePlusModel):

    statistics_info: List[PlanBenchmarkStatisticsBasicVm]
    score_symbol_info: Optional[BenchmarkScoreSymbolViewModel]


class PlanProgressDetailVm(BasePlusModel):
    """
    计划进展详情
    """

    id: str
    name: str
    status: str
    status_name: Optional[str]
    finished_count: Optional[int] = 0
    unfinished_count: Optional[int] = 0
    input_count: Optional[int] = 0
    all_student: Optional[int] = 0
    unfinished_student_count: Optional[int] = 0
    todo_count: Optional[int] = 0

