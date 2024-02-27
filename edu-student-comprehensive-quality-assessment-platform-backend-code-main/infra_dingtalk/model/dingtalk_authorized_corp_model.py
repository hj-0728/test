"""
授权的组织
"""
from typing import Any, Dict

from infra_basic.basic_model import VersionedModel


class DingTalkAuthorizedCorpModel(VersionedModel):
    """
    授权的组织
    """

    suite_id: str
    auth_corp_id: str
    permanent_code: str
    authorized_data: Dict[str, Any]
