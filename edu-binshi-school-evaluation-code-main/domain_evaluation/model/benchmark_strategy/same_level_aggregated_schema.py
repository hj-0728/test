from infra_utility.base_plus_model import BasePlusModel

from domain_evaluation.data.enum import EnumComponentType
from domain_evaluation.model.benchmark_strategy.basic_schema import BasicSchema


class SameLevelAggregatedSchema(BasePlusModel):
    source_benchmark: BasicSchema = BasicSchema(
        title="可选项",
        form_name="sourceBenchmark",
        component_type=EnumComponentType.WEIGHT.name,
        items=[],
    )
