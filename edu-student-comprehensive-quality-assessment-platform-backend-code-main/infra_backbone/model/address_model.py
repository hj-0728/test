from typing import Optional

from infra_basic.basic_model import VersionedModel
from infra_basic.basic_resource import BasicResource
from infra_basic.errors.input import DataNotFoundError

from infra_backbone.model.address_relationship_model import AddressRelationshipModel


class AddressModel(VersionedModel):
    # Geography属性没加，等用的时候再研究这种类型怎么写
    area_id: str
    detail: str

    link_resource: Optional[BasicResource]

    def prepare_address_relationship(self) -> AddressRelationshipModel:
        """
        准备地址资源关联
        :return:
        """
        if not self.link_resource:
            raise DataNotFoundError("未获取到关联的资源")
        return AddressRelationshipModel(
            address_id=self.id,
            resource_id=self.link_resource.res_id,
            resource_category=self.link_resource.res_category,
        )
