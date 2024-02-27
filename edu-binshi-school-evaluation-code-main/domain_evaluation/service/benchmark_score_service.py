from typing import List

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.algorithm.tree import list_to_tree

from domain_evaluation.model.benchmark_execute_node_model import EnumBenchmarkExecuteNodeCategory
from domain_evaluation.model.benchmark_score_model import BenchmarkScoreModel
from domain_evaluation.model.calc_score_input_model import CalcScoreInputModel, \
    EnumCalcScoreInputCategory
from domain_evaluation.model.calc_score_output_model import CalcScoreOutputModel
from domain_evaluation.model.view.benchmark_node_score_tree_vm import BenchmarkNodeScoreTreeModel
from domain_evaluation.repository.benchmark_repository import BenchmarkRepository
from domain_evaluation.repository.benchmark_score_repository import BenchmarkScoreRepository
from domain_evaluation.repository.calc_score_input_repository import CalcScoreInputRepository
from domain_evaluation.repository.calc_score_output_repository import CalcScoreOutputRepository
from domain_evaluation.service.node_calc_method_service import NodeCalcMethodService


class BenchmarkScoreService:
    """
    基准分数 service
    """

    def __init__(
        self,
        benchmark_repository: BenchmarkRepository,
        benchmark_score_repository: BenchmarkScoreRepository,
        calc_score_input_repository: CalcScoreInputRepository,
        calc_score_output_repository: CalcScoreOutputRepository,
        node_calc_method_service: NodeCalcMethodService,
    ):
        self.__benchmark_repository = benchmark_repository
        self.__benchmark_score_repository = benchmark_score_repository
        self.__calc_score_input_repository = calc_score_input_repository
        self.__calc_score_output_repository = calc_score_output_repository
        self.__node_calc_method_service = node_calc_method_service

    def save_benchmark_score(
        self,
        benchmark_id: str,
        evaluation_assignment_id: str,
        transaction: Transaction,
    ):
        """
        保存基准分数
        找到benchmark的计算节点，一个一个进行计算，并保存输入及输出
        :param benchmark_id:
        :param evaluation_assignment_id:
        :param transaction:
        """

        # 1. 获取所有初始节点
        node_info_list = (
            self.__benchmark_score_repository.fetch_calc_benchmark_score_need_node_info(
                benchmark_id=benchmark_id,
                evaluation_assignment_id=evaluation_assignment_id,
            )
        )

        # 2. 生成树
        node_tree = list_to_tree(
            original_list=node_info_list,
            tree_node_type=BenchmarkNodeScoreTreeModel,
            parent_id_attr="next_node_id",
        )

        # 3. 计算节点分数
        self.calc_benchmark_score(
            node_tree=node_tree,
            transaction=transaction,
        )

        # 4. 保存基准分数 先根据evaluation_assignment_id和benchmark_id判断是否存在，存在就update
        new_benchmark_score = BenchmarkScoreModel(
            evaluation_assignment_id=evaluation_assignment_id,
            benchmark_id=benchmark_id,
            numeric_score=node_tree[0].numeric_score,
            string_score=node_tree[0].string_score,
            source_score_log_category=node_tree[0].source_score_category,
            source_score_log_id=node_tree[0].source_score_id,
        )

        benchmark_score = self.__benchmark_score_repository.fetch_benchmark_score_by_evaluation_assignment_id_and_benchmark_id(
            evaluation_assignment_id=evaluation_assignment_id,
            benchmark_id=benchmark_id
        )
        if benchmark_score:
            new_benchmark_score.id = benchmark_score.id
            new_benchmark_score.version = benchmark_score.version
            self.__benchmark_score_repository.update_benchmark_score(
                benchmark_score=new_benchmark_score,
                transaction=transaction,
                limited_col_list=["numeric_score", "string_score",
                                  "source_score_log_category", "source_score_log_id"]
            )
        else:
            self.__benchmark_score_repository.insert_benchmark_score(
                benchmark_score=new_benchmark_score,
                transaction=transaction,
            )

    def calc_benchmark_score(
        self,
        node_tree: List[BenchmarkNodeScoreTreeModel],
        transaction: Transaction,
    ):
        """
        计算基准节点分数
        :param node_tree:
        :param transaction:
        :return:
        """

        for node_info in node_tree:
            for child_node in node_info.children:
                if (
                    child_node.string_score is None
                    and child_node.numeric_score is None
                    and child_node.category == EnumBenchmarkExecuteNodeCategory.CALC.name
                ):
                    self.calc_benchmark_score(
                        node_tree=child_node,
                        transaction=transaction,
                    )
            if node_info.category == EnumBenchmarkExecuteNodeCategory.CALC.name:
                # 计算当前节点分数
                self.calc_benchmark_node_score(
                    node_tree=node_info,
                    transaction=transaction,
                )

    def calc_benchmark_node_score(
        self,
        node_tree: BenchmarkNodeScoreTreeModel,
        transaction: Transaction,
    ):
        """
        计算基准节点分数
        :param node_tree:
        :param transaction:
        :return:
        """

        numeric_score_list = []
        string_score_list = []

        # 删除计算节点log input、output

        self.delete_calc_score_input_and_output(
            calc_score_log_id=node_tree.calc_score_log_id,
            transaction=transaction,
        )

        # 保存输入

        for input_score in node_tree.children:
            # 缺少数据
            if input_score.source_score_id is None:
                raise BusinessError("数据未全部填完")
            self.__calc_score_input_repository.insert_calc_score_input(
                calc_score_input=CalcScoreInputModel(
                    calc_score_log_id=node_tree.calc_score_log_id,
                    source_score_category=input_score.source_score_category,
                    source_score_id=input_score.source_score_id,
                ),
                transaction=transaction,
            )
            numeric_score_list.append(input_score.numeric_score)
            string_score_list.append(input_score.string_score)

        # 计算分数

        node_tree.numeric_score, node_tree.string_score = self.__node_calc_method_service.calc_node(
            numeric_score_list=numeric_score_list,
            node_id=node_tree.id,
        )

        node_tree.source_score_id = node_tree.calc_score_log_id
        node_tree.source_score_category = EnumCalcScoreInputCategory.CALC_LOG.name

        # 保存输出

        self.__calc_score_output_repository.insert_calc_score_output(
            calc_score_output=CalcScoreOutputModel(
                calc_score_log_id=node_tree.calc_score_log_id,
                numeric_score=node_tree.numeric_score,
                string_score=node_tree.string_score,
            ),
            transaction=transaction,
        )

    def delete_calc_score_input_and_output(
        self, calc_score_log_id: str, transaction: Transaction,
    ):
        """
        删除计算节点log input、output
        :param calc_score_log_id:
        :param transaction:
        :return:
        """

        calc_score_input_list = self.__calc_score_input_repository.get_calc_score_input_by_log_id(
            calc_score_log_id=calc_score_log_id
        )

        for calc_score_input in calc_score_input_list:
            self.__calc_score_input_repository.delete_calc_score_input(
                calc_score_input_id=calc_score_input.id,
                transaction=transaction,
            )

        calc_score_output_list = self.__calc_score_output_repository.get_calc_score_output_by_log_id(
            calc_score_log_id=calc_score_log_id
        )

        for calc_score_output in calc_score_output_list:
            self.__calc_score_output_repository.delete_calc_score_output(
                calc_score_output_id=calc_score_output.id,
                transaction=transaction,
            )

