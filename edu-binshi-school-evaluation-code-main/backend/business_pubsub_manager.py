"""
业务pubsub管理器
"""
import json
import traceback

from infra_pub_sub_manager.settings import PubSubSettings
from infra_pub_sub_manager.sync_sub_manager import SyncSubManager
from infra_utility.config_helper import load_to_env
from loguru import logger

from backend.backend_containers import BackendContainer
from backend.tasks.tasks import (
    task_get_dimension_dept_tree_report,
    task_handle_generate_input_score_log,
    task_regenerate_score_log,
    task_save_access_log,
    task_save_benchmark_score,
    task_refresh_evaluation_criteria_plan_data,
    task_save_evaluation_assignment_relationship,
    task_disable_unavailable_user, task_sync_k12_teacher_subject,
)


class BusinessPubsubManager(SyncSubManager):
    """
    业务pubsub管理器
    """

    def __init__(self, settings: PubSubSettings = None):
        """
        初始化
        """
        super().__init__(settings=settings)

        logger.info("start init container")
        container = BackendContainer()
        container.init_resources()


def process_command(command: str):
    """
    根据command执行那个方法
    """
    command = json.loads(command)
    logger.info(f"start process command: { command['category']}")
    process_map = {
        "task_save_access_log": task_save_access_log,
        "task_save_benchmark_score": task_save_benchmark_score,
        "task_regenerate_score_log": task_regenerate_score_log,
        "task_handle_generate_input_score_log": task_handle_generate_input_score_log,
        "task_get_dimension_dept_tree_report": task_get_dimension_dept_tree_report,
        "task_refresh_evaluation_criteria_plan_data": task_refresh_evaluation_criteria_plan_data,
        "task_save_evaluation_assignment_relationship": task_save_evaluation_assignment_relationship,
        "task_disable_unavailable_user": task_disable_unavailable_user,
        "task_sync_k12_teacher_subject": task_sync_k12_teacher_subject,
    }
    try:
        process_map[command["category"]](command["args"])
    except Exception as err:
        logger.error(f"process_map command [{command}] failed: {err}")
        traceback.print_exc()
    logger.info(f"finish process_command: { command['category']}")


def run_pubsub_manager():
    load_to_env(__file__, "../app.toml")
    sub_manager = BusinessPubsubManager()
    sub_manager.setup_consume_func(consume_func=process_command)
    sub_manager.running()


if __name__ == "__main__":
    run_pubsub_manager()
