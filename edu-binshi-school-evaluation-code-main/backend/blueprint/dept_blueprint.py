import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier

from backend.backend_containers import BackendContainer
from backend.blueprint import get_current_user_id
from backend.data.constant import FlaskConfigConst
from infra_backbone.data.params.dept_tree_query_params import DeptTreeQueryParams
from infra_backbone.service.dept_service import DeptService

blueprint_dept = Blueprint(
    name="dept",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/dept"


@blueprint_dept.route(f"{WEB_PREFIX}/get-tree", methods=["POST"])
@inject
def route_get_dept_tree(
    dept_service: DeptService = Provide[BackendContainer.backbone_container.dept_service],
):
    """
    获取部门树
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        params = DeptTreeQueryParams(**data)
        params.user_id = get_current_user_id()
        dept_tree = dept_service.get_dept_tree(
            params=params,
        )
        carrier.push_succeed_data(data=dept_tree)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
