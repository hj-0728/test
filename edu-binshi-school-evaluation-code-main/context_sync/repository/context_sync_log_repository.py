"""
上下文同步日志 repository
"""

from infra_basic.basic_repository import BasicRepository

from context_sync.entity.context_sync_log import ContextSyncLogEntity
from context_sync.model.context_sync_log_model import ContextSyncLogModel


class ContextSyncLogRepository(BasicRepository):
    """
    上下文同步日志 repository
    """

    def insert_context_sync_log(
        self,
        context_sync_log: ContextSyncLogModel,
    ) -> str:
        """
        添加上下文同步日志
        """
        return self._insert_basic_entity_by_model(
            entity_cls=ContextSyncLogEntity,
            insert_model=context_sync_log,
        )
