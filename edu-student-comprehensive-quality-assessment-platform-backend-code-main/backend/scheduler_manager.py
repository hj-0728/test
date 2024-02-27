import logging
from time import sleep
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler
from infra_utility.config_helper import load_to_env
from loguru import logger
from pytz import utc

from backend import scheduler_jobs
from backend.backend_container import BackendContainer
from backend.utility.redis_helper import get_pubsub_message
from infra_backbone.data.constant import SchedulerJobConst
from infra_backbone.model.scheduler_job_model import SchedulerJobModel
from infra_backbone.utility.scheduler_helper import load_scheduler_jobs


class SchedulerManager:
    """
    定时任务执行管理器
    """

    def __init__(self):
        self.__scheduler = BackgroundScheduler(timezone=utc)
        container = BackendContainer()
        container.init_resources()
        self.__container = container
        self.__redis_manager = container.redis_manager()
        self.__scheduler_job_service = container.backbone_container.scheduler_job_service()

    def running(self):
        """
        启动
        """

        self.__scheduler.start()
        self.__refresh()
        listen_sub = self.__redis_manager.redis_client.pubsub()
        db = self.__redis_manager.redis_client.connection_pool.connection_kwargs["db"]
        channel = f"{SchedulerJobConst.CHANNEL_SCHEDULER}&&{str(db)}"
        listen_sub.subscribe(channel)
        while True:
            try:
                command = get_pubsub_message(listen_sub)
                if command and command == SchedulerJobConst.COMMAND_REFRESH:
                    self.__refresh()
            except Exception as err:
                logger.error(str(err))
            sleep(1)

    def __load_jobs_by_jobs_list(self, jobs_list: List[SchedulerJobModel]):
        """

        :param jobs_list:
        :return:
        """
        jobs_config = self.__scheduler_job_service.prepare_enabled_scheduler_jobs(
            jobs_list=jobs_list
        )
        load_scheduler_jobs(self.__scheduler, scheduler_jobs, jobs_config)

    def __batch_remove_job(self, job_id_list: List[str]):
        """
        批量移除任务
        :param job_id_list:
        :return:
        """
        for job_id in job_id_list:
            self.__scheduler.remove_job(job_id)

    def __refresh(self):
        """
        刷新进程任务
        :return:
        """
        processing_scheduler_jobs = self.__scheduler.get_jobs()
        scheduler_jobs_from_db = self.__scheduler_job_service.get_scheduler_jobs_to_be_run()

        processing_jobs_ids = [x.id for x in processing_scheduler_jobs]
        db_jobs_ids = [x.id for x in scheduler_jobs_from_db]

        need_del_jobs_ids = [x for x in processing_jobs_ids if x not in db_jobs_ids]
        self.__batch_remove_job(need_del_jobs_ids)

        need_add_jobs = [x for x in scheduler_jobs_from_db if x.id not in processing_jobs_ids]
        self.__load_jobs_by_jobs_list(need_add_jobs)


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)",
        datefmt="%Y-%m-%d %H:%M:%S",
        level="INFO",
        force=True,
    )
    load_to_env(__file__, "../app.toml")

    scheduler_manager = SchedulerManager()
    scheduler_manager.running()
