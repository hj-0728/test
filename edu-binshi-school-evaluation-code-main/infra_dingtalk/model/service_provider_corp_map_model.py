"""
服务商跟组织的map关系
"""

from infra_basic.basic_model import VersionedModel


class ServiceProviderCorpMapModel(VersionedModel):
    """
    服务商跟组织的map关系
    """

    service_provider_corp_id: str
    wechat_corp_id: str
    wechat_corp_id_ciphertext: str
