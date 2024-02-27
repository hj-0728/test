from enum import Enum
from typing import List, Optional

from infra_basic.basic_model import BasePlusModel

from infra_backbone.model.contact_info_model import ContactInfoModel


class ResourceContactInfoModel(BasePlusModel):
    id: Optional[str]
    resource_category: str
    resource_id: str
    contact_info_id: Optional[str]

    contact_info_list: List[ContactInfoModel] = []

    def renew_resource_contact_info(self, contact_info_id: str) -> "ResourceContactInfoModel":
        """
        重新生成一个资源的联系方式
        :param contact_info_id:
        :return:
        """
        return ResourceContactInfoModel(
            resource_category=self.resource_category,
            resource_id=self.resource_id,
            contact_info_id=contact_info_id,
        )


class EnumContactInfoResourceCategory(Enum):
    PEOPLE = "人"
