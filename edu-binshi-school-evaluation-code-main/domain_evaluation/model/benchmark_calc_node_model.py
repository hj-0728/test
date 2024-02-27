from enum import Enum
from typing import Dict, Optional

from infra_basic.basic_model import VersionedModel


class EnumBenchmarkCalcMethod(Enum):
    """
    计算方式
    """

    RANGE_VALUE = "区间取值"
    STATS = "统计"
    WEIGHT = "权重"


class BenchmarkCalcNodeModel(VersionedModel):
    """
    计算节点
    """

    benchmark_execute_node_id: str
    input_score_symbol_id: str
    output_score_symbol_id: str
    calc_method: str


class BenchmarkCalcNodeRangeValueArgsModel(VersionedModel):
    """
    计算方式为区间取值时的计算参数
    """

    benchmark_calc_node_id: Optional[str]
    min_score: float
    max_score: float
    left_operator: str
    right_operator: str
    match_value: str


class EnumBenchmarkCalcNodeStatsMethod(Enum):
    """
    计算方式为统计时的计算方法
    """

    SUM = "求和"
    AVG = "平均值"
    MAX = "最大值"
    MIN = "最小值"
    MEDIAN = "中位数"
    MODE = "众数"


class BenchmarkCalcNodeStatsArgsModel(VersionedModel):
    """
    计算方式为统计时的计算参数
    """

    benchmark_calc_node_id: str
    stats_method: str
    stats_args: Optional[Dict]


class BenchmarkCalcNodeWeightArgsModel(VersionedModel):
    """
    计算方式为权重时的计算参数
    """

    benchmark_calc_node_id: str
    weight: float
    seq: int
