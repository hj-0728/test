from typing import List

from infra_utility.base_plus_model import BasePlusModel
from domain_evaluation.model.view.evaluation_criteria_tree_vm import EvaluationCriteriaTreeViewModel


class EvaluationRecordViewModel(BasePlusModel):
    tree_data: List[EvaluationCriteriaTreeViewModel]
    need_input_dict: dict
