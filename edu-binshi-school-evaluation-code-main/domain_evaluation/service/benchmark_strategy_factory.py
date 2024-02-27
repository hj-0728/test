import importlib
import re
from typing import List, Optional, Type, TypeVar

from infra_basic.errors import BusinessError
from infra_utility.algorithm.tree import list_to_tree, TreeNodeModel
from infra_utility.base_plus_model import BasePlusModel
from infra_utility.enum_helper import enum_to_dict_list

from domain_evaluation.data.enum import EnumComponentType
from domain_evaluation.model.benchmark_calc_node_model import EnumBenchmarkCalcNodeStatsMethod
from domain_evaluation.model.benchmark_strategy.aggregated_process_params_type import (
    AggregatedProcessParamsType,
)
from domain_evaluation.model.benchmark_strategy.basic_schema import (
    BasicNumSchema,
    BasicSchema,
    NameValuePair,
    WeightValuePair,
)
from domain_evaluation.model.benchmark_strategy.built_benchmark_node import BuiltBenchmarkNode
from domain_evaluation.model.benchmark_strategy.classmates_fixed_number_process_params_type import (
    ClassmatesFixedNumberProcessParamsType,
)
from domain_evaluation.model.benchmark_strategy.classmates_fixed_number_schema import (
    ClassmatesFixedNumberSchema,
)
from domain_evaluation.model.benchmark_strategy.grade_process_params_type import (
    GradeProcessParamsType,
)
from domain_evaluation.model.benchmark_strategy.grade_schema import GradeSchema
from domain_evaluation.model.benchmark_strategy.input_no_extra_property_process_params_type import (
    InputNoExtraPropertyProcessParamsType,
)
from domain_evaluation.model.benchmark_strategy.only_one_teacher_process_params_type import (
    OnlyOneTeacherProcessParamsType,
)
from domain_evaluation.model.benchmark_strategy.only_one_teacher_schema import OnlyOneTeacherSchema
from domain_evaluation.model.benchmark_strategy.only_one_team_category_process_params_type import (
    OnlyOneTeamCategoryProcessParamsType,
)
from domain_evaluation.model.benchmark_strategy.only_one_team_category_schema import (
    OnlyOneTeamCategorySchema,
)
from domain_evaluation.model.benchmark_strategy.same_level_aggregated_schema import (
    SameLevelAggregatedSchema,
)
from domain_evaluation.model.benchmark_strategy.same_level_stats_schema import SameLevelStatsSchema
from domain_evaluation.model.benchmark_strategy.score_symbol_schema import ScoreSymbolSchema
from domain_evaluation.model.benchmark_strategy.stats_process_params_type import (
    StatsProcessParamsType,
)
from domain_evaluation.model.benchmark_strategy.sub_level_aggregated_schema import (
    SubLevelAggregatedSchema,
    SubLevelAggregatedTreeItem,
)
from domain_evaluation.model.benchmark_strategy.sub_level_stats_schema import SubLevelStatsSchema
from domain_evaluation.model.benchmark_strategy_model import EnumBenchmarkStrategyScoreSymbolScope
from domain_evaluation.model.score_symbol_model import EnumScoreSymbolValueType, ScoreSymbolModel
from domain_evaluation.model.view.sub_level_indicator_tree_vm import SubLevelIndicatorTreeItem
from domain_evaluation.repository.benchmark_repository import BenchmarkRepository
from domain_evaluation.repository.score_symbol_repository import ScoreSymbolRepository
from edu_binshi.repository.subject_repository import SubjectRepository
from infra_backbone.repository.team_category_repository import TeamCategoryRepository

GenericModelData = TypeVar("GenericModelData", bound=BasePlusModel)
GenericTreeModelData = TypeVar("GenericTreeModelData", bound=TreeNodeModel)


