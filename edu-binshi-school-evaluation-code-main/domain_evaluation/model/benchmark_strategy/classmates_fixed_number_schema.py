from infra_basic.basic_model import BasePlusModel

from domain_evaluation.data.enum import EnumComponentType
from domain_evaluation.model.benchmark_strategy.basic_schema import BasicNumSchema, BasicSchema


class ClassmatesFixedNumberSchema(BasePlusModel):
    classmates_number: BasicNumSchema = BasicNumSchema(
        title="参与同学数量",
        min=2,
        form_name="classmatesNumber",
        component_type=EnumComponentType.INTEGER.name,
    )
    stats_method: BasicSchema = BasicSchema(
        title="统计方法",
        form_name="statsMethod",
        component_type=EnumComponentType.SINGLE_CHOICE.name,
    )
