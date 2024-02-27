from infra_utility.datetime_helper import local_now

from infra_backbone.model.scheduler_job_model import SchedulerJobModel, EnumSchedulerJobTriggerType
from infra_backbone.repository.scheduler_job_repository import SchedulerJobRepository


def test_add_scheduler_job(prepare_backbone_container, prepare_robot):
    """
    测试添加定时任务
    :param prepare_backbone_container:
    :return:
    """
    uow = prepare_backbone_container.uow()
    scheduler_job_repository: SchedulerJobRepository = prepare_backbone_container.scheduler_job_repository()
    with uow:
        transaction = uow.log_transaction(
            handler=prepare_robot,
            action="test_add_scheduler_job"
        )

        scheduler_job_id = scheduler_job_repository.insert_scheduler_job(
            data=SchedulerJobModel(
                trigger_type=EnumSchedulerJobTriggerType.CRON.name,
                trigger_expression="0 6 * * * *",
                start_at=local_now(),
                finish_at='infinity',
                is_activated=True,
                func_name="job_sync_context",
                func_args=None
            ),
            transaction=transaction
        )

        print(scheduler_job_id)
