from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.contact_info import ContactInfoEntity
from infra_backbone.model.contact_info_model import ContactInfoModel


class ContactInfoRepository(BasicRepository):
    def insert_contact_info(self, data: ContactInfoModel, transaction: Transaction) -> str:
        """
        插入联系方式
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=ContactInfoEntity, entity_model=data, transaction=transaction
        )

    def fetch_contact_info(self, category: str, detail: str) -> Optional[ContactInfoModel]:
        """
        获取联系方式
        :param category:
        :param detail:
        :return:
        """

        sql = """select * from st_contact_info
        where category = :category and detail  = :detail"""
        return self._fetch_first_to_model(
            model_cls=ContactInfoModel,
            sql=sql,
            params={"category": category, "detail": detail},
        )
