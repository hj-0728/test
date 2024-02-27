from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction

from infra_backbone.model.distributed_task_log_model import (
    DistributedTaskLogModel,
    EnumDistributedTaskLogStatus,
)
from infra_backbone.repository.distributed_task_log_repository import DistributedTaskLogRepository


class DistributedTaskLogService:
    def __init__(self, distributed_task_log_repository: DistributedTaskLogRepository):
        self.__distributed_task_log_repository = distributed_task_log_repository

    def add_distributed_task_log(
        self, log: DistributedTaskLogModel, transaction: Transaction
    ) -> str:
        """
        添加分布式任务日志
        :param log:
        :param transaction:
        :return:
        """
        log.status = EnumDistributedTaskLogStatus.READY.name
        return self.__distributed_task_log_repository.insert_distributed_task_log(
            log=log, transaction=transaction
        )

    def get_distributed_task_log(self, log_id: str) -> DistributedTaskLogModel:
        """
        获取分布式任务日志
        :param log_id:
        :return:
        """
        log = self.__distributed_task_log_repository.fetch_distributed_task_log(log_id=log_id)
        if not log:
            raise BusinessError("分布式任务日志不存在")
        return log

    def update_distributed_task_log(self, log: DistributedTaskLogModel, transaction: Transaction):
        """
        更新分布式任务日志
        :param log:
        :param transaction:
        :return:
        """
        self.__distributed_task_log_repository.update_distribution_task_log(
            log=log, transaction=transaction, limited_col_list=["status", "err_msg", "try_count"]
        )
