from datetime import datetime
from typing import Optional

from infra_basic.basic_model import BasicModel
from infra_utility.datetime_helper import local_now

from domain_evaluation.model.benchmark_strategy.score_symbol_schema import ScoreSymbolSchema


class BenchmarkStrategyViewModel(BasicModel):
    name: str
    score_symbol: ScoreSymbolSchema
    source_category: Optional[str]
    source_category_name: Optional[str]
    tag_ownership_id: Optional[str]


class BenchmarkStrategyInfoVm(BasicModel):
    name: str
    code: str
    process_params_type: str
    prepare_func: str
    build_node_func: str
    score_symbol_scope: str
    start_at: datetime = local_now()
    finish_at: Optional[datetime]
    source_category: str
    tag_ownership_id: Optional[str]
