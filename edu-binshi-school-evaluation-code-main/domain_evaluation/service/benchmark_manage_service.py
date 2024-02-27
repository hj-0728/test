import importlib
import pkgutil
from inspect import isclass
from typing import List, Optional

from infra_basic.basic_resource import BasicResource

import domain_evaluation.benchmark as filler_module
from domain_evaluation.benchmark.basic_benchmark_impl import BasicBenchmarkImpl
from domain_evaluation.model.edit.load_filler_em import LoadFillerEditModel
from domain_evaluation.repository.benchmark_node_assistant_repository import (
    BenchmarkNodeAssistantRepository,
)
from domain_evaluation.service.benchmark_execute_node_service import BenchmarkExecuteNodeService
from edu_binshi.repository.subject_repository import SubjectRepository
from infra_backbone.repository.team_category_repository import TeamCategoryRepository


class BenchmarkManageService:
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

        self._benchmark_factory = {}
        self.init_benchmark_factory()

    def init_benchmark_factory(self):
        """
        初始基准工厂
        """
        benchmark_list = self.scan_module()
        for benchmark in benchmark_list:
            self._benchmark_factory[benchmark.__name__] = benchmark(
                execute_node_service=self._execute_node_service,
                subject_repository=self._subject_repository,
                benchmark_node_assistant_repository=self._benchmark_node_assistant_repository,
                team_category_repository=self._team_category_repository,
            )

    @staticmethod
    def scan_module(filter_item_name: Optional[str] = None):
        all_types = []
        for _, model_name, is_pkg in pkgutil.walk_packages(
            path=filler_module.__path__, prefix=filler_module.__name__ + "."
        ):
            if not is_pkg:
                sub_model = importlib.import_module(model_name)
                for sub_item in dir(sub_model):
                    sub_item = getattr(sub_model, sub_item)
                    if (
                        isclass(sub_item)
                        and issubclass(sub_item, BasicBenchmarkImpl)
                        and sub_item != BasicBenchmarkImpl
                    ):
                        if filter_item_name is None or filter_item_name == sub_item.__name__:
                            all_types.append(sub_item)
        return all_types

    def load_benchmark_filler(self, params: LoadFillerEditModel) -> List[BasicResource]:
        """
        加载填充者
        """
        benchmark = self._benchmark_factory[params.filler_calc_method]
        return benchmark.load_filler(params=params)
