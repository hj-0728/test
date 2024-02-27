from typing import List, Optional

from infra_basic.basic_repository import BasicRepository, PageInitParams
from infra_basic.transaction import Transaction

from infra_backbone.entity.site_message import SiteMessageEntity
from infra_backbone.model.params.site_message_query_params import SiteMessageQueryParams
from infra_backbone.model.site_message_context_model import EnumSiteMessageContextResourceCategory
from infra_backbone.model.site_message_model import SiteMessageModel
from infra_backbone.model.view.site_message_vm import SiteMessageVm


class SiteMessageRepository(BasicRepository):
    def insert_site_message(self, data: SiteMessageModel, transaction: Transaction) -> str:
        """
        插入站内信
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=SiteMessageEntity,
            entity_model=data,
            transaction=transaction,
        )

    def update_site_message(
        self,
        data: SiteMessageModel,
        transaction: Transaction,
        col_list: Optional[List[str]] = None,
    ):
        """
        更新站内信
        :param data:
        :param transaction:
        :param col_list:
        :return:
        """

        return self._update_versioned_entity_by_model(
            entity_cls=SiteMessageEntity,
            update_model=data,
            transaction=transaction,
            limited_col_list=col_list,
        )

    def get_received_site_message_lit_page_info(self, query_params: SiteMessageQueryParams):
        """
        获取收到的站内信列表页数据
        """
        sql = """
        select ssm.id, ssm.created_on, ssm.read_on,
        ssm.send_user_id, ssm.receive_user_id,
        ssm.init_resource_category, ssm.init_resource_id,
        ssm.content ->> 'title' as title,
        ssm.content ->> 'content' as content,
        ssm.content ->> 'file_id' as file_id,
        case when ssm.read_on is null then 1
        else 0 end as seq
        from st_site_message ssm
        join st_site_message_context ssmc on ssm.id = ssmc.site_message_id
        where ssm.receive_user_id = :user_id
        and ssmc.resource_id = :role_id and ssmc.resource_category = :ROLE
        """
        if query_params.category:
            sql += """
            AND init_resource_category = ANY(:category)
            """
        if query_params.is_read == "unread":
            sql += " and read_on is null"
        elif query_params.is_read == "read":
            sql += " and read_on is not null"
        sql += " order by seq desc "
        if query_params.order_by == "asc":
            sql += ", created_on"
        elif query_params.order_by == "desc" or not query_params.order_by:
            sql += ", created_on desc"

        page_init_params = PageInitParams(
            sql=sql,
            filter_columns=["title", "content"],
            params={
                "user_id": query_params.user_id,
                "role_id": query_params.role_id,
                "ROLE": EnumSiteMessageContextResourceCategory.ROLE.name,
                "category": query_params.category,
            },
        )
        return self._paginate(
            result_type=SiteMessageVm,
            total_params=page_init_params,
            page_params=query_params,
        )

    def check_user_has_unread_message(
        self,
        user_id: str,
        role_id: str,
    ) -> int:
        """
        检查是否有未读消息
        :param user_id:
        :param role_id:
        :return:
        """
        sql = """
        select distinct ssm.id from st_site_message ssm
        join st_site_message_context ssmc on ssm.id = ssmc.site_message_id
        where ssm.read_on is null and ssm.receive_user_id = :user_id
        and ssmc.resource_id = :role_id and ssmc.resource_category = :ROLE
        """
        return self._fetch_count(
            sql=sql,
            params={
                "user_id": user_id,
                "role_id": role_id,
                "ROLE": EnumSiteMessageContextResourceCategory.ROLE.name,
            },
        )

    def get_site_message_info_by_id(self, site_message_id: str):
        """
        获取站内信信息
        """
        sql = """
        select ssm.id, ssm.created_on, ssm.read_on,ssm.version,
        ssm.send_user_id, ssm.receive_user_id,
        ssm.init_resource_category, ssm.init_resource_id,
        ssm.content -> 'title' as title,
        ssm.content -> 'content' as content,
        ssm.content ->> 'file_id' as file_id
        from st_site_message ssm
        where ssm.id  = :site_message_id
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=SiteMessageVm,
            params={"site_message_id": site_message_id},
        )
