import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier
from infra_basic.uow_interface import UnitOfWork

from backend.backend_container import BackendContainer
from backend.blueprint import get_current_handler, get_current_people_id
from backend.data.constant import BusinessConst, FlaskConfigConst
from biz_comprehensive.repository.search_history_repository import SearchHistoryRepository
from biz_comprehensive.service.search_history_service import SearchHistoryService

blueprint_search_history = Blueprint(
    name="search_history", import_name=__name__, url_prefix=f"{FlaskConfigConst.API_PREFIX}"
)

MOBILE_PREFIX = "/mobile/search-history"


@blueprint_search_history.route(f"{MOBILE_PREFIX}/get-owner-search-history-list", methods=["POST"])
@inject
def route_get_search_history_list(
    search_history_repository: SearchHistoryRepository = Provide[
        BackendContainer.comprehensive_container.search_history_repository
    ],
):
    """
    获取搜索历史
    """
    carrier = MessageCarrier()
    try:
        search_scene = request.get_json().get("searchScene")
        if not search_scene:
            raise BusinessError("搜索场景不能为空")
        scene_list = search_history_repository.fetch_people_search_history_list(
            people_id=get_current_people_id(),
            search_scene=search_scene,
            limit_count=BusinessConst.SEARCH_HISTORY_LIMIT_COUNT,
        )
        carrier.push_succeed_data(data=scene_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))


@blueprint_search_history.route(f"{MOBILE_PREFIX}/clear", methods=["POST"])
@inject
def route_clear_search_history_list(
    search_history_search: SearchHistoryService = Provide[
        BackendContainer.comprehensive_container.search_history_service
    ],
    uow: UnitOfWork = Provide[BackendContainer.uow],
):
    """
    清空搜索历史
    """
    carrier = MessageCarrier()
    try:
        search_scene = request.get_json().get("searchScene")
        if not search_scene:
            raise BusinessError("搜索场景不能为空")
        people_id = get_current_people_id()
        transaction = uow.log_transaction(
            handler=get_current_handler(),
            action="clear_search_history",
            action_params={"search_scene": search_scene, "people_id": people_id},
        )
        with uow:
            scene_list = search_history_search.clear_search_history(
                search_scene=search_scene, people_id=people_id, transaction=transaction
            )
        carrier.push_succeed_data(data=scene_list)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err)
    return jsonify(carrier.dict(by_alias=True))
