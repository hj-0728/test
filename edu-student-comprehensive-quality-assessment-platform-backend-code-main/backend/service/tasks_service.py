import inspect
from typing import List

from infra_basic.basic_resource import BasicResource
from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction

from biz_comprehensive.service.calc_resource_service import CalcResourceService
from biz_comprehensive.service.calc_service import CalcService
from biz_comprehensive.service.points_log_service import PointsLogService
from biz_comprehensive.service.snapshot_service import SnapshotService
from infra_backbone.model.distributed_task_log_model import (
    DistributedTaskLogModel,
    EnumDistributedTaskLogSourceResCategory,
)
from infra_backbone.service.distributed_task_log_service import DistributedTaskLogService


class TasksService:
    def __init__(
        self,
        calc_service: CalcService,
        calc_resource_service: CalcResourceService,
        distributed_task_log_service: DistributedTaskLogService,
        snapshot_service: SnapshotService,
        points_log_service: PointsLogService,
    ):
        self.__calc_service = calc_service
        self.__calc_resource_service = calc_resource_service
        self.__distributed_task_log_service = distributed_task_log_service
        self.__snapshot_service = snapshot_service
        self.__points_log_service = points_log_service

    def execute_task(self, distributed_task_log: DistributedTaskLogModel, transaction: Transaction):
        """
        执行任务
        :param distributed_task_log:
        :param transaction:
        :return:
        """
        task_func = getattr(self, distributed_task_log.task_func)
        if not task_func:
            raise BusinessError("任务函数不存在")
        params = inspect.signature(task_func).parameters.keys()
        task_log_dict = distributed_task_log.dict()
        args = {key: task_log_dict.get(key) for key in params}
        if "transaction" in params:
            args["transaction"] = transaction
        return task_func(**args)

    def task_revoke_points(
        self, source_res_category: str, source_res_id: str, transaction: Transaction
    ):
        """
        撤销积分，暂时先只撤销影响到的 points log，不考虑对应 points log 影响到的其他因素
        :return:
        """

        self.__points_log_service.revoke_points(
            cause_res_category=source_res_category,
            cause_res_id=source_res_id,
            transaction=transaction,
        )

    def task_save_calc(
        self, source_res_category: str, source_res_id: str, transaction: Transaction
    ) -> List[str]:
        """
        保存计算结果
        :param source_res_category:
        :param source_res_id:
        :param transaction:
        :return:
        """

        resource_data = self.__calc_resource_service.get_calc_resource_data_by_source_res(
            source_res_category=source_res_category,
            source_res_id=source_res_id,
        )

        if not resource_data:
            return []

        log_result_list = self.__calc_service.calc_and_save_all_result(
            resource_data=resource_data, transaction=transaction
        )
        log_ids = self.prepare_after_task_save_calc_task_log(
            log_result_list=log_result_list,
            source_res_category=source_res_category,
            source_res_id=source_res_id,
            transaction=transaction,
        )
        return log_ids

    def prepare_after_task_save_calc_task_log(
        self,
        log_result_list: List[BasicResource],
        source_res_category: str,
        source_res_id: str,
        transaction: Transaction,
    ) -> List[str]:
        """
        准备保存计算结果后的任务日志
        :return:
        """
        log_ids = []
        for log_result in log_result_list:
            log = {
                "source_res_category": log_result.res_category,
                "source_res_id": log_result.res_id,
                "task_func": "task_save_calc",
            }
            log_id = self.__distributed_task_log_service.add_distributed_task_log(
                log=DistributedTaskLogModel(**log), transaction=transaction
            )
            log_ids.append(log_id)

        if (
            source_res_category
            == EnumDistributedTaskLogSourceResCategory.OBSERVATION_POINT_LOG.name
        ):
            log = {
                "source_res_category": source_res_category,
                "source_res_id": source_res_id,
                "task_func": "task_add_snapshot",
            }
            log_id = self.__distributed_task_log_service.add_distributed_task_log(
                log=DistributedTaskLogModel(**log), transaction=transaction
            )
            log_ids.append(log_id)
        return log_ids

    def task_add_snapshot(
        self, source_res_category: str, source_res_id: str, transaction: Transaction
    ):
        """
        添加快照
        :param source_res_id:
        :param source_res_category:
        :param transaction:
        :return:
        """
        self.__snapshot_service.add_snapshot(
            source_res_category=source_res_category,
            source_res_id=source_res_id,
            transaction=transaction,
        )

    def task_delete_snapshot(
        self, source_res_category: str, source_res_id: str, transaction: Transaction
    ):
        """
        删除快照
        :param source_res_category:
        :param source_res_id:
        :param transaction:
        :return:
        """
        self.__snapshot_service.delete_snapshot(
            source_res_category=source_res_category,
            source_res_id=source_res_id,
            transaction=transaction,
        )
