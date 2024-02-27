import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier

from backend.backend_containers import BackendContainer
from backend.data.constant import FlaskConfigConst
from domain_evaluation.model.edit.load_benchmark_schema_args_em import (
    LoadBenchmarkSchemaArgsEditModel,
)
from domain_evaluation.service.benchmark_strategy_service import BenchmarkStrategyService

blueprint_benchmark_strategy = Blueprint(
    name="benchmark-strategy",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/benchmark-strategy"


@blueprint_benchmark_strategy.route(f"{WEB_PREFIX}/list", methods=["GET"])
@inject
def route_get_benchmark_strategy_list(
    benchmark_strategy_service: BenchmarkStrategyService = Provide[
        BackendContainer.domain_evaluation_container.benchmark_strategy_service
    ],
) -> jsonify:
    """
    获取list
    :return:
    """
    carrier = MessageCarrier()
    try:
        benchmark_id = request.args.get("benchmarkId")
        data = benchmark_strategy_service.load_benchmark_strategy_list(benchmark_id=benchmark_id)
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_benchmark_strategy.route(
    f"{WEB_PREFIX}/get-input-params/", methods=["POST"]
)
@inject
def route_get_benchmark_input_params(
    benchmark_strategy_service: BenchmarkStrategyService = Provide[
        BackendContainer.domain_evaluation_container.benchmark_strategy_service
    ],
) -> jsonify:
    """
    获取input_params
    :return:
    """
    carrier = MessageCarrier()
    try:
        input_params = request.get_json(silent=True)
        data = benchmark_strategy_service.load_benchmark_input_schema(
            load_args=LoadBenchmarkSchemaArgsEditModel(**input_params)
        )
        carrier.push_succeed_data(data=data)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
