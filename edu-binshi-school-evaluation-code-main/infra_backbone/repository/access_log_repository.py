from infra_basic.basic_repository import BasicRepository

from infra_backbone.entity.access_log import AccessLogEntity
from infra_backbone.model.access_log_model import AccessLogModel


class AccessLogRepository(BasicRepository):
    def insert_access_log(self, data: AccessLogModel) -> str:
        """
        插入访问日志
        :param data:
        :return:
        """
        return self._insert_basic_entity_by_model(entity_cls=AccessLogEntity, insert_model=data)
