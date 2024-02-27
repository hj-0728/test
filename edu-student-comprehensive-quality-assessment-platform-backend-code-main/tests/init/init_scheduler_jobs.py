from infra_utility.datetime_helper import local_now

from infra_backbone.model.scheduler_job_model import SchedulerJobModel, EnumSchedulerJobTriggerCategory
from infra_backbone.repository.scheduler_job_repository import SchedulerJobRepository


def test_init_scheduler_job(prepare_backbone_container, prepare_robot):
    """
    初始定时任务
    :param prepare_backbone_container:
    :return:
    """
    uow = prepare_backbone_container.uow()
    scheduler_job_repository: SchedulerJobRepository = prepare_backbone_container.scheduler_job_repository()
    with uow:
        transaction = uow.log_transaction(
            handler=prepare_robot,
            action="test_init_scheduler_job"
        )
        job_list = [
            {
                "trigger_category": EnumSchedulerJobTriggerCategory.CRON.name,
                "trigger_expression": "0 4,19,29,34,49 * * * *",
                "started_on": local_now(),
                "ended_on": 'infinity',
                "func_name": "job_sync_context",
                "func_args": {"dingtalk_corp_id": "b51e6648-7947-4969-8c1f-52051ecb5673"}
            },
            {
                "trigger_category": EnumSchedulerJobTriggerCategory.CRON.name,
                "trigger_expression": "0 0,15,25,30,45 * * * *",
                "started_on": local_now(),
                "ended_on": 'infinity',
                "func_name": "job_sync_dingtalk",
                "func_args": {"dingtalk_corp_id": "b51e6648-7947-4969-8c1f-52051ecb5673"}
            }
        ]
        for job in job_list:
            scheduler_job_repository.insert_scheduler_job(
                data=SchedulerJobModel(**job),
                transaction=transaction
            )
