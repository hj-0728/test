from datetime import datetime
from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel
from infra_utility.datetime_helper import local_now


class EnumBenchmarkStrategyScoreSymbolScope(Enum):
    NUM = "分值"
    STRING = "分级"
    BOTH = "分值和分级都有"
    CUSTOM = "自定义具体的符号"


class EnumCalcStrategyCode(Enum):
    """
    计算类的策略
    """

    SAME_LEVEL_AGGREGATED = "同一层级分值聚合"
    SUB_LEVEL_AGGREGATED = "子级分值聚合"
    SUB_LEVEL_STATS = "子级评价项的评价分类相加"
    SAME_LEVEL_STATS = "本级评价项的评价分类相加"


class EnumBenchmarkStrategySourceCategory(Enum):
    INPUT = "输入"
    CALC = "计算"


class BenchmarkStrategyModel(VersionedModel):
    name: str
    code: str
    process_params_type: str
    prepare_func: str
    build_node_func: str
    score_symbol_scope: str
    start_at: datetime = local_now()
    finish_at: Optional[datetime]
    source_category: str
