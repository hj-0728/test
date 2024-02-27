from infra_basic.basic_model import BasePlusModel

from domain_evaluation.data.enum import EnumComponentType
from domain_evaluation.model.benchmark_strategy.basic_schema import BasicSchema


class OnlyOneTeacherSchema(BasePlusModel):
    subject: BasicSchema = BasicSchema(
        title="科目",
        form_name="subjectId",
        component_type=EnumComponentType.SINGLE_CHOICE.name,
    )
