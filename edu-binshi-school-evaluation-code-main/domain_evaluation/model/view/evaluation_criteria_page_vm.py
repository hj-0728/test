from typing import Optional

from infra_utility.base_plus_model import BasePlusModel


class EvaluationCriteriaPageVm(BasePlusModel):
    """
    评价标准分页
    """

    name: str
    comments: Optional[str]
    scale_factor: float
