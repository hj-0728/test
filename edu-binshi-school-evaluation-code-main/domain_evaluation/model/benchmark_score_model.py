from enum import Enum
from typing import Optional

from infra_basic.basic_model import VersionedModel


class EnumBenchmarkScoreLogCategory(Enum):
    """
    基准执行节点类型
    """

    CALC_LOG = "计算"
    INPUT_LOG = "输入"


class BenchmarkScoreModel(VersionedModel):
    """
    基准分数
    """

    evaluation_assignment_id: str
    benchmark_id: str
    numeric_score: Optional[float]
    string_score: Optional[str]
    source_score_log_category: Optional[str]
    source_score_log_id: Optional[str]
