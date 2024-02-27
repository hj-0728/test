from typing import Optional

from infra_basic.basic_model import VersionedModel


class AreaModel(VersionedModel):
    parent_id: Optional[str]
    name: str
    zoning_code: str
