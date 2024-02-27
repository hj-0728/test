import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.message_carrier import MessageCarrier
from infra_basic.query_params import PageFilterParams

from backend.backend_containers import BackendContainer
from backend.data.constant import FlaskConfigConst
from edu_binshi.service.people_service import PeopleService

blueprint_people = Blueprint(
    name="people",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/people"


@blueprint_people.route(f"{WEB_PREFIX}/bind-user-page", methods=["POST"])
@inject
def route_get_people_page(
    people_service: PeopleService = Provide[
        BackendContainer.edu_evaluation_container.people_service
    ],
):
    """

    :param people_service:
    :return:
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        result = people_service.get_can_bind_user_people_page(
            params=PageFilterParams(**data),
        )
        carrier.push_succeed_data(data=result)
    except Exception as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
