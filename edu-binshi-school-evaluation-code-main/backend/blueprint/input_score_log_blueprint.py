import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork
from infra_pub_sub_manager.sync_pub_client import SyncPubClient
from infra_utility.serialize_helper import ORJSONPickle

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_people_id, get_current_handler
from backend.data.constant import FlaskConfigConst
from backend.model.edit.command_em import CommandEm
from backend.model.edit.save_benchmark_score_em import SaveBenchmarkScoreEm
from backend.service.app_input_score_log_service import AppInputScoreLogService
from domain_evaluation.model.edit.input_score_log_em import InputScoreLogEditModel

blueprint_input_score_log = Blueprint(
    name="input-score-log",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/input-score-log"


@blueprint_input_score_log.route(f"{WEB_PREFIX}/update", methods=["POST"])
@inject
def route_update_input_score_log(
    app_input_score_log_service: AppInputScoreLogService = Provide[
        BackendContainer.app_input_score_log_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    pub_client: SyncPubClient = Provide[BackendContainer.pub_client],
):
    """
    保存输入分数的日志
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="update_input_score_log",
            action_params=data,
        )
        with uow:
            input_score_log_em = InputScoreLogEditModel(**data)
            input_score_log_em.people_id = get_current_people_id()
            result = app_input_score_log_service.update_input_score_log(
                input_score_log_em=input_score_log_em, transaction=transaction
            )
        command = CommandEm(category="task_save_benchmark_score", args=result)
        pub_client.send_message(message=ORJSONPickle.encode_model(command))
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
