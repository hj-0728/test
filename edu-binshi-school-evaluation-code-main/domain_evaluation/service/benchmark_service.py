from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now
from infra_utility.token_helper import generate_uuid_id

from domain_evaluation.model.benchmark_model import BenchmarkModel
from domain_evaluation.model.edit.load_benchmark_schema_args_em import (
    LoadBenchmarkSchemaArgsEditModel,
)
from domain_evaluation.model.edit.save_benchmark_em import SaveBenchmarkEditModel
from domain_evaluation.repository.benchmark_repository import BenchmarkRepository
from domain_evaluation.service.benchmark_execute_node_service import BenchmarkExecuteNodeService
from domain_evaluation.service.benchmark_manage_service import BenchmarkManageService
from domain_evaluation.service.benchmark_strategy_service import BenchmarkStrategyService
from domain_evaluation.service.evaluation_criteria_service import \
    EvaluationCriteriaService
from infra_backbone.service.tag_service import TagService


class BenchmarkService:
    """
    评价标准适用的集合 service
    """

    def __init__(
        self,
        benchmark_repository: BenchmarkRepository,
        benchmark_manage_service: BenchmarkManageService,
        benchmark_strategy_service: BenchmarkStrategyService,
        benchmark_execute_node_service: BenchmarkExecuteNodeService,
        tag_service: TagService,
        evaluation_criteria_service: EvaluationCriteriaService,
    ):
        self.__benchmark_repository = benchmark_repository
        self.__benchmark_manage_service = benchmark_manage_service
        self.__benchmark_strategy_service = benchmark_strategy_service
        self.__benchmark_execute_node_service = benchmark_execute_node_service
        self.__tag_service = tag_service
        self.__evaluation_criteria_service = evaluation_criteria_service

    def save_benchmark(self, data: SaveBenchmarkEditModel, transaction: Transaction) -> str:
        """
        保存基准
        :param transaction:
        :param data:
        """

        self.__evaluation_criteria_service.judge_evaluation_criteria_can_update(
            evaluation_criteria_id=data.evaluation_criteria_id
        )

        benchmark_id = self.refresh_benchmark(benchmark=data.benchmark, transaction=transaction)
        node_list = self.__benchmark_strategy_service.build_benchmark_node(
            benchmark_id=benchmark_id,
            strategy_id=data.benchmark.benchmark_strategy_id,
            params=data.benchmark.benchmark_strategy_params,
        )
        self.__benchmark_execute_node_service.add_benchmark_node(
            node_list=node_list, transaction=transaction
        )
        self.__tag_service.update_related_relationship(
            tag_ownership_relationship=data.build_save_tag_ownership_relationship_model(
                benchmark_id=benchmark_id
            ),
            transaction=transaction,
        )
        return benchmark_id

    def get_benchmark_list_by_indicator_id(self, indicator_id: str, input_score_symbol_id: str):
        """
        获取指标的所有基准
        """
        benchmark_list = self.__benchmark_repository.get_benchmark_list_by_indicator_id(
            indicator_id=indicator_id,
            input_score_symbol_id=input_score_symbol_id,
        )
        return benchmark_list

    def refresh_benchmark(self, benchmark: BenchmarkModel, transaction: Transaction) -> str:
        """
        更新基准
        """
        new_benchmark = benchmark.cast_to(cast_type=BenchmarkModel, id=generate_uuid_id())
        if benchmark.id:
            benchmark.finish_at = new_benchmark.start_at
            self.handle_old_benchmark(
                benchmark=benchmark, new_benchmark_id=new_benchmark.id, transaction=transaction
            )
        self.__benchmark_repository.insert_benchmark(
            benchmark=new_benchmark, transaction=transaction
        )
        return new_benchmark.id

    def handle_old_benchmark(
        self, benchmark: BenchmarkModel, new_benchmark_id: str, transaction: Transaction
    ):
        """
        处理旧的基准
        """
        db_old_benchmark = self.__benchmark_repository.fetch_specific_version_benchmark(
            benchmark_id=benchmark.id, benchmark_version=benchmark.version
        )
        if not db_old_benchmark:
            raise BusinessError("数据已发生改变，请刷新页面重试")
        # 如果本次修改只是改了下名字或这修改了分数填写的区间，那么应该把这个基准作为输入源的基准替换到新的基准上
        if benchmark.same_strategy_and_symbol(compared_benchmark=db_old_benchmark):
            self.__benchmark_execute_node_service.update_benchmark_as_source(
                old_benchmark_id=benchmark.id,
                new_benchmark_id=new_benchmark_id,
                transaction=transaction,
            )
            reference_benchmark_list = self.__benchmark_repository.fetch_benchmark_reference_list(
                source_benchmark_id=benchmark.id
            )
            for reference_benchmark in reference_benchmark_list:
                strategy_params = reference_benchmark.benchmark_strategy_params
                change = False
                if "sourceBenchmarkIdList" in strategy_params and benchmark.id in strategy_params["sourceBenchmarkIdList"]:
                    source_benchmark_id_list = strategy_params["sourceBenchmarkIdList"]
                    source_benchmark_id_list[source_benchmark_id_list.index(benchmark.id)] = new_benchmark_id
                    change = True
                elif "sourceBenchmark" in strategy_params:
                    source_benchmark = strategy_params["sourceBenchmark"]
                    if isinstance(source_benchmark, dict):
                        strategy_params["sourceBenchmark"]["sourceBenchmarkId"] = new_benchmark_id
                        change = True
                    else:
                        for agg_benchmark in source_benchmark:
                            if agg_benchmark["sourceBenchmarkId"] == benchmark.id:
                                agg_benchmark["sourceBenchmarkId"] = new_benchmark_id
                                change = True
                if change:
                    self.__benchmark_repository.update_benchmark(
                        benchmark=reference_benchmark,
                        transaction=transaction,
                        limited_col_list=["benchmark_strategy_params"],
                    )
        else:
            as_source_count = self.__benchmark_repository.fetch_current_benchmark_as_other_source(
                benchmark_id=benchmark.id
            )
            if as_source_count:
                raise BusinessError("该基准已经被其他基准引用，无法修改")
        self.__benchmark_repository.update_benchmark(
            benchmark=benchmark, transaction=transaction, limited_col_list=["finish_at"]
        )
        self.__benchmark_execute_node_service.finish_benchmark_input_node(
            benchmark_id=benchmark.id, transaction=transaction
        )

    def get_benchmark_detail(self, benchmark_id: str):
        """
        获取benchmark基础信息
        """
        benchmark_info = self.__benchmark_repository.get_benchmark_detail_by_id(
            benchmark_id=benchmark_id
        )
        benchmark_info.benchmark_strategy_schema = (
            self.__benchmark_strategy_service.load_benchmark_input_schema(
                load_args=LoadBenchmarkSchemaArgsEditModel(
                    strategy_id=benchmark_info.benchmark_strategy_id,
                    indicator_id=benchmark_info.indicator_id,
                    score_symbol_id=benchmark_info.benchmark_strategy_params.get(
                        "scoreSymbolId", None
                    ),
                    benchmark_id=benchmark_info.id,
                )
            )
        )
        return benchmark_info

    def finish_benchmark_by_indicator_id(
        self, indicator_id: str, transaction: Transaction, need_check_as_parent_source: bool = False
    ):
        """
        结束某个指标下的所有benchmark
        :indicator_id
        :transaction
        :need_check_as_parent_source 是否需要检查这个benchmark被其他节点引用了
        """
        if need_check_as_parent_source:
            as_source_count = (
                self.__benchmark_repository.fetch_current_benchmark_as_parent_source(
                    indicator_id=indicator_id,
                )
            )
            if as_source_count:
                raise BusinessError("该评论项或其子评论项基准已经被其他基准引用，无法删除")
        benchmark_list = self.__benchmark_repository.fetch_benchmark_list(indicator_id=indicator_id)
        for benchmark in benchmark_list:
            benchmark.finish_at = local_now()
            self.__benchmark_repository.update_benchmark(
                benchmark=benchmark, transaction=transaction, limited_col_list=["finish_at"]
            )
            self.__benchmark_execute_node_service.finish_benchmark_input_node(
                benchmark_id=benchmark.id, transaction=transaction
            )

    def finish_single_benchmark(
        self, benchmark_id: str, benchmark_version: int, transaction: Transaction
    ):
        """
        结束benchmark
        :benchmark_id
        :benchmark_version
        :transaction
        :need_check_as_parent_source 是否需要检查这个benchmark被父节点引用了
        """

        benchmark = self.__benchmark_repository.fetch_benchmark_by_id(benchmark_id=benchmark_id)
        if benchmark.version != benchmark_version:
            raise BusinessError("该基准已经被改动或删除，请刷新页面")
        as_source_count = self.__benchmark_repository.fetch_current_benchmark_as_other_source(
            benchmark_id=benchmark.id
        )
        if as_source_count:
            raise BusinessError("该基准已经被其他基准引用，无法修改")
        benchmark.finish_at = local_now()
        self.__benchmark_repository.update_benchmark(
            benchmark=benchmark, transaction=transaction, limited_col_list=["finish_at"]
        )
        self.__benchmark_execute_node_service.finish_benchmark_input_node(
            benchmark_id=benchmark.id, transaction=transaction
        )
