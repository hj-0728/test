from typing import List, Optional

from infra_utility.algorithm.tree import TreeNodeModel
from infra_utility.base_plus_model import BasePlusModel

from domain_evaluation.data.enum import EnumComponentType
from domain_evaluation.model.benchmark_strategy.basic_schema import (
    BasicSchema,
    NameValuePair,
    WeightValuePair,
)
from domain_evaluation.model.view.sub_level_indicator_tree_vm import \
    SubLevelIndicatorTreeItem


class ChildWeightValuePair(WeightValuePair):
    parent_id: str


class SubLevelAggregatedItem(NameValuePair):
    children: List[ChildWeightValuePair] = []


class SubLevelAggregatedSchema(BasePlusModel):
    source_benchmark: BasicSchema = BasicSchema(
        title="可选项",
        form_name="sourceBenchmark",
        component_type=EnumComponentType.TREE_SELECT.name,
        items=[],
    )


class SubLevelAggregatedTreeItem(SubLevelIndicatorTreeItem):
    weight: Optional[int]
