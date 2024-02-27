from typing import List, Optional

from infra_basic.basic_model import BasePlusModel


class AdditionalRuleOption(BasePlusModel):
    name: str
    value: str


class AdditionalRule(BasePlusModel):
    component_type: str
    options_description: Optional[str]
    options: List[AdditionalRuleOption] = []


class BenchmarkDefinitionViewModel(BasePlusModel):
    calc_method: str
    name: str
    rule: Optional[AdditionalRule]
