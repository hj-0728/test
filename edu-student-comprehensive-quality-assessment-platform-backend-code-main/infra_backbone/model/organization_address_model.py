from infra_basic.basic_model import BasePlusModel


class OrganizationAddressModel(BasePlusModel):
    organization_id: str
    address_id: str
    seq: int
