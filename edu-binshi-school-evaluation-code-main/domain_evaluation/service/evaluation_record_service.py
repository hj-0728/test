from infra_utility.algorithm.tree import list_to_tree

from domain_evaluation.model.edit.evaluation_record_em import EvaluationRecordEditModel
from domain_evaluation.model.view.benchmark_input_node_vm import BenchmarkInputNodeVm
from domain_evaluation.model.view.evaluation_criteria_tree_vm import EvaluationCriteriaTreeViewModel
from domain_evaluation.model.view.evaluation_record_vm import EvaluationRecordViewModel
from domain_evaluation.repository.benchmark_input_node_repository import BenchmarkInputNodeRepository
from domain_evaluation.repository.evaluation_criteria_tree_repository import EvaluationCriteriaTreeRepository


class EvaluationRecordService:
    """
    评价记录 service
    """

    def __init__(
        self,
        evaluation_criteria_tree_repository: EvaluationCriteriaTreeRepository,
        benchmark_input_node_repository: BenchmarkInputNodeRepository,
    ):
        self.__evaluation_criteria_tree_repository = evaluation_criteria_tree_repository
        self.__benchmark_input_node_repository = benchmark_input_node_repository

    def get_evaluation_record_tree(
        self,
        evaluation_record_em: EvaluationRecordEditModel,
    ):
        """
        获取评价记录树
        :param evaluation_record_em:
        :return:
        """
        evaluation_criteria_tree = self.__evaluation_criteria_tree_repository.get_evaluation_criteria_tree_with_all_benchmark(
            evaluation_criteria_id=evaluation_record_em.evaluation_criteria_id,
            evaluation_criteria_plan_id=evaluation_record_em.evaluation_criteria_plan_id,
            evaluation_assignment_id=evaluation_record_em.evaluation_assignment_id,
        )
        log_list = self.__benchmark_input_node_repository.get_benchmark_input_node_score_log(
            evaluation_assignment_id=evaluation_record_em.evaluation_assignment_id,
            people_id=evaluation_record_em.people_id,
        )
        log_dict = {x.benchmark_id: x for x in log_list}
        for indicator in evaluation_criteria_tree:
            if indicator.benchmark_simple_list:
                for benchmark in indicator.benchmark_simple_list:
                    log = log_dict.get(benchmark.benchmark_id, None)
                    if log:
                        indicator.benchmark_display_list.append(log)
                    else:
                        indicator.benchmark_display_list.append(
                            BenchmarkInputNodeVm(**benchmark.dict())
                        )

        tree_data = list_to_tree(
            original_list=evaluation_criteria_tree,
            tree_node_type=EvaluationCriteriaTreeViewModel,
            parent_id_attr="parent_indicator_id",
            seq_attr="sort_info",
        )
        return EvaluationRecordViewModel(
            tree_data=tree_data,
            need_input_dict=log_dict
        )
