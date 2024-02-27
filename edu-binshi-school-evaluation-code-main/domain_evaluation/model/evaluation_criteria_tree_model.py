from datetime import datetime
from typing import Dict, List, Optional

from infra_basic.basic_model import VersionedModel
from infra_utility.datetime_helper import local_now

from domain_evaluation.model.benchmark_calc_node_model import (
    BenchmarkCalcNodeRangeValueArgsModel,
    BenchmarkCalcNodeStatsArgsModel,
    BenchmarkCalcNodeWeightArgsModel,
)
from domain_evaluation.model.indicator_model import IndicatorModel
from domain_evaluation.model.score_symbol_model import ScoreSymbolModel


class EvaluationCriteriaTreeModel(VersionedModel):
    """
    评价标准的树（对用户可以叫评价项）
    """

    evaluation_criteria_id: str
    parent_indicator_id: Optional[str]
    indicator_id: str
    seq: int
    start_at: datetime
    finish_at: datetime


class BenchmarkListItemModel(VersionedModel):
    """
    基准
    """

    name: str
    guidance: Optional[str]
    calc_method: Optional[str]
    input_score_symbol: Optional[ScoreSymbolModel]
    output_score_symbol: Optional[ScoreSymbolModel]
    numeric_min_score: Optional[float]
    numeric_max_score: Optional[float]
    limited_string_options: Optional[List[str]]
    classmates_count: Optional[int]
    stats_method: Optional[str]
    options_value: Optional[str]
    range_value_list: List[BenchmarkCalcNodeRangeValueArgsModel] = []


class SaveEvaluationCriteriaTreeModel(VersionedModel):
    """
    评价标准的树（对用户可以叫评价项）
    """

    evaluation_criteria_id: Optional[str]
    parent_indicator_id: Optional[str]
    indicator_id: Optional[str]
    name: str
    seq: Optional[int]
    indicator_version: Optional[int] = 1
    level: Optional[int] = 1
    comments: Optional[str]
    benchmark_list: Optional[List[BenchmarkListItemModel]]
    tag_ownership_id: Optional[str]
    start_at: Optional[datetime]
    finish_at: Optional[datetime]

    def to_evaluation_criteria_tree_model(self) -> EvaluationCriteriaTreeModel:
        """
        为了编辑的
        """
        return EvaluationCriteriaTreeModel(
            id=self.id,
            version=self.version,
            evaluation_criteria_id=self.evaluation_criteria_id,
            parent_indicator_id=self.parent_indicator_id,
            indicator_id=self.indicator_id,
            seq=self.seq,
            start_at=self.start_at if self.start_at else local_now(),
            finish_at="infinity",
        )

    def to_save_evaluation_criteria_tree_model(self) -> EvaluationCriteriaTreeModel:
        """
        为了新建的
        """
        return EvaluationCriteriaTreeModel(
            evaluation_criteria_id=self.evaluation_criteria_id,
            parent_indicator_id=self.parent_indicator_id,
            indicator_id=self.indicator_id,
            seq=self.seq,
            start_at=local_now(),
            finish_at="infinity",
        )

    def to_indicator_model(self) -> IndicatorModel:
        return IndicatorModel(
            id=self.indicator_id if self.indicator_id else None,
            version=self.indicator_version if self.indicator_version else 1,
            name=self.name,
            comments=self.comments,
            start_at=local_now(),
            finish_at="infinity",
        )


class BenchmarkInputNodeInfoVm(VersionedModel):
    """
    输入节点
    """

    category: str
    input_score_symbol: ScoreSymbolModel
    numeric_min_score: Optional[float]
    numeric_max_score: Optional[float]
    limited_string_options: Optional[List[str]]
    filler_calc_method: Optional[str]
    filler_calc_context: Optional[Dict]


class BenchmarkCalcNodeInfoVm(VersionedModel):
    """
    计算节点
    """

    benchmark_calc_node_stats_args_info: Optional[BenchmarkCalcNodeStatsArgsModel]
    benchmark_calc_node_weight_args_info: Optional[BenchmarkCalcNodeWeightArgsModel]
    benchmark_calc_node_range_value_args_info: Optional[BenchmarkCalcNodeRangeValueArgsModel]
    input_score_symbol_id: str
    output_score_symbol_id: str
    calc_method: str


class BenchmarkListItemVm(VersionedModel):
    """
    基准列表for view
    """

    name: Optional[str]
    guidance: Optional[str]
    benchmark_strategy_id: Optional[str]
    benchmark_strategy_code: Optional[str]
    source_category: Optional[str]
    benchmark_input_node_id_list: Optional[List[str]]


class EvaluationCriteriaTreeInfoModel(VersionedModel):
    """
    评价标准的树（对用户可以叫评价项）
    """

    evaluation_criteria_id: str
    evaluation_criteria_tree_id: Optional[str]
    parent_indicator_id: Optional[str]
    indicator_id: Optional[str]
    name: Optional[str]
    comments: Optional[str]
    indicator_version: Optional[int]

    seq: Optional[int]
    tag_ownership_id: Optional[str]
    tag_ownership_relationship_id: Optional[str]
