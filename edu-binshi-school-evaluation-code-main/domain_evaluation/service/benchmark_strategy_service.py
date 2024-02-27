import inspect
from typing import Dict, List, Optional

from infra_basic.errors import BusinessError
from infra_utility.base_plus_model import BasePlusModel
from infra_utility.enum_helper import get_enum_value_by_name

from domain_evaluation.model.benchmark_strategy.built_benchmark_node import BuiltBenchmarkNode
from domain_evaluation.model.benchmark_strategy.score_symbol_schema import ScoreSymbolSchema
from domain_evaluation.model.benchmark_strategy_model import (
    BenchmarkStrategyModel,
    EnumBenchmarkStrategySourceCategory,
    EnumCalcStrategyCode,
)
from domain_evaluation.model.edit.load_benchmark_schema_args_em import (
    LoadBenchmarkSchemaArgsEditModel,
)
from domain_evaluation.model.view.benchmark_strategy_vm import BenchmarkStrategyViewModel
from domain_evaluation.repository.benchmark_repository import BenchmarkRepository
from domain_evaluation.repository.benchmark_strategy_repository import BenchmarkStrategyRepository
from domain_evaluation.service.benchmark_strategy_factory import BenchmarkStrategyFactory


class BenchmarkStrategyService:
    def __init__(
        self,
        benchmark_strategy_factory: BenchmarkStrategyFactory,
        benchmark_strategy_repository: BenchmarkStrategyRepository,
        benchmark_repository: BenchmarkRepository,
    ):
        self._benchmark_strategy_factory = benchmark_strategy_factory
        self._benchmark_strategy_repository = benchmark_strategy_repository
        self._benchmark_repository = benchmark_repository

    def load_benchmark_strategy_list(
        self, benchmark_id: Optional[str]
    ) -> List[BenchmarkStrategyViewModel]:
        """
        加载所有的基准策略
        """
        benchmark_info = None
        if benchmark_id:
            benchmark_info = self._benchmark_repository.get_benchmark_detail_by_id(
                benchmark_id=benchmark_id
            )
        strategy_list = self._benchmark_strategy_repository.get_benchmark_strategy_list()
        score_symbol_dict: Dict[str, ScoreSymbolSchema] = {}
        result = []
        for strategy in strategy_list:
            score_symbol = score_symbol_dict.get(strategy.score_symbol_scope)
            if not score_symbol:
                need_item_schema = strategy.code not in EnumCalcStrategyCode.__members__
                score_symbol = self._benchmark_strategy_factory.prepare_score_symbol_params(
                    score_symbol_scope=strategy.score_symbol_scope,
                    need_item_schema=need_item_schema,
                )
                score_symbol_dict[strategy.score_symbol_scope] = score_symbol
            new_items = []
            for item in score_symbol.items:
                if item.is_activated or (
                    benchmark_info
                    and benchmark_info.benchmark_strategy_id == strategy.id
                    and benchmark_info.benchmark_strategy_params.get("scoreSymbolId") == item.value
                ):
                    new_items.append(item)
            result.append(
                BenchmarkStrategyViewModel(
                    id=strategy.id,
                    name=strategy.name,
                    score_symbol=ScoreSymbolSchema(
                        component_type=score_symbol.component_type,
                        form_name=score_symbol.form_name,
                        items=new_items,
                        item_params=score_symbol.item_params,
                        title=score_symbol.title,
                    ),
                    source_category=strategy.source_category,
                    source_category_name=get_enum_value_by_name(
                        enum_class=EnumBenchmarkStrategySourceCategory,
                        enum_name=strategy.source_category,
                    ),
                    tag_ownership_id=strategy.tag_ownership_id,
                )
            )
        return result

    def load_benchmark_input_schema(
        self, load_args: LoadBenchmarkSchemaArgsEditModel
    ) -> Optional[BasePlusModel]:
        """
        加载基准策略的输入参数
        """
        strategy = self.must_get_benchmark_strategy(strategy_id=load_args.strategy_id)
        method = getattr(self._benchmark_strategy_factory, strategy.prepare_func)
        # 使用inspect来获取method的参数
        parameters = inspect.signature(method).parameters
        # 仅传递method需要的参数
        args = load_args.dict()
        required_args = {k: v for k, v in args.items() if k in parameters}
        schema = method(**required_args)
        return schema

    def must_get_benchmark_strategy(self, strategy_id: str) -> BenchmarkStrategyModel:
        """
        获取基准策略
        """
        strategy = self._benchmark_strategy_repository.fetch_benchmark_strategy_by_id(
            strategy_id=strategy_id
        )
        if not strategy:
            raise BusinessError("未获取到相关策略")
        return strategy

    def build_benchmark_node(
        self, benchmark_id, strategy_id: str, params: Dict
    ) -> List[BuiltBenchmarkNode]:
        """
        构建基准节点
        """
        strategy = self.must_get_benchmark_strategy(strategy_id=strategy_id)
        model_cls = self._benchmark_strategy_factory.load_model_cls(
            model_cls_name=strategy.process_params_type
        )
        method = getattr(self._benchmark_strategy_factory, strategy.build_node_func)
        return method(benchmark_id, model_cls(**params))
