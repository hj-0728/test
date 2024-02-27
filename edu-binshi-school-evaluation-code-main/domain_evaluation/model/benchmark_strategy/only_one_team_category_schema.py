from infra_basic.basic_model import BasePlusModel

from domain_evaluation.data.enum import EnumComponentType
from domain_evaluation.model.benchmark_strategy.basic_schema import BasicSchema


class OnlyOneTeamCategorySchema(BasePlusModel):
    team_category: BasicSchema = BasicSchema(
        title="小组类型",
        form_name="teamCategoryId",
        component_type=EnumComponentType.SINGLE_CHOICE.name,
    )
