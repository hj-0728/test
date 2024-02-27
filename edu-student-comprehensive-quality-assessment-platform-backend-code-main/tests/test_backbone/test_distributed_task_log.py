from infra_backbone.model.distributed_task_log_model import DistributedTaskLogModel


def test_add_distributed_task_log(prepare_backbone_container, prepare_handler):
    uow = prepare_backbone_container.uow()
    service = prepare_backbone_container.distributed_task_log_service()
    with uow:
        log = DistributedTaskLogModel(
            task_func="task_revoke_observation_point",
        )
        transaction = uow.log_transaction(
            handler=prepare_handler,
            action_params=log,
            action="test_add_distributed_task_log"
        )
        service.add_distributed_task_log(log=log, transaction=transaction)

