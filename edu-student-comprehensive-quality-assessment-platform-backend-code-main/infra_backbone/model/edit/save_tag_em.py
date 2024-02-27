from typing import List, Optional

from infra_basic.basic_model import BasePlusModel


class SaveTagOwnershipRelationshipEditModel(BasePlusModel):
    resource_category: str
    resource_id: str
    relationship: str


class SaveTagEditModel(BasePlusModel):
    id: Optional[str]
    name: str
    code: Optional[str]
    owner_category: Optional[str]
    owner_id: Optional[str]
    is_editable: bool = True
    is_activated: bool = True

    tag_ownership_relationship_list: List[SaveTagOwnershipRelationshipEditModel] = []
