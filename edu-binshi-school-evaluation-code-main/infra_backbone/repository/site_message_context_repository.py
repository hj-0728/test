from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.site_message_context import SiteMessageContextEntity
from infra_backbone.model.site_message_context_model import SiteMessageContextModel


class SiteMessageContextRepository(BasicRepository):
    def insert_site_message_context(
        self, data: SiteMessageContextModel, transaction: Transaction
    ) -> str:
        """
        插入站内信上下文
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=SiteMessageContextEntity,
            entity_model=data,
            transaction=transaction,
        )
