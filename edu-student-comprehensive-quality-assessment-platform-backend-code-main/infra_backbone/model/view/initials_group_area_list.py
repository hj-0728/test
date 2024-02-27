from typing import List

from infra_basic.basic_model import BasePlusModel

from infra_backbone.model.area_model import AreaModel


class InitialsGroupAreaList(BasePlusModel):
    initials: str
    area_list: List[AreaModel]
