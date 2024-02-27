from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from domain_evaluation.entity.benchmark_calc_node import BenchmarkCalcNodeEntity
from domain_evaluation.entity.benchmark_calc_node_range_value_args import (
    BenchmarkCalcNodeRangeValueArgsEntity,
)
from domain_evaluation.entity.benchmark_calc_node_stats_args import BenchmarkCalcNodeStatsArgsEntity
from domain_evaluation.entity.benchmark_calc_node_weight_args import (
    BenchmarkCalcNodeWeightArgsEntity,
)
from domain_evaluation.entity.benchmark_execute_node import BenchmarkExecuteNodeEntity
from domain_evaluation.entity.benchmark_input_node import BenchmarkInputNodeEntity
from domain_evaluation.model.benchmark_calc_node_model import (
    BenchmarkCalcNodeModel,
    BenchmarkCalcNodeRangeValueArgsModel,
    BenchmarkCalcNodeStatsArgsModel,
    BenchmarkCalcNodeWeightArgsModel,
)
from domain_evaluation.model.benchmark_execute_node_model import BenchmarkExecuteNodeModel
from domain_evaluation.model.benchmark_input_node_model import BenchmarkInputNodeModel
from domain_evaluation.model.view.benchmark_calc_node_score_symbol_vm import (
    BenchmarkCalcNodeScoreSymbolViewModel,
)


