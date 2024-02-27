from typing import List

from infra_basic.basic_model import VersionedModel


class EvaluationCriteriaTreeBindTagEditModel(VersionedModel):
    """
    评价标准计划
    """

    tag_name: str
    evaluation_criteria_id: str
    evaluation_criteria_tree_id_list: List[str]
