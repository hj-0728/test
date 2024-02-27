from typing import Optional

from infra_basic.basic_model import VersionedModel


class TagInfoModel(VersionedModel):
    name: str
    tag_ownership_id: Optional[str]
    tag_ownership_relationship_id: Optional[str]
