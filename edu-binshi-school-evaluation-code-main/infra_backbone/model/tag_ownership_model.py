from typing import Optional

from infra_basic.basic_model import VersionedModel


class TagOwnershipModel(VersionedModel):
    """
    标签所属
    """

    tag_id: Optional[str]
    code: Optional[str]
    owner_category: str
    owner_id: str
    is_editable: bool = True
    is_activated: bool = True
