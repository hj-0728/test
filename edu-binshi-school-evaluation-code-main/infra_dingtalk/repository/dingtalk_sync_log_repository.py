"""
钉钉同步日志
"""

from infra_basic.basic_repository import BasicRepository

from infra_dingtalk.entity.dingtalk_sync_log import DingtalkSyncLogEntity
from infra_dingtalk.model.dingtalk_sync_log_model import DingtalkSyncLogModel


class DingtalkSyncLogRepository(BasicRepository):
    """
    钉钉同步日志
    """

    def insert_dingtalk_sync_log(self, data: DingtalkSyncLogModel):
        """
        插入同步日志
        """
        self._insert_basic_entity_by_model(entity_cls=DingtalkSyncLogEntity, insert_model=data)
