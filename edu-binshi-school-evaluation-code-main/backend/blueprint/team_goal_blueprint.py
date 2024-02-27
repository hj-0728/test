import traceback

from dependency_injector.wiring import inject, Provide
from flask import Blueprint, jsonify, request
from infra_basic.errors import BusinessError
from infra_basic.message_carrier import MessageCarrier

from backend.backend_containers import BackendContainer
from backend.data.constant import FlaskConfigConst
from infra_backbone.model.params.team_goal_query_params import TeamGoalQueryParams
from infra_backbone.service.team_goal_service import TeamGoalService

blueprint_team_goal = Blueprint(
    name="team-goal",
    import_name=__name__,
    url_prefix=f"{FlaskConfigConst.API_PREFIX}",
)

WEB_PREFIX = "/web/team-goal"


@blueprint_team_goal.route(f"{WEB_PREFIX}/get-team-goal-tree", methods=["POST"])
@inject
def route_get_team_goal_tree(
    team_goal_service: TeamGoalService = Provide[
        BackendContainer.backbone_container.team_goal_service
    ],
):
    """
    获取小组目标树
    """
    carrier = MessageCarrier()
    try:
        data = request.get_json(silent=True)
        dept_tree = team_goal_service.get_team_goal_tree(
            query_params=TeamGoalQueryParams(**data),
        )
        carrier.push_succeed_data(data=dept_tree)
    except BusinessError as err:
        traceback.print_exc()
        carrier.push_exception(err=err)
    return jsonify(carrier.dict(by_alias=True))