class BenchmarkStrategyFactory:
    def __init__(
        self,
        subject_repository: SubjectRepository,
        score_symbol_repository: ScoreSymbolRepository,
        team_category_repository: TeamCategoryRepository,
        benchmark_repository: BenchmarkRepository,
    ):
        self._subject_repository = subject_repository
        self._score_symbol_repository = score_symbol_repository
        self._team_category_repository = team_category_repository
        self._benchmark_repository = benchmark_repository

    @staticmethod
    def camel_to_snake(name: str) -> str:
        """
        驼峰转下划线
        """
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    def load_model_cls(self, model_cls_name: str) -> Type[BasePlusModel]:
        # 动态加载模块
        model_file_name = self.camel_to_snake(name=model_cls_name)
        model_module = f"domain_evaluation.model.benchmark_strategy.{model_file_name}"
        module = importlib.import_module(model_module)
        # 获取模块中的类
        model_class = getattr(module, model_cls_name)
        # 检查类是否继承自 BasePlusModel
        if not issubclass(model_class, BasePlusModel):
            raise TypeError(f"{model_cls_name} must be a subclass of pydantic.BaseModel")
        return model_class

    def prepare_score_symbol_params(
        self, score_symbol_scope: str, need_item_schema: bool
    ) -> Optional[ScoreSymbolSchema]:
        """
        准备分数符号参数
        """
        if score_symbol_scope == EnumBenchmarkStrategyScoreSymbolScope.CUSTOM.name:
            score_symbol_list = []
        elif score_symbol_scope == EnumBenchmarkStrategyScoreSymbolScope.BOTH.name:
            score_symbol_list = self._score_symbol_repository.fetch_score_symbol()
        else:
            score_symbol_list = self._score_symbol_repository.fetch_score_symbol(
                value_type=score_symbol_scope
            )

        items = []
        item_params = {}
        for score_symbol in score_symbol_list:
            items.append(
                {
                    "name": score_symbol.name,
                    "value": score_symbol.id,
                    "is_activated": score_symbol.is_activated,
                }
            )

            if need_item_schema:
                item_schema = self._prepare_score_symbol_item_params(score_symbol=score_symbol)
                item_params[score_symbol.id] = item_schema

        return ScoreSymbolSchema(
            title="得分符号",
            form_name="scoreSymbolId",
            component_type=EnumComponentType.SINGLE_CHOICE.name,
            items=items,
            item_params=item_params if need_item_schema else None,
        )

    @staticmethod
    def _prepare_score_symbol_item_params(score_symbol: ScoreSymbolModel) -> BasicSchema:
        """
        准备分数符号参数
        """
        if score_symbol.value_type == EnumScoreSymbolValueType.NUM.name:
            num_schema = BasicNumSchema(
                title="最高得分值",
                component_type=EnumComponentType.INTEGER.name,
                form_name="numericMaxScore",
                numeric_precision=score_symbol.numeric_precision,
            )
            return num_schema
        schema = BasicSchema(
            title="可选项",
            component_type=EnumComponentType.MULTIPLE_CHOICE.name,
            items=[{"name": x, "value": x} for x in score_symbol.string_options],
            form_name="limitedStringOptions",
        )
        return schema

    def prepare_only_one_teacher_schema(self) -> OnlyOneTeacherSchema:
        """
        准备仅一个老师参与时的参数
        """
        subject_list = self._subject_repository.get_subject_list()
        schema = OnlyOneTeacherSchema()
        schema.subject.items = [{"name": x.name, "value": x.id} for x in subject_list]
        return schema

    @staticmethod
    def build_only_one_teacher_node(
        benchmark_id, process_data: OnlyOneTeacherProcessParamsType
    ) -> List[BuiltBenchmarkNode]:
        """
        构建仅一个老师参与时的节点
        """
        built_node = process_data.to_built_input_node(benchmark_id=benchmark_id)
        return [built_node]

    @staticmethod
    def prepare_classmates_fixed_number_schema() -> ClassmatesFixedNumberSchema:
        """
        准备同班同学-固定人数参与时的参数
        """
        stats_method = enum_to_dict_list(
            enum_class=EnumBenchmarkCalcNodeStatsMethod, name_col="value", value_col="name"
        )
        json_schema = ClassmatesFixedNumberSchema()
        json_schema.stats_method.items = stats_method
        return json_schema

    @staticmethod
    def build_classmates_fixed_number_node(
        benchmark_id, process_data: ClassmatesFixedNumberProcessParamsType
    ) -> List[BuiltBenchmarkNode]:
        """
        构建同班同学-固定人数参与时的节点
        """
        calc_exec_node = process_data.to_built_calc_node(benchmark_id=benchmark_id)
        input_exec_node = process_data.to_built_input_node(
            benchmark_id=benchmark_id, calc_exec_node_id=calc_exec_node.id
        )
        return [calc_exec_node, input_exec_node]

    @staticmethod
    def prepare_no_extra_property_schema() -> None:
        """
        因为有一类的策略是不需要额外的属性的，所以这里返回 None
        """
        return None

    @staticmethod
    def build_self_node(
        benchmark_id, process_data: InputNoExtraPropertyProcessParamsType
    ) -> List[BuiltBenchmarkNode]:
        """
        构建本人参与时的节点
        """
        built_node = process_data.to_built_input_node(
            benchmark_id=benchmark_id, filler_calc_method="SelfBenchmark", name="本人"
        )
        return [built_node]

    @staticmethod
    def build_only_one_head_teacher_node(
        benchmark_id, process_data: InputNoExtraPropertyProcessParamsType
    ) -> List[BuiltBenchmarkNode]:
        """
        构建只有一个班主任参与时的节点
        """
        built_node = process_data.to_built_input_node(
            benchmark_id=benchmark_id, filler_calc_method="HeadTeacherBenchmark", name="仅一位班主任参与"
        )
        return [built_node]

    def prepare_only_one_team_category_schema(
        self, benchmark_id: Optional[str]
    ) -> OnlyOneTeamCategorySchema:
        """
        准备一种小组类型参与时的参数
        """

        team_category_list = self._team_category_repository.get_team_category_for_prepare_only_one_team_category_schema(
            benchmark_id=benchmark_id
        )
        schema = OnlyOneTeamCategorySchema()
        schema.team_category.items = [
            {"name": x.name, "value": x.id, "disabled": not x.is_activated}
            for x in team_category_list
        ]
        return schema

    @staticmethod
    def build_only_one_team_category_node(
        benchmark_id, process_data: OnlyOneTeamCategoryProcessParamsType
    ) -> List[BuiltBenchmarkNode]:
        """
        构建一种小组类型参与时的节点
        """
        built_node = process_data.to_built_input_node(benchmark_id=benchmark_id)
        return [built_node]

    def fetch_indicator_same_symbol_benchmark(
        self, indicator_id: str, score_symbol_id: str, benchmark_id: Optional[str]
    ) -> List[NameValuePair]:
        """
        同一指标的下符号类型相同的基准
        :param indicator_id:
        :param score_symbol_id:
        :param benchmark_id:
        :return:
        """

        source_benchmark_list = self._benchmark_repository.fetch_indicator_same_symbol_benchmark(
            indicator_id=indicator_id, score_symbol_id=score_symbol_id, benchmark_id=benchmark_id
        )
        if len(source_benchmark_list) < 2:
            raise BusinessError("可选得分符号相同的评价分类少于两个，无法聚合。")

        return source_benchmark_list

    def prepare_same_level_aggregated_schema(
        self, indicator_id: str, score_symbol_id: str, benchmark_id: Optional[str]
    ) -> SameLevelAggregatedSchema:
        """
        准备同一层级分值聚合时的参数
        """
        schema = SameLevelAggregatedSchema()
        source_benchmark_list = self.fetch_indicator_same_symbol_benchmark(
            indicator_id=indicator_id, score_symbol_id=score_symbol_id, benchmark_id=benchmark_id
        )
        source_benchmark_items = []
        for source_benchmark in source_benchmark_list:
            source_benchmark_items.append(source_benchmark.cast_to(cast_type=WeightValuePair))
        schema.source_benchmark.items = source_benchmark_items
        return schema

    def prepare_same_level_stats_schema(
        self, indicator_id: str, score_symbol_id: str, benchmark_id: Optional[str]
    ) -> SameLevelStatsSchema:
        """
        准备同一层级分值求和时的参数
        :param indicator_id:
        :param score_symbol_id:
        :param benchmark_id:
        :return:
        """

        schema = SameLevelStatsSchema()
        schema.source_benchmark.items = self.fetch_indicator_same_symbol_benchmark(
            indicator_id=indicator_id, score_symbol_id=score_symbol_id, benchmark_id=benchmark_id
        )
        return schema

    @staticmethod
    def build_aggregated_node(
        benchmark_id, process_data: AggregatedProcessParamsType
    ) -> List[BuiltBenchmarkNode]:
        """
        构建同一层级分值聚合时的节点
        """

        calc_exec_node = process_data.to_built_calc_node(benchmark_id=benchmark_id)
        input_exec_node_list = process_data.to_built_input_node(
            benchmark_id=benchmark_id, exec_calc_node_id=calc_exec_node.id
        )
        return [calc_exec_node, *input_exec_node_list]

    @staticmethod
    def build_stats_node(
        benchmark_id, process_data: StatsProcessParamsType
    ) -> List[BuiltBenchmarkNode]:
        """
        构建统计节点
        """

        calc_exec_node = process_data.to_built_calc_node(benchmark_id=benchmark_id)
        input_exec_node_list = process_data.to_built_input_node(
            benchmark_id=benchmark_id, exec_calc_node_id=calc_exec_node.id
        )
        return [calc_exec_node, *input_exec_node_list]

    def fetch_sub_indicator_same_symbol_benchmark_tree(
        self, indicator_id: str, score_symbol_id: str, tree_node_type: Type[GenericTreeModelData]
    ) -> List[GenericTreeModelData]:
        """
        获取子指标相同符合的基准树
        :param indicator_id:
        :param score_symbol_id:
        :param tree_node_type:
        :return:
        """

        source_benchmark_list = (
            self._benchmark_repository.fetch_sub_indicator_same_symbol_benchmark(
                indicator_id=indicator_id, score_symbol_id=score_symbol_id
            )
        )
        source_benchmark_tree = list_to_tree(
            original_list=source_benchmark_list,
            tree_node_type=tree_node_type,
            id_attr="value",
            parent_id_attr="parent_id",
            seq_attr="seq",
        )

        checkable_benchmark = [x for x in source_benchmark_list if x.checkable]
        if len(checkable_benchmark) < 1:
            raise BusinessError("暂无可选项，请选择其他策略")

        return source_benchmark_tree

    def prepare_sub_level_aggregated_schema(
        self, indicator_id: str, score_symbol_id: str
    ) -> SubLevelAggregatedSchema:
        """
        准备子级分值聚合时的参数
        """
        schema = SubLevelAggregatedSchema()
        schema.source_benchmark.items = self.fetch_sub_indicator_same_symbol_benchmark_tree(
            indicator_id=indicator_id,
            score_symbol_id=score_symbol_id,
            tree_node_type=SubLevelAggregatedTreeItem,
        )
        return schema

    def prepare_sub_level_stats_schema(
        self, indicator_id: str, score_symbol_id: str
    ) -> SubLevelStatsSchema:
        """
        准备子级分值聚合时的参数
        """
        schema = SubLevelStatsSchema()
        schema.source_benchmark.items = self.fetch_sub_indicator_same_symbol_benchmark_tree(
            indicator_id=indicator_id,
            score_symbol_id=score_symbol_id,
            tree_node_type=SubLevelIndicatorTreeItem,
        )
        return schema

    def prepare_grade_schema(self, indicator_id: str) -> GradeSchema:
        """
        准备同级的参数
        """
        schema = GradeSchema()
        source_benchmark_list = self._benchmark_repository.fetch_same_level_num_benchmark(
            indicator_id=indicator_id
        )
        schema.source_benchmark.items = source_benchmark_list
        return schema

    @staticmethod
    def build_grade_node(
        benchmark_id: str, process_data: GradeProcessParamsType
    ) -> List[BuiltBenchmarkNode]:
        """
        构建同一层级分值聚合时的节点
        """

        calc_exec_node = process_data.to_built_calc_node(benchmark_id=benchmark_id)
        input_exec_node = process_data.to_built_input_node(
            benchmark_id=benchmark_id, exec_calc_node_id=calc_exec_node.id
        )
        return [calc_exec_node, input_exec_node]
