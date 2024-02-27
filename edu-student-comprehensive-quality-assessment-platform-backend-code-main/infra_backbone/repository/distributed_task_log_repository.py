from typing import Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.distributed_task_log import DistributedTaskLogEntity
from infra_backbone.model.distributed_task_log_model import DistributedTaskLogModel


class DistributedTaskLogRepository(BasicRepository):
    def insert_distributed_task_log(
        self, log: DistributedTaskLogModel, transaction: Transaction
    ) -> str:
        """
        添加分布式任务日志
        :param log:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=DistributedTaskLogEntity,
            entity_model=log,
            transaction=transaction,
        )

    def fetch_distributed_task_log(self, log_id: str) -> Optional[DistributedTaskLogModel]:
        """
        获取分布式任务日志
        :param log_id:
        :return:
        """
        sql = """select * from st_distributed_task_log where id = :log_id"""
        return self._fetch_first_to_model(
            sql=sql, model_cls=DistributedTaskLogModel, params={"log_id": log_id}
        )

    def update_distribution_task_log(
        self,
        log: DistributedTaskLogModel,
        transaction: Transaction,
        limited_col_list: Optional[list] = None,
    ):
        """
        更新分布式任务日志
        :param log:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        self._update_versioned_entity_by_model(
            entity_cls=DistributedTaskLogEntity,
            update_model=log,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )
