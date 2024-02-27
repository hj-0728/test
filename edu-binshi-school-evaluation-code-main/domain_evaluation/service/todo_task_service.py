from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now

from domain_evaluation.data.query_params.todo_task_query_params import TodoTaskQueryParams
from domain_evaluation.model.edit.complete_todo_task_em import CompleteTodoTaskEditModel
from domain_evaluation.model.edit.save_todo_task_em import SaveTodoTaskEditModel
from domain_evaluation.model.todo_task_model import TodoTaskModel
from domain_evaluation.model.view.todo_task_page_vm import TodoTaskPageViewModel
from domain_evaluation.repository.evaluation_criteria_plan_repository import (
    EvaluationCriteriaPlanRepository,
)
from domain_evaluation.repository.todo_task_repository import TodoTaskRepository
from infra_backbone.model.role_model import EnumRoleCode
from infra_backbone.model.site_message_context_model import (
    EnumSiteMessageContextRelationship,
    EnumSiteMessageContextResourceCategory,
)
from infra_backbone.model.site_message_model import (
    EnumSiteMessageInitResourceCategory,
    SiteMessageModel,
)
from infra_backbone.repository.user_repository import UserRepository
from infra_backbone.service.site_message_service import SiteMessageService


class TodoTaskService:
    """
    待办事项 service
    """

    def __init__(
        self,
        todo_task_repository: TodoTaskRepository,
        site_message_service: SiteMessageService,
        evaluation_criteria_plan_repository: EvaluationCriteriaPlanRepository,
        user_repository: UserRepository,
    ):
        self.__todo_task_repository = todo_task_repository
        self.__site_message_service = site_message_service
        self.__user_repository = user_repository
        self.__evaluation_criteria_plan_repository = evaluation_criteria_plan_repository

    def fetch_todo_task_page(
        self, params: TodoTaskQueryParams
    ) -> PaginationCarrier[TodoTaskPageViewModel]:
        """
        获取待办事项列表
        :param params:
        :return:
        """

        return self.__todo_task_repository.fetch_todo_task_page(params=params)

    def save_todo_task(
        self, plan_id: str, todo_task: SaveTodoTaskEditModel, transaction: Transaction
    ):
        """
        保存待办事项
        """
        todo_task.make_title_beautiful()
        existed_task = self.__todo_task_repository.fetch_existed_todo_task(params=todo_task)
        count = 0
        for title in todo_task.title_list:
            if title in existed_task:
                continue
            self.__todo_task_repository.insert_todo_task(
                todo_task=todo_task.cast_to(cast_type=TodoTaskModel, title=title),
                transaction=transaction,
            )
            count += 1
        self.save_todo_task_remind_site_message(
            plan_id=plan_id,
            todo_task_count=count,
            role_id=todo_task.assign_id,
            transaction=transaction,
        )

    def save_todo_task_remind_site_message(
        self, plan_id: str, todo_task_count: int, role_id: str, transaction: Transaction
    ):
        """
        添加一条站内信，提醒用户新增了几条待办事项
        """
        if todo_task_count <= 0:
            return
        admin_list = self.__user_repository.fetch_user_list_by_role_code(
            role_code=EnumRoleCode.ADMIN.name
        )
        plan_info = self.__evaluation_criteria_plan_repository.fetch_evaluation_criteria_plan_by_id(
            evaluation_criteria_plan_id=plan_id
        )
        for admin in admin_list:
            data = {
                "receive_user_id": admin.id,
                "send_user_id": admin.id,
                "init_resource_category": EnumSiteMessageInitResourceCategory.TODO_TASK.name,
                "init_resource_id": "",
                "created_at": local_now(),
                "content": {
                    "title": "新增待办事项",
                    "content": f"由于“{plan_info.name}”评价计划新增【{todo_task_count}】条待办事项，请前往首页查看详情。",
                },
                "site_message_context_list": [
                    {
                        "relationship": EnumSiteMessageContextRelationship.UNKNOWN.name,
                        "resource_category": EnumSiteMessageContextResourceCategory.ROLE.name,
                        "resource_id": role_id,
                    }
                ],
            }
            site_message = SiteMessageModel(**data)
            self.__site_message_service.add_site_message(
                site_message=site_message, transaction=transaction
            )

    def complete_todo_task(
        self, todo_task_data: CompleteTodoTaskEditModel, transaction: Transaction
    ):
        """
        完成待办事项
        :param todo_task_data:
        :param transaction:
        :return:
        """

        self.__todo_task_repository.update_todo_task(
            todo_task=todo_task_data.cast_to(TodoTaskModel),
            transaction=transaction,
            limited_col_list=["completed_by", "completed_at"],
        )
