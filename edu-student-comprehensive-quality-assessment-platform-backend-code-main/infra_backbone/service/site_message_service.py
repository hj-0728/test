from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now
from infra_utility.enum_helper import get_enum_value_by_name

from infra_backbone.model.params.site_message_query_params import SiteMessageQueryParams
from infra_backbone.model.site_message_model import (
    EnumSiteMessageInitResourceCategory,
    SiteMessageModel,
)
from infra_backbone.repository.site_message_context_repository import SiteMessageContextRepository
from infra_backbone.repository.site_message_repository import SiteMessageRepository


class SiteMessageService:
    def __init__(
        self,
        site_message_repository: SiteMessageRepository,
        site_message_context_repository: SiteMessageContextRepository,
    ):
        self.__site_message_repository = site_message_repository
        self.__site_message_context_repository = site_message_context_repository

    def add_site_message(self, site_message: SiteMessageModel, transaction: Transaction) -> str:
        """
        添加站内信
        """
        site_message_id = self.__site_message_repository.insert_site_message(
            data=site_message,
            transaction=transaction,
        )
        for site_message_context in site_message.site_message_context_list:
            site_message_context.site_message_id = site_message_id
            self.__site_message_context_repository.insert_site_message_context(
                data=site_message_context,
                transaction=transaction,
            )
        return site_message_id

    def get_site_message_list_page_info(self, query_params: SiteMessageQueryParams):
        """
        获取站内信列表页数据
        """
        result = self.__site_message_repository.get_received_site_message_lit_page_info(
            query_params=query_params
        )
        for message_info in result.data:
            message_info.init_resource_category_name = get_enum_value_by_name(
                enum_class=EnumSiteMessageInitResourceCategory,
                enum_name=message_info.init_resource_category,
            )
        return result

    def check_has_unread_message(self, user_id: str, role_id: str):
        """
        获取未读消息数目
        """
        return self.__site_message_repository.check_user_has_unread_message(
            user_id=user_id,
            role_id=role_id,
        )

    def get_site_message_info(self, site_message_id: str, transaction: Transaction):
        """
        获取站内信信息
        """
        site_message_info = self.__site_message_repository.get_site_message_info_by_id(
            site_message_id=site_message_id
        )
        if not site_message_info:
            raise BusinessError("未获取到消息详情")
        site_message_info.init_resource_category_name = get_enum_value_by_name(
            enum_class=EnumSiteMessageInitResourceCategory,
            enum_name=site_message_info.init_resource_category,
        )
        if not site_message_info.read_on:
            site_message_info.read_on = local_now()
            self.__site_message_repository.update_site_message(
                data=site_message_info,
                transaction=transaction,
                col_list=["read_on"],
            )
        return site_message_info

    def read_site_message(self, site_message_id: str, transaction: Transaction):
        """
        阅读消息信息
        """
        site_message_info = self.__site_message_repository.get_site_message_info_by_id(
            site_message_id=site_message_id
        )
        if not site_message_info:
            raise BusinessError("未获取到消息详情")
        if not site_message_info.read_on:
            site_message_info.read_on = local_now()
            self.__site_message_repository.update_site_message(
                data=site_message_info,
                transaction=transaction,
                col_list=["read_on"],
            )
