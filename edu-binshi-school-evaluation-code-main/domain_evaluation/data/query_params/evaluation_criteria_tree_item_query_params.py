from infra_basic.basic_repository import PageFilterParams
from infra_basic.basic_model import BasicModel


class EvaluationCriteriaBoundTagItemQueryParams(BasicModel):
    """
    绑定标签评价标准项 查询条件
    """
    level: int = 1
    tag_name: str
    evaluation_criteria_id: str
    is_selected: bool = False


class EvaluationCriteriaNotBoundTagItemQueryParams(PageFilterParams):
    """
    未绑定标签评价标准项 查询条件
    """

    level: int
    evaluation_criteria_id: str
