"""
服务商跟组织的map关系
"""

from infra_basic.basic_model import VersionedModel


class ServiceProviderModel(VersionedModel):
    """
    服务商
    """

    wechat_corp_id: str
    provider_secret: str
    code: str
    name: str
