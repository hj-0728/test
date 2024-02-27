from typing import List, Optional

from infra_basic.basic_repository import PageFilterParams
from infra_utility.base_plus_model import BasePlusModel


class EvaluationCriteriaPageQueryParams(PageFilterParams):
    """
    评价标准 查询条件
    """

    status_list: List[str] = []
    evaluation_object_category: Optional[str]
    evaluation_object_category_list: List[str] = []


class EvaluationCriteriaListQueryParams(BasePlusModel):
    status_list: List[str] = []
    evaluation_object_category_list: List[str] = []
