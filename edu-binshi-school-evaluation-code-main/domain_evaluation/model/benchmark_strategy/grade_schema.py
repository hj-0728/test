from infra_utility.base_plus_model import BasePlusModel

from domain_evaluation.data.enum import EnumComponentType
from domain_evaluation.model.benchmark_strategy.basic_schema import BasicSchema


class GradeItemValue(BasePlusModel):
    source_benchmark_id: str
    input_score_symbol_id: str


class GradeItem(BasePlusModel):
    name: str
    value: GradeItemValue


class GradeSchema(BasePlusModel):
    source_benchmark: BasicSchema = BasicSchema(
        title="分数来源",
        form_name="sourceBenchmark",
        component_type=EnumComponentType.SINGLE_CHOICE.name,
        items=[],
    )

    range_value_args: BasicSchema = BasicSchema(
        title="规则",
        form_name="rangeValueArgs",
        component_type=EnumComponentType.RANGE_VALUE.name,
    )
