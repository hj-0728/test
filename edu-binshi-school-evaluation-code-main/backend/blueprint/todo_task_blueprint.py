import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_user_id, get_current_handler, \
    get_current_period_id
from backend.data.constant import FlaskConfigConst
from domain_evaluation.data.query_params.todo_task_query_params import TodoTaskQueryParams
from domain_evaluation.model.edit.complete_todo_task_em import CompleteTodoTaskEditModel
from domain_evaluation.service.todo_task_service import TodoTaskService

blueprint_todo_task = Blueprint(
    name="todo-task",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/todo-task"


@blueprint_todo_task.route(f"{WEB_PREFIX}/page", methods=["POST"])
@inject
def route_get_todo_task_page(
    todo_task_service: TodoTaskService = Provide[
        BackendContainer.domain_evaluation_container.todo_task_service
    ],
):
    """
    获取待办事项
    :param todo_task_service:
    :return:
    """

    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        params = TodoTaskQueryParams(**data)
        params.period_id = get_current_period_id()
        result = todo_task_service.fetch_todo_task_page(
            params=params,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_todo_task.route(f"{WEB_PREFIX}/complete", methods=["POST"])
@inject
def route_complete_todo_task(
    uow: UnitOfWork = Provide[BackendContainer.uow],
    todo_task_service: TodoTaskService = Provide[
        BackendContainer.domain_evaluation_container.todo_task_service
    ],
):
    """
    完成待办事项
    :param uow:
    :param todo_task_service:
    :return:
    """

    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="complete_todo_task",
                action_params={"data": data},
            )
            todo_task_data = CompleteTodoTaskEditModel(**data)
            todo_task_data.completed_by = get_current_user_id()
            todo_task_service.complete_todo_task(
                todo_task_data=todo_task_data,
                transaction=transaction
            )
        carrier.push_succeed_data(data=True)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))

