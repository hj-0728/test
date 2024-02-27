from typing import List

from infra_basic.basic_model import BasePlusModel

from infra_backbone.model.area_model import AreaModel
from infra_backbone.model.view.initials_group_area_list import InitialsGroupAreaList


class OrganizationAddressAreaViewModel(BasePlusModel):
    area_list: List[InitialsGroupAreaList]
    parent_area_list: List[AreaModel] = []
