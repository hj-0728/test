from typing import Dict, List

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now
from infra_utility.token_helper import generate_uuid_id

from domain_evaluation.model.benchmark_calc_node_model import (
    BenchmarkCalcNodeModel,
    BenchmarkCalcNodeRangeValueArgsModel,
    BenchmarkCalcNodeStatsArgsModel,
    BenchmarkCalcNodeWeightArgsModel,
    EnumBenchmarkCalcMethod,
)
from domain_evaluation.model.benchmark_execute_node_model import (
    BenchmarkExecuteNodeModel,
    EnumBenchmarkExecuteNodeCategory,
)
from domain_evaluation.model.benchmark_input_node_model import BenchmarkInputNodeModel
from domain_evaluation.model.benchmark_strategy.built_benchmark_node import (
    BuiltBenchmarkCalcNode,
    BuiltBenchmarkNode,
)
from domain_evaluation.model.edit.save_benchmark_node_em import (
    SaveBenchmarkCalcNode,
    SaveBenchmarkInputNode,
)
from domain_evaluation.repository.benchmark_execute_node_repository import (
    BenchmarkExecuteNodeRepository,
)


class BenchmarkExecuteNodeService:
    def __init__(self, benchmark_execute_node_repository: BenchmarkExecuteNodeRepository):
        self._benchmark_execute_node_repository = benchmark_execute_node_repository

    def save_benchmark_execute_node(
        self, node: BenchmarkExecuteNodeModel, transaction: Transaction
    ) -> str:
        """
        保存执行节点
        """
        return self._benchmark_execute_node_repository.insert_benchmark_execute_node(
            node=node, transaction=transaction
        )

    def save_benchmark_input_node(
        self, node: SaveBenchmarkInputNode, transaction: Transaction
    ) -> str:
        """
        保存输入节点
        """

        execute_node = BenchmarkExecuteNodeModel(
            benchmark_id=node.benchmark_id,
            name=node.name,
            category=EnumBenchmarkExecuteNodeCategory.INPUT.name,
            next_node_id=node.next_node_id,
            seq=node.seq,
        )
        execute_node_id = self.save_benchmark_execute_node(
            node=execute_node, transaction=transaction
        )
        input_node = node.input_node.cast_to(
            cast_type=BenchmarkInputNodeModel, benchmark_execute_node_id=execute_node_id
        )
        self._benchmark_execute_node_repository.insert_benchmark_input_node(
            node=input_node, transaction=transaction
        )
        return execute_node_id

    def save_benchmark_calc_node(
        self, node: SaveBenchmarkCalcNode, transaction: Transaction
    ) -> str:
        """
        保存计算节点
        """

        execute_node = BenchmarkExecuteNodeModel(
            benchmark_id=node.benchmark_id,
            name=node.name,
            category=EnumBenchmarkExecuteNodeCategory.CALC.name,
            next_node_id=node.next_node_id,
        )
        execute_node_id = self.save_benchmark_execute_node(
            node=execute_node, transaction=transaction
        )
        calc_node = node.calc_node.cast_to(
            cast_type=BenchmarkCalcNodeModel, benchmark_execute_node_id=execute_node_id
        )
        calc_node_id = self._benchmark_execute_node_repository.insert_benchmark_calc_node(
            node=calc_node, transaction=transaction
        )
        node_args = node.calc_node.args
        node_args["benchmark_calc_node_id"] = calc_node_id
        self.save_benchmark_calc_node_args(
            calc_method=node.calc_node.calc_method, args=node_args, transaction=transaction
        )
        return execute_node_id

    def save_benchmark_calc_node_args(self, calc_method: str, args: Dict, transaction: Transaction):
        """
        保存计算节点的参数
        """
        if calc_method == EnumBenchmarkCalcMethod.STATS.name:
            self._benchmark_execute_node_repository.insert_benchmark_calc_node_stats_args(
                args=BenchmarkCalcNodeStatsArgsModel(**args), transaction=transaction
            )
        elif calc_method == EnumBenchmarkCalcMethod.WEIGHT.name:
            weight_list = args["weight_list"]
            for weight in weight_list:
                weight["benchmark_calc_node_id"] = args["benchmark_calc_node_id"]
                self._benchmark_execute_node_repository.insert_benchmark_calc_node_weight_args(
                    args=BenchmarkCalcNodeWeightArgsModel(**weight), transaction=transaction
                )
        elif calc_method == EnumBenchmarkCalcMethod.RANGE_VALUE.name:
            range_value_list = args["range_value_list"]
            for range_value in range_value_list:
                range_value["benchmark_calc_node_id"] = args["benchmark_calc_node_id"]
                self._benchmark_execute_node_repository.insert_benchmark_calc_node_range_value_args(
                    args=BenchmarkCalcNodeRangeValueArgsModel(**range_value),
                    transaction=transaction,
                )

    def delete_benchmark_node(self, benchmark_id: str, transaction: Transaction):
        """
        删除节点
        """
        exec_node_list = self._benchmark_execute_node_repository.fetch_benchmark_execute_node(
            benchmark_id=benchmark_id
        )
        for exec_node in exec_node_list:
            if exec_node.category == EnumBenchmarkExecuteNodeCategory.INPUT.name:
                self.delete_input_node(execute_node_id=exec_node.id, transaction=transaction)
            elif exec_node.category == EnumBenchmarkExecuteNodeCategory.CALC.name:
                self.delete_calc_node(execute_node_id=exec_node.id, transaction=transaction)
            self._benchmark_execute_node_repository.delete_benchmark_execute_node(
                execute_node_id=exec_node.id, transaction=transaction
            )

    def delete_input_node(self, execute_node_id: str, transaction: Transaction):
        """
        删除输入节点
        """
        input_node = (
            self._benchmark_execute_node_repository.fetch_benchmark_input_node_by_execute_node_id(
                benchmark_execute_node_id=execute_node_id
            )
        )
        if input_node:
            self._benchmark_execute_node_repository.delete_benchmark_input_node(
                input_node_id=input_node.id, transaction=transaction
            )

    def delete_calc_node(self, execute_node_id: str, transaction: Transaction):
        """
        删除计算节点
        """
        calc_node = self._benchmark_execute_node_repository.fetch_calc_node_by_execute_node_id(
            benchmark_execute_node_id=execute_node_id
        )
        if calc_node:
            self._benchmark_execute_node_repository.delete_benchmark_calc_node(
                calc_node_id=calc_node.id, transaction=transaction
            )
            self.delete_calc_node_args(calc_node=calc_node, transaction=transaction)

    def delete_calc_node_args(self, calc_node: BenchmarkCalcNodeModel, transaction: Transaction):
        """
        删除计算节点的参数
        """
        if calc_node.calc_method == EnumBenchmarkCalcMethod.STATS.name:
            stats_args = (
                self._benchmark_execute_node_repository.fetch_calc_node_stats_args_by_calc_node_id(
                    benchmark_calc_node_id=calc_node.id
                )
            )
            self._benchmark_execute_node_repository.delete_calc_node_stats_args(
                stats_args_id=stats_args.id, transaction=transaction
            )
        elif calc_node.calc_method == EnumBenchmarkCalcMethod.WEIGHT.name:
            weight_args_list = (
                self._benchmark_execute_node_repository.fetch_calc_node_weight_args_by_calc_node_id(
                    benchmark_calc_node_id=calc_node.id
                )
            )
            for weight_args in weight_args_list:
                self._benchmark_execute_node_repository.delete_calc_node_weight_args(
                    weight_args_id=weight_args.id, transaction=transaction
                )
        elif calc_node.calc_method == EnumBenchmarkCalcMethod.RANGE_VALUE.name:
            range_value_args_list = self._benchmark_execute_node_repository.fetch_calc_node_range_value_args_by_calc_node_id(
                benchmark_calc_node_id=calc_node.id
            )
            for range_value_args in range_value_args_list:
                self._benchmark_execute_node_repository.delete_calc_node_range_value_args(
                    range_value_args_id=range_value_args.id, transaction=transaction
                )

    def load_input_node(self, input_node_id: str) -> BenchmarkInputNodeModel:
        """
        加载输入节点
        """
        input_node = self._benchmark_execute_node_repository.fetch_benchmark_input_node_by_id(
            input_node_id=input_node_id
        )
        if not input_node:
            raise BusinessError("未获取到输入节点")
        return input_node

    def add_benchmark_node(self, node_list: List[BuiltBenchmarkNode], transaction: Transaction):
        """
        添加节点
        """
        for node in node_list:
            self._benchmark_execute_node_repository.insert_benchmark_execute_node(
                node=node.cast_to(BenchmarkExecuteNodeModel), transaction=transaction
            )
            if node.category == EnumBenchmarkExecuteNodeCategory.INPUT.name:
                self._benchmark_execute_node_repository.insert_benchmark_input_node(
                    node=node.input_node, transaction=transaction
                )
            else:
                calc_node = node.calc_node
                self.add_calc_node(calc_node=calc_node, transaction=transaction)

    def add_calc_node(self, calc_node: BuiltBenchmarkCalcNode, transaction: Transaction):
        """
        添加计算节点
        """
        self._benchmark_execute_node_repository.insert_benchmark_calc_node(
            node=calc_node.cast_to(BenchmarkCalcNodeModel), transaction=transaction
        )
        if calc_node.calc_method == EnumBenchmarkCalcMethod.STATS.name:
            self._benchmark_execute_node_repository.insert_benchmark_calc_node_stats_args(
                args=calc_node.stats_args, transaction=transaction
            )
        elif calc_node.calc_method == EnumBenchmarkCalcMethod.WEIGHT.name:
            for weight in calc_node.weight_args:
                self._benchmark_execute_node_repository.insert_benchmark_calc_node_weight_args(
                    args=weight, transaction=transaction
                )
        elif calc_node.calc_method == EnumBenchmarkCalcMethod.RANGE_VALUE.name:
            for range_value in calc_node.range_value_args:
                self._benchmark_execute_node_repository.insert_benchmark_calc_node_range_value_args(
                    args=range_value, transaction=transaction
                )

    def update_benchmark_as_source(
        self, old_benchmark_id: str, new_benchmark_id: str, transaction: Transaction
    ):
        """
        更新benchmark作为其他节点输入源的输入节点
        """
        input_node_list = (
            self._benchmark_execute_node_repository.fetch_input_node_by_source_benchmark_id(
                source_benchmark_id=old_benchmark_id
            )
        )
        now = local_now()
        for input_node in input_node_list:
            new_input_dict = {
                "id": generate_uuid_id(),
                "source_benchmark_id": new_benchmark_id,
                "start_at": now,
            }
            new_input_node = input_node.cast_to(BenchmarkInputNodeModel, **new_input_dict)
            self._benchmark_execute_node_repository.insert_benchmark_input_node(
                node=new_input_node, transaction=transaction
            )
            input_node.finish_at = now
            self._benchmark_execute_node_repository.update_benchmark_input_node(
                input_node=input_node, transaction=transaction, limited_col_list=["finish_at"]
            )

    def finish_benchmark_input_node(self, benchmark_id: str, transaction: Transaction):
        """
        完成基准的输入节点
        """
        input_node_list = self._benchmark_execute_node_repository.fetch_benchmark_input_node_list(
            benchmark_id=benchmark_id
        )
        for input_node in input_node_list:
            input_node.finish_at = local_now()
            self._benchmark_execute_node_repository.update_benchmark_input_node(
                input_node=input_node, transaction=transaction, limited_col_list=["finish_at"]
            )
