from typing import Optional

from infra_basic.basic_model import VersionedModel


class CalcScoreOutputModel(VersionedModel):
    """
    计算节点输出
    """

    calc_score_log_id: str
    numeric_score: Optional[float]
    string_score: Optional[str]
