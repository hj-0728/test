from infra_utility.algorithm.tree import list_to_tree

from edu_binshi.model.view.period_vm import PeriodTreeNodeVm
from edu_binshi.repository.period_repository import PeriodRepository


class PeriodService:
    def __init__(
        self,
        period_repository: PeriodRepository,
    ):
        self.__period_repository = period_repository

    def get_period_tree(
        self,
        period_category_code: str = None,
    ):
        """
        获取周期分页
        :return:
        """
        tree_list = self.__period_repository.get_period_tree_list(
            period_category_code=period_category_code
        )
        return list_to_tree(tree_list, tree_node_type=PeriodTreeNodeVm, seq_attr="start_at")
