from backend.tasks.tasks import task_handle_distributed_task


def test_task_handle_distributed_task(prepare_app_container):
    task_handle_distributed_task(distributed_task_log_id="450af4c0-0f13-49e0-a50c-25c84c17b49e")
