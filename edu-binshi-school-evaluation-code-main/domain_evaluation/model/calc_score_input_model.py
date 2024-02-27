from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumCalcScoreInputCategory(Enum):
    """
    基准执行节点类型
    """

    CALC_LOG = "计算"
    INPUT_LOG = "输入"
    BENCHMARK_SCORE = "引用基准分数"


class CalcScoreInputModel(VersionedModel):
    """
    计算节点来源
    """

    calc_score_log_id: str
    source_score_category: str
    source_score_id: str
