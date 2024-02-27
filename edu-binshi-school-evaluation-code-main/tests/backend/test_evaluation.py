"""
测试评价相关的一些方法
"""
from backend.tasks.tasks import task_save_benchmark_score


def test_refresh_evaluation_criteria_plan_data(prepare_backend_container, prepare_robot):
    uow = prepare_backend_container.uow()
    service = prepare_backend_container.app_evaluation_criteria_plan_service()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_refresh_evaluation_criteria_plan_data")
        service.refresh_evaluation_criteria_plan_data(
            transaction=trans
        )


def test_task_save_benchmark_score(prepare_backend_container, prepare_robot):
    task_save_benchmark_score(
        data={
            "benchmark_id": "367d2b75-7e46-4aae-8b78-3b4eed42e736",
            "evaluation_assignment_id": "48c3bd70-d8be-4cf6-a5f3-f2b48b83e0a2"
        }
    )
