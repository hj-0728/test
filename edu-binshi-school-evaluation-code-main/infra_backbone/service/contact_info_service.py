from typing import List

from infra_basic.errors.input import DataNotFoundError
from infra_basic.transaction import Transaction

from infra_backbone.model.contact_info_model import (
    ContactInfoCategory,
    ContactInfoModel,
    EnumContactInfoCategory,
)
from infra_backbone.model.resource_contact_info_model import ResourceContactInfoModel
from infra_backbone.repository.contact_info_repository import ContactInfoRepository
from infra_backbone.repository.resource_contact_info_repository import ResourceContactInfoRepository


class ContactInfoService:
    def __init__(
        self,
        contact_info_repository: ContactInfoRepository,
        resource_contact_info_repository: ResourceContactInfoRepository,
    ):
        self.__contact_info_repository = contact_info_repository
        self.__resource_contact_info_repository = resource_contact_info_repository

    def save_resource_contact_info(
        self,
        data: ResourceContactInfoModel,
        transaction: Transaction,
        full_update: bool = True,
    ):
        """
        保存资源的联系方式
        :param data:
        :param transaction:
        :param full_update: 是否全量更新，默认为True，为True的时候保持资源的联系方式最终和传入的一样。
                            为False的话这个资源在数据库但是不在入参中的联系方式会被保留，
                            添加入参中且不在数据库中的
                            这个参数只在更新时有用
        :return:
        """
        if not data.contact_info_list:
            raise DataNotFoundError("未获取到资源联系方式")
        db_resource_contact = self.__resource_contact_info_repository.fetch_resource_contact_info(
            resource_id=data.resource_id, resource_category=data.resource_category
        )
        if not db_resource_contact:
            self.add_resource_contact_info(data=data, transaction=transaction)
        else:
            self.update_resource_contact_info(
                data=data,
                db_resource_contact=db_resource_contact,
                transaction=transaction,
                full_update=full_update,
            )

    def add_resource_contact_info(self, data: ResourceContactInfoModel, transaction: Transaction):
        """
        添加资源的联系方式
        :param data:
        :param transaction:
        :return:
        """
        for contact in data.contact_info_list:
            contact_info_id = self.refresh_contact_info(contact=contact, transaction=transaction)
            exist_resource_contact_info = (
                self.__resource_contact_info_repository.get_exist_resource_contact_info(
                    resource_category=data.resource_category,
                    resource_id=data.resource_id,
                    contact_info_id=contact_info_id,
                )
            )
            if not exist_resource_contact_info:
                self.__resource_contact_info_repository.insert_resource_contact_info(
                    data=data.renew_resource_contact_info(contact_info_id=contact_info_id),
                    transaction=transaction,
                )

    def refresh_contact_info(self, contact: ContactInfoModel, transaction: Transaction) -> str:
        """
        获取联系方式的id
        :param contact: 联系方式
        :param transaction:
        :return:
        """
        db_contact = self.__contact_info_repository.fetch_contact_info(
            category=contact.category, detail=contact.detail
        )
        if db_contact:
            return db_contact.id
        return self.__contact_info_repository.insert_contact_info(
            data=contact, transaction=transaction
        )

    def update_resource_contact_info(
        self,
        data: ResourceContactInfoModel,
        db_resource_contact: ResourceContactInfoModel,
        transaction: Transaction,
        full_update: bool,
    ):
        """
        更新资源的联系方式
        :param db_resource_contact:
        :param data:
        :param transaction:
        :param full_update:
        :return:
        """
        for new_contact in data.contact_info_list:
            if new_contact not in db_resource_contact.contact_info_list:
                contact_info_id = self.refresh_contact_info(
                    contact=new_contact, transaction=transaction
                )
                exist_resource_contact_info = (
                    self.__resource_contact_info_repository.get_exist_resource_contact_info(
                        resource_category=data.resource_category,
                        resource_id=data.resource_id,
                        contact_info_id=contact_info_id,
                    )
                )
                if not exist_resource_contact_info:
                    self.__resource_contact_info_repository.insert_resource_contact_info(
                        data=data.renew_resource_contact_info(contact_info_id=contact_info_id),
                        transaction=transaction,
                    )
        # 只有全量更新的时候才需要删除
        if not full_update:
            return
        for db_contact in db_resource_contact.contact_info_list:
            if db_contact not in data.contact_info_list:
                if not db_contact.resource_contact_info_id:
                    raise DataNotFoundError("未获取到资源联系方式id")
                self.__resource_contact_info_repository.delete_resource_contact_info(
                    resource_contact_info_id=db_contact.resource_contact_info_id,
                    transaction=transaction,
                )

    def get_contact_info_by_resource_id(
        self,
        resource_id: str,
    ):
        """
        获取资源的联系方式
        :param resource_id:
        :return:
        """

        return self.__resource_contact_info_repository.get_contact_info_by_resource_id(
            resource_id=resource_id,
        )

    def delete_resource_contact_info(
        self,
        resource_category: str,
        resource_id: str,
        category_list: List[str],
        transaction: Transaction,
    ):
        """
        删除资源的联系方式
        :param resource_category:
        :param resource_id:
        :param category_list: contact_info category list
        :param transaction:
        :return:
        """

        resource_contact_info_list = (
            self.__resource_contact_info_repository.get_resource_contact_info(
                resource_category=resource_category,
                resource_id=resource_id,
                category_list=category_list,
            )
        )

        for resource_contact_info in resource_contact_info_list:
            self.__resource_contact_info_repository.delete_resource_contact_info(
                resource_contact_info_id=resource_contact_info.id,
                transaction=transaction,
            )

    @staticmethod
    def get_contact_info_category_list() -> List[ContactInfoCategory]:
        """
        获取联系方式类型
        :return:
        """
        category_list = []
        for category in EnumContactInfoCategory:
            category_list.append(ContactInfoCategory(name=category.value, value=category.name))
        return category_list
