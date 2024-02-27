from typing import Optional

from infra_utility.base_plus_model import BasePlusModel


class EvaluationCriteriaTreeItemViewModel(BasePlusModel):
    id: str
    name: str
    level: int
    tag_ownership_relationship_id: Optional[str]
    tag_name: Optional[str]
