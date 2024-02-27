from typing import List

from infra_backbone.data.scheduler_jobs_config import (
    SchedulerJobsConfig,
    SchedulerJobsConfigForCron,
    SchedulerJobsConfigForInterval,
)
from infra_backbone.model.scheduler_job_model import EnumSchedulerJobTriggerType, SchedulerJobModel
from infra_backbone.repository.scheduler_job_repository import SchedulerJobRepository
from infra_backbone.utility.scheduler_helper import parse_cron_setting, parse_interval_setting


class SchedulerJobsService:
    def __init__(
        self,
        scheduler_job_repository: SchedulerJobRepository,
    ):
        self.__scheduler_job_repository = scheduler_job_repository

    def get_scheduler_jobs_to_be_run(self) -> List[SchedulerJobModel]:
        """
        获取待运行的排程任务
        :return:
        """
        return self.__scheduler_job_repository.get_scheduler_job_to_be_run()

    @staticmethod
    def prepare_enabled_scheduler_jobs(
        jobs_list: List[SchedulerJobModel],
    ) -> List[SchedulerJobsConfig]:
        """
        准备启用的定时任务
        :param jobs_list
        :return:
        """
        result = []

        for job_info in jobs_list:
            job_config = {
                "id": job_info.id,
                "func_name": job_info.func_name,
                "trigger_type": job_info.trigger_type,
                "func_args": job_info.func_args,
                "start_date": job_info.start_at,
                "end_date": job_info.finish_at,
            }
            job_config_obj = None
            if job_info.trigger_type == EnumSchedulerJobTriggerType.INTERVAL.name:
                interval_config = parse_interval_setting(job_info.trigger_expression)
                job_config |= interval_config
                job_config_obj = SchedulerJobsConfigForInterval(job_config)
            if job_info.trigger_type == EnumSchedulerJobTriggerType.CRON.name:
                cron_config = parse_cron_setting(job_info.trigger_expression)
                job_config |= cron_config
                job_config_obj = SchedulerJobsConfigForCron(job_config)
            if job_config_obj:
                job_config_obj.start_date = job_info.start_at
                job_config_obj.end_date = job_info.finish_at
                result.append(job_config_obj)

        return result
