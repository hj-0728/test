import logging
import statistics
from typing import Any, List, Optional, Tuple

from infra_basic.errors import BusinessError
from infra_utility.enum_helper import get_enum_name_list

from domain_evaluation.model.benchmark_calc_node_model import (
    BenchmarkCalcNodeModel,
    BenchmarkCalcNodeRangeValueArgsModel,
    BenchmarkCalcNodeStatsArgsModel,
    BenchmarkCalcNodeWeightArgsModel,
    EnumBenchmarkCalcMethod,
    EnumBenchmarkCalcNodeStatsMethod,
)
from domain_evaluation.model.score_symbol_model import EnumScoreSymbolValueType, ScoreSymbolModel
from domain_evaluation.model.view.benchmark_calc_node_score_symbol_vm import (
    BenchmarkCalcNodeScoreSymbolViewModel,
)
from domain_evaluation.repository.benchmark_execute_node_repository import (
    BenchmarkExecuteNodeRepository,
)


class NodeCalcMethodService:
    """
    节点计算方式 service
    """

    def __init__(
        self,
        benchmark_execute_node_repository: BenchmarkExecuteNodeRepository,
    ):
        self.__benchmark_execute_node_repository = benchmark_execute_node_repository

    def calc_node(
        self,
        node_id: str,
        numeric_score_list: List[Optional[float]],
    ) -> Tuple[float, str]:
        """
        计算基准分数
        :param node_id:
        :param numeric_score_list:
        :return:
        """

        # 1. 获取节点
        calc_node = self.__benchmark_execute_node_repository.fetch_calc_node_by_execute_node_id(
            benchmark_execute_node_id=node_id
        )

        calc_method_list = get_enum_name_list(enum_class=EnumBenchmarkCalcMethod)
        if calc_node.calc_method not in calc_method_list:
            raise BusinessError("未知的节点计算方式")

        args = self.fetch_calc_method_args(
            calc_node=calc_node,
        )

        calc_score_symbol = (
            self.__benchmark_execute_node_repository.fetch_benchmark_calc_node_score_symbol_by_id(
                benchmark_calc_node_id=calc_node.id
            )
        )

        return self.calc(
            calc_score_symbol=calc_score_symbol,
            calc_method=calc_node.calc_method.lower(),
            numeric_score_list=numeric_score_list,
            args=args,
        )

    def fetch_calc_method_args(self, calc_node: BenchmarkCalcNodeModel) -> Any:
        """

        :param calc_node:
        :return:
        """

        calc_method_args = {
            EnumBenchmarkCalcMethod.WEIGHT.name: self.__benchmark_execute_node_repository.fetch_calc_node_weight_args_by_calc_node_id,
            EnumBenchmarkCalcMethod.RANGE_VALUE.name: self.__benchmark_execute_node_repository.fetch_calc_node_range_value_args_by_calc_node_id,
            EnumBenchmarkCalcMethod.STATS.name: self.__benchmark_execute_node_repository.fetch_calc_node_stats_args_by_calc_node_id,
        }

        return calc_method_args[calc_node.calc_method](benchmark_calc_node_id=calc_node.id)

    def calc(
        self,
        calc_score_symbol: BenchmarkCalcNodeScoreSymbolViewModel,
        calc_method: str,
        numeric_score_list: List[Optional[float]],
        args: Any,
    ) -> Tuple[float, str]:
        """
        计算
        :param calc_score_symbol:
        :param calc_method:
        :param numeric_score_list:
        :param args:
        :return:
        """

        # 前置校验

        self.validate_value_by_score_symbol(
            score_symbol=calc_score_symbol.input_score_symbol,
            numeric_score_list=numeric_score_list,
        )

        calc_method = getattr(self, calc_method)

        numeric_score, string_score = calc_method(
            numeric_score_list=numeric_score_list,
            args=args,
        )

        # 后置校验
        self.validate_value_by_score_symbol(
            score_symbol=calc_score_symbol.output_score_symbol,
            numeric_score_list=[numeric_score],
            string_score_list=[string_score],
        )

        return numeric_score, string_score

    @staticmethod
    def validate_value_by_score_symbol(
        score_symbol: ScoreSymbolModel,
        numeric_score_list: Optional[List[Optional[float]]] = None,
        string_score_list: Optional[List[Optional[str]]] = None,
    ):
        """
        根据分数符号校验值
        :param score_symbol:
        :param numeric_score_list:
        :param string_score_list:
        :return:
        """

        if score_symbol.value_type == EnumScoreSymbolValueType.NUM.name:
            if not numeric_score_list:
                raise BusinessError("分数符号值类型与分数值类型不匹配，或没有分数")
            power_value = 0
            if score_symbol.numeric_precision:
                power_value = 10 ** (score_symbol.numeric_precision * -1)
            for numeric_score in numeric_score_list:
                if numeric_score is None:
                    raise BusinessError("分数值不能为空")
                if power_value and not numeric_score % power_value != 0:
                    raise BusinessError("分数值精度错误")
        else:
            if not string_score_list:
                raise BusinessError("分数符号值类型与分数值类型不匹配")
            for string_score in string_score_list:
                if string_score is None:
                    raise BusinessError("分数值不能为空")
                if string_score not in score_symbol.string_options:
                    raise BusinessError("分数值不在分数符号值列表中")

    @staticmethod
    def range_value(
        numeric_score_list: List[Optional[float]],
        args: List[BenchmarkCalcNodeRangeValueArgsModel],
    ) -> Tuple[Optional[float], Optional[str]]:
        """
        区间取值
        :param numeric_score_list:
        :param args:
        :return:
        """

        if not numeric_score_list or numeric_score_list[0] is None:
            raise BusinessError("区间取值参数错误")

        for range_info in args:
            expression = (
                f"{numeric_score_list[0]} {range_info.left_operator} {range_info.min_score} and "
                f"{numeric_score_list[0]} {range_info.right_operator} {range_info.max_score}"
            )
            if eval(expression):
                return None, range_info.match_value
        logging.error('分数在区间取值之外')
        return None, None

    @staticmethod
    def stats(
        numeric_score_list: List[Optional[float]],
        args: BenchmarkCalcNodeStatsArgsModel,
    ) -> Tuple[Optional[float], Optional[str]]:
        """
        统计
        :param numeric_score_list:
        :param args:
        :return:
        """

        for numeric_score in numeric_score_list:
            if numeric_score is None:
                raise BusinessError("统计参数错误")

        if args.stats_method == EnumBenchmarkCalcNodeStatsMethod.SUM.name:
            return sum(numeric_score_list), None

        if args.stats_method == EnumBenchmarkCalcNodeStatsMethod.AVG.name:
            return statistics.mean(numeric_score_list), None

        if args.stats_method == EnumBenchmarkCalcNodeStatsMethod.MAX.name:
            return max(numeric_score_list), None

        if args.stats_method == EnumBenchmarkCalcNodeStatsMethod.MIN.name:
            return min(numeric_score_list), None

        if args.stats_method == EnumBenchmarkCalcNodeStatsMethod.MEDIAN.name:
            return statistics.median(numeric_score_list), None

        if args.stats_method == EnumBenchmarkCalcNodeStatsMethod.MODE.name:
            return statistics.mode(numeric_score_list), None

    @staticmethod
    def weight(
        numeric_score_list: List[Optional[float]],
        args: List[BenchmarkCalcNodeWeightArgsModel],
    ) -> Tuple[Optional[float], Optional[str]]:
        """
        权重
        :param numeric_score_list:
        :param args:
        :return:
        """

        value = 0

        weight_sum = 0

        for weight_value in args:
            if (
                weight_value.seq > len(numeric_score_list)
                or numeric_score_list[weight_value.seq - 1] is None
            ):
                raise BusinessError("权重参数错误")
            weight_sum += weight_value.weight
            value += weight_value.weight * numeric_score_list[weight_value.seq - 1]

        if weight_sum:
            return value / weight_sum, None
        return value, None
