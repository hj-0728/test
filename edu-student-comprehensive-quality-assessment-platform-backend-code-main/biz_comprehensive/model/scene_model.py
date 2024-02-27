from typing import Optional

from infra_basic.basic_model import VersionedModel


class SceneModel(VersionedModel):
    """
    场景
    """

    name: str
    code: Optional[str]
