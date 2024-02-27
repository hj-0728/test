from typing import List

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.scheduler_job import SchedulerJobEntity
from infra_backbone.model.scheduler_job_model import SchedulerJobModel


class SchedulerJobRepository(BasicRepository):
    def insert_scheduler_job(self, data: SchedulerJobModel, transaction: Transaction) -> str:
        """
        插入定时任务
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=SchedulerJobEntity, entity_model=data, transaction=transaction
        )

    def get_scheduler_job_to_be_run(self) -> List[SchedulerJobModel]:
        """
        获取所有待运行的排程任务
        :return:
        """
        sql = """
        select  * from  st_scheduler_job
        where start_at <= now() and ((finish_at is null)
        or (finish_at is not null and finish_at>=now()))
        and is_activated is true
        """
        return self._fetch_all_to_model(
            model_cls=SchedulerJobModel,
            sql=sql,
        )