class BenchmarkExecuteNodeRepository(BasicRepository):
    def insert_benchmark_execute_node(
        self, node: BenchmarkExecuteNodeModel, transaction: Transaction
    ) -> str:
        """
        插入执行节点
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=BenchmarkExecuteNodeEntity, entity_model=node, transaction=transaction
        )

    def insert_benchmark_input_node(
        self, node: BenchmarkInputNodeModel, transaction: Transaction
    ) -> str:
        """
        插入输入节点
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=BenchmarkInputNodeEntity, entity_model=node, transaction=transaction
        )

    def insert_benchmark_calc_node(
        self, node: BenchmarkCalcNodeModel, transaction: Transaction
    ) -> str:
        """
        插入计算节点
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=BenchmarkCalcNodeEntity, entity_model=node, transaction=transaction
        )

    def insert_benchmark_calc_node_stats_args(
        self, args: BenchmarkCalcNodeStatsArgsModel, transaction: Transaction
    ) -> str:
        """
        插入计算节点统计参数
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=BenchmarkCalcNodeStatsArgsEntity, entity_model=args, transaction=transaction
        )

    def insert_benchmark_calc_node_weight_args(
        self, args: BenchmarkCalcNodeWeightArgsModel, transaction: Transaction
    ) -> str:
        """
        插入计算节点权重参数
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=BenchmarkCalcNodeWeightArgsEntity, entity_model=args, transaction=transaction
        )

    def insert_benchmark_calc_node_range_value_args(
        self, args: BenchmarkCalcNodeRangeValueArgsModel, transaction: Transaction
    ) -> str:
        """
        插入计算节点区间取值参数
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=BenchmarkCalcNodeRangeValueArgsEntity,
            entity_model=args,
            transaction=transaction,
        )

    def fetch_calc_node_by_execute_node_id(
        self, benchmark_execute_node_id: str
    ) -> Optional[BenchmarkCalcNodeModel]:
        """
        根据执行节点id获取计算节点信息
        :param benchmark_execute_node_id:
        :return:
        """

        sql = """
        SELECT bc.* FROM st_benchmark_execute_node en 
        INNER JOIN st_benchmark_calc_node bc on en.id = bc.benchmark_execute_node_id
        WHERE en.id = :benchmark_execute_node_id
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=BenchmarkCalcNodeModel,
            params={"benchmark_execute_node_id": benchmark_execute_node_id},
        )

    def fetch_calc_node_stats_args_by_calc_node_id(
        self, benchmark_calc_node_id: str
    ) -> Optional[BenchmarkCalcNodeStatsArgsModel]:
        """
        根据计算节点id获取计算节点统计参数信息
        :param benchmark_calc_node_id:
        :return:
        """

        sql = """
        SELECT * 
        FROM st_benchmark_calc_node_stats_args
        WHERE benchmark_calc_node_id = :benchmark_calc_node_id
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=BenchmarkCalcNodeStatsArgsModel,
            params={"benchmark_calc_node_id": benchmark_calc_node_id},
        )

    def fetch_calc_node_weight_args_by_calc_node_id(
        self, benchmark_calc_node_id: str
    ) -> List[BenchmarkCalcNodeWeightArgsModel]:
        """
        根据计算节点id获取计算节点权重参数信息
        :param benchmark_calc_node_id:
        :return:
        """

        sql = """
        SELECT * 
        FROM st_benchmark_calc_node_weight_args
        WHERE benchmark_calc_node_id = :benchmark_calc_node_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=BenchmarkCalcNodeWeightArgsModel,
            params={"benchmark_calc_node_id": benchmark_calc_node_id},
        )

    def fetch_calc_node_range_value_args_by_calc_node_id(
        self, benchmark_calc_node_id: str
    ) -> List[BenchmarkCalcNodeRangeValueArgsModel]:
        """
        根据计算节点id获取计算节点区间取值参数信息
        :param benchmark_calc_node_id:
        :return:
        """

        sql = """
        SELECT * 
        FROM st_benchmark_calc_node_range_value_args bcsa
        WHERE benchmark_calc_node_id = :benchmark_calc_node_id
        """

        return self._fetch_all_to_model(
            sql=sql,
            model_cls=BenchmarkCalcNodeRangeValueArgsModel,
            params={"benchmark_calc_node_id": benchmark_calc_node_id},
        )

    def fetch_benchmark_calc_node_score_symbol_by_id(
        self, benchmark_calc_node_id: str
    ) -> Optional[BenchmarkCalcNodeScoreSymbolViewModel]:
        """
        根据计算节点id获取计算节点分数符号信息
        :param benchmark_calc_node_id:
        :return:
        """

        sql = """
        select cn.id, row_to_json(iss.*) as input_score_symbol, 
        row_to_json(oss.*) as output_score_symbol
        from st_benchmark_calc_node cn 
        inner join st_score_symbol iss on cn.input_score_symbol_id = iss.id
        inner join st_score_symbol oss on cn.output_score_symbol_id = oss.id
        where cn.id=:benchmark_calc_node_id
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=BenchmarkCalcNodeScoreSymbolViewModel,
            params={"benchmark_calc_node_id": benchmark_calc_node_id},
        )

    def fetch_benchmark_execute_node(self, benchmark_id: str) -> List[BenchmarkExecuteNodeModel]:
        """
        获取指标下的所有执行节点
        """
        sql = """
        select * from st_benchmark_execute_node where benchmark_id = :benchmark_id
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=BenchmarkExecuteNodeModel,
            params={"benchmark_id": benchmark_id},
        )

    def fetch_benchmark_input_node_by_execute_node_id(
        self, benchmark_execute_node_id: str
    ) -> Optional[BenchmarkInputNodeModel]:
        """
        根据执行节点id获取输入节点信息
        :param benchmark_execute_node_id:
        :return:
        """

        sql = """
        SELECT * FROM st_benchmark_input_node
        WHERE benchmark_execute_node_id = :benchmark_execute_node_id
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=BenchmarkInputNodeModel,
            params={"benchmark_execute_node_id": benchmark_execute_node_id},
        )

    def delete_benchmark_input_node(self, input_node_id: str, transaction: Transaction):
        """
        删除输入节点
        """
        self._delete_versioned_entity_by_id(
            entity_cls=BenchmarkInputNodeEntity, entity_id=input_node_id, transaction=transaction
        )

    def delete_benchmark_calc_node(self, calc_node_id: str, transaction: Transaction):
        """
        删除计算节点
        """
        self._delete_versioned_entity_by_id(
            entity_cls=BenchmarkCalcNodeEntity, entity_id=calc_node_id, transaction=transaction
        )

    def delete_calc_node_stats_args(self, stats_args_id: str, transaction: Transaction):
        """
        删除计算节点统计参数
        """
        self._delete_versioned_entity_by_id(
            entity_cls=BenchmarkCalcNodeStatsArgsEntity,
            entity_id=stats_args_id,
            transaction=transaction,
        )

    def delete_calc_node_weight_args(self, weight_args_id: str, transaction: Transaction):
        """
        删除计算节点权重参数
        """
        self._delete_versioned_entity_by_id(
            entity_cls=BenchmarkCalcNodeWeightArgsEntity,
            entity_id=weight_args_id,
            transaction=transaction,
        )

    def delete_calc_node_range_value_args(self, range_value_args_id: str, transaction: Transaction):
        """
        删除计算节点区间取值参数
        """
        self._delete_versioned_entity_by_id(
            entity_cls=BenchmarkCalcNodeRangeValueArgsEntity,
            entity_id=range_value_args_id,
            transaction=transaction,
        )

    def delete_benchmark_execute_node(self, execute_node_id: str, transaction: Transaction):
        """
        删除执行节点
        """
        self._delete_versioned_entity_by_id(
            entity_cls=BenchmarkExecuteNodeEntity,
            entity_id=execute_node_id,
            transaction=transaction,
        )

    def fetch_benchmark_input_node_by_id(
        self, input_node_id: str
    ) -> Optional[BenchmarkInputNodeModel]:
        """
        根据输入节点id获取输入节点信息
        :param input_node_id:
        :return:
        """

        sql = """
        SELECT * FROM st_benchmark_input_node
        WHERE id = :input_node_id
        """

        return self._fetch_first_to_model(
            sql=sql,
            model_cls=BenchmarkInputNodeModel,
            params={"input_node_id": input_node_id},
        )

    def fetch_input_node_by_source_benchmark_id(
        self, source_benchmark_id: str
    ) -> List[BenchmarkInputNodeModel]:
        """
        根据源benchmark的id获取输入节点信息
        """
        sql = """
        select * from st_benchmark_input_node
        where source_benchmark_id = :source_benchmark_id
        and finish_at = 'infinity'
        """
        return self._fetch_all_to_model(
            sql=sql,
            model_cls=BenchmarkInputNodeModel,
            params={"source_benchmark_id": source_benchmark_id},
        )

    def update_benchmark_input_node(
        self,
        input_node: BenchmarkInputNodeModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新输入节点
        通常只更新finish_at
        """
        self._update_versioned_entity_by_model(
            entity_cls=BenchmarkInputNodeEntity,
            update_model=input_node,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def fetch_benchmark_input_node_list(self, benchmark_id: str) -> List[BenchmarkInputNodeModel]:
        """
        获取基准的输入节点列表
        """
        sql = """
        select sin.* from st_benchmark_execute_node sen
        inner join st_benchmark_input_node sin on sen.id = sin.benchmark_execute_node_id
        where sen.benchmark_id = :benchmark_id
        and finish_at = 'infinity'
        """
        return self._fetch_all_to_model(
            model_cls=BenchmarkInputNodeModel,
            sql=sql,
            params={"benchmark_id": benchmark_id},
        )

    def fetch_benchmark_calc_node_list(
        self, benchmark_id: str
    ) -> List[BenchmarkCalcNodeModel]:
        """
        获取基准的计算节点列表
        :param benchmark_id:
        :return:
        """
        sql = """
        select scn.* from st_benchmark_execute_node sen
        inner join st_benchmark_calc_node scn on sen.id = scn.benchmark_execute_node_id
        where sen.benchmark_id = :benchmark_id
        """
        return self._fetch_all_to_model(
            model_cls=BenchmarkCalcNodeModel,
            sql=sql,
            params={"benchmark_id": benchmark_id},
        )

