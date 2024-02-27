from typing import Optional

from infra_basic.basic_model import BasePlusModel

from domain_evaluation.model.evaluation_assignment_model import EvaluationAssignmentModel
from domain_evaluation.model.input_score_log_model import InputScoreLogModel


class AssignmentInputScoreLogViewModel(BasePlusModel):
    evaluation_assignment: EvaluationAssignmentModel
    input_score_log: Optional[InputScoreLogModel]
