from typing import List, Dict

from infra_basic.basic_model import BasePlusModel

from domain_evaluation.model.evaluation_criteria_plan_model import EvaluationCriteriaPlanModel


class BenchmarkPlanViewModel(BasePlusModel):
    benchmark_id: str
    benchmark_input_node_id: str
    filler_calc_method: str
    plan_list: List[EvaluationCriteriaPlanModel]

    def plan_dict(self) -> Dict[str, EvaluationCriteriaPlanModel]:
        return {plan.id: plan for plan in self.plan_list}

    def plan_ids(self) -> List[str]:
        return [plan.id for plan in self.plan_list]

