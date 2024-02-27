import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork
from infra_pub_sub_manager.sync_pub_client import SyncPubClient
from infra_utility.serialize_helper import ORJSONPickle

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_handler
from backend.data.constant import FlaskConfigConst
from backend.model.edit.command_em import CommandEm
from backend.model.edit.command_update_benchmark_em import CommandUpdateBenchmarkEditModel
from domain_evaluation.model.edit.save_benchmark_em import SaveBenchmarkEditModel
from domain_evaluation.service.benchmark_service import BenchmarkService

blueprint_benchmark = Blueprint(
    name="benchmark",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/benchmark"


@blueprint_benchmark.route(
    f"{WEB_PREFIX}/get-list-by-indicator-id/<string:indicator_id>/<string:input_score_symbol_id>",
    methods=["GET"],
)
@inject
def route_get_benchmark_list_by_indicator_id(
    indicator_id: str,
    input_score_symbol_id: str,
    benchmark_service: BenchmarkService = Provide[
        BackendContainer.domain_evaluation_container.benchmark_service
    ],
) -> jsonify:
    """
    获取benchmark list
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = benchmark_service.get_benchmark_list_by_indicator_id(
            indicator_id=indicator_id,
            input_score_symbol_id=input_score_symbol_id,
        )
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_benchmark.route(f"{WEB_PREFIX}/save-benchmark", methods=["POST"])
@inject
def route_save_benchmark(
    benchmark_service: BenchmarkService = Provide[
        BackendContainer.domain_evaluation_container.benchmark_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
    pub_client: SyncPubClient = Provide[BackendContainer.pub_client],
):
    """
    保存基准
    :param uow:
    :param benchmark_service:
    :param pub_client:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            params = data["benchmark"]["benchmarkStrategyParams"]
            if not params.get("numericMinScore"):
                params["numericMinScore"] = 0
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="save_benchmark",
                action_params={"data": data},
            )
            benchmark_id = benchmark_service.save_benchmark(
                data=SaveBenchmarkEditModel(**data),
                transaction=transaction,
            )
        command_args = CommandUpdateBenchmarkEditModel(benchmark_id=benchmark_id)
        command = CommandEm(category="task_regenerate_score_log", args=command_args)
        pub_client.send_message(message=ORJSONPickle.encode_model(command))
        carrier.push_succeed_data(data=benchmark_id)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_benchmark.route(
    f"{WEB_PREFIX}/detail/<string:benchmark_id>", methods=["GET"]
)
@inject
def route_get_benchmark_detail(
    benchmark_id: str,
    benchmark_service: BenchmarkService = Provide[
        BackendContainer.domain_evaluation_container.benchmark_service
    ],
):
    """
    获取benchmark基础信息
    :param benchmark_id:
    :param benchmark_service:
    """
    carrier = MessageCarrier()
    try:
        result = benchmark_service.get_benchmark_detail(
            benchmark_id=benchmark_id,
        )
        carrier.push_succeed_data(data=result)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_benchmark.route(f"{WEB_PREFIX}/delete", methods=["POST"])
@inject
def route_delete_benchmark(
    benchmark_service: BenchmarkService = Provide[
        BackendContainer.domain_evaluation_container.benchmark_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    删除基准
    :param uow:
    :param benchmark_service:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        with uow:
            transaction = uow.log_transaction(
                handler=get_current_handler(),
                action="delete_benchmark",
                action_params={"data": data},
            )
            benchmark_service.finish_single_benchmark(
                benchmark_id=data.get('benchmarkId'),
                benchmark_version=data.get('benchmarkVersion'),
                transaction=transaction,
            )
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))