from typing import List

from infra_basic.basic_resource import BasicResource

from domain_evaluation.benchmark.basic_benchmark import BasicBenchmark
from domain_evaluation.model.edit.load_filler_em import LoadFillerEditModel
from domain_evaluation.repository.benchmark_node_assistant_repository import (
    BenchmarkNodeAssistantRepository,
)
from domain_evaluation.service.benchmark_execute_node_service import BenchmarkExecuteNodeService
from edu_binshi.repository.subject_repository import SubjectRepository
from infra_backbone.repository.team_category_repository import TeamCategoryRepository


class BasicBenchmarkImpl(BasicBenchmark):
    def __init__(
        self,
        execute_node_service: BenchmarkExecuteNodeService,
        subject_repository: SubjectRepository,
        benchmark_node_assistant_repository: BenchmarkNodeAssistantRepository,
        team_category_repository: TeamCategoryRepository,
    ):
        self._execute_node_service = execute_node_service
        self._subject_repository = subject_repository
        self._benchmark_node_assistant_repository = benchmark_node_assistant_repository
        self._team_category_repository = team_category_repository

    def load_filler(self, params: LoadFillerEditModel) -> List[BasicResource]:
        """
        加载填充者
        """
        return []
