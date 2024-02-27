from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from infra_basic.basic_model import VersionedModel
from infra_utility.datetime_helper import local_now
from pydantic import Field


class BenchmarkInputNodeSourceCategory(Enum):
    INPUT = "输入"
    BENCHMARK = "其他的基准"


class BenchmarkInputNodeSourceExecMode(Enum):
    FREEDOM = "自由"
    ONCE = "一次"
    SCHEDULER = "定时"


class BenchmarkInputNodeFillerCalcMethod(Enum):
    SELF_BENCHMARK = "SelfBenchmark"


class BenchmarkInputNodeModel(VersionedModel):
    benchmark_execute_node_id: Optional[str]
    source_category: str
    source_benchmark_id: Optional[str]
    source_exec_mode: Optional[str]
    scheduler_expression: Optional[str]
    filler_calc_method: Optional[str]
    filler_calc_context: Optional[Dict]
    score_symbol_id: str
    numeric_min_score: Optional[float]
    numeric_max_score: Optional[float]
    limited_string_options: Optional[List[str]]

    start_at: datetime = Field(default_factory=local_now)
    finish_at: Optional[datetime]
