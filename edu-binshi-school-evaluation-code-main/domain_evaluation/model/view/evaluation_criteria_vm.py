from typing import List, Optional

from infra_basic.basic_model import VersionedModel

from domain_evaluation.model.evaluation_criteria_tree_model import EvaluationCriteriaTreeModel


class EvaluationCriteriaVm(VersionedModel):
    """
    评价标准
    """

    name: str
    status: str
    status_display: Optional[str]
    evaluation_object_category: str
    evaluation_object_category_display: Optional[str]
    comments: Optional[str]
    evaluation_object_category: str
    evaluation_criteria_tree: Optional[EvaluationCriteriaTreeModel]
