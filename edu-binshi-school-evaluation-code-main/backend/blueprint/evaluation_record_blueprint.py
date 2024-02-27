import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_people_id
from backend.data.constant import FlaskConfigConst
from domain_evaluation.model.edit.evaluation_record_em import EvaluationRecordEditModel
from domain_evaluation.service.evaluation_record_service import EvaluationRecordService

blueprint_evaluation_record = Blueprint(
    name="evaluation-record",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/evaluation-record"


@blueprint_evaluation_record.route(f"{WEB_PREFIX}/tree", methods=["POST"])
@inject
def route_get_evaluation_record_tree(
    evaluation_record_service: EvaluationRecordService = Provide[
        BackendContainer.domain_evaluation_container.evaluation_record_service
    ],
):
    """
    获取评价记录树
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        evaluation_record_em = EvaluationRecordEditModel(**data)
        evaluation_record_em.people_id = get_current_people_id()
        result = evaluation_record_service.get_evaluation_record_tree(
            evaluation_record_em=evaluation_record_em,
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
