"""
钉钉组织
"""

from infra_basic.basic_model import VersionedModel


class DingtalkCorpModel(VersionedModel):
    remote_corp_id: str
    name: str
