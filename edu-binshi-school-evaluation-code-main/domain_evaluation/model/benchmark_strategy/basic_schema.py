from typing import Dict, List, Optional, Union

from infra_basic.basic_model import BasePlusModel


class NameValuePair(BasePlusModel):
    name: str
    value: str
    is_activated: bool = True


class WeightValuePair(NameValuePair):
    weight: Optional[int]


class BasicSchema(BasePlusModel):
    title: str
    form_name: Union[str, Dict]
    component_type: str
    items: List[NameValuePair] = []


class BasicNumSchema(BasicSchema):
    min: Optional[int]
    max: Optional[int]
    numeric_precision: int = 0
