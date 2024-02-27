from infra_basic.basic_model import VersionedModel


class OrganizationUserMapModel(VersionedModel):
    """
    组织用户信息
    """

    user_id: str
    organization_id: str
