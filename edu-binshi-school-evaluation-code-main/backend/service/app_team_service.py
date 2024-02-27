from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now

from backend.repository.app_evaluation_criteria_plan_repository import (
    AppEvaluationCriteriaPlanRepository,
)
from infra_backbone.model.team_model import TeamModel
from infra_backbone.service.team_service import TeamService


class AppTeamService:
    def __init__(
        self,
        team_service: TeamService,
        app_evaluation_criteria_plan_repository: AppEvaluationCriteriaPlanRepository,
    ):
        self.__team_service = team_service
        self.__app_evaluation_criteria_plan_repository = app_evaluation_criteria_plan_repository

    def delete_team(self, team_id: str, transaction: Transaction):
        """
        删除小组
        """
        plan_count = self.__app_evaluation_criteria_plan_repository.fetch_team_execute_plan_count(
            team_id=team_id
        )
        if plan_count > 0:
            raise BusinessError("该小组还有正在执行的计划，请等待计划执行完成后再删除")
        self.__team_service.delete_team(team_id=team_id, transaction=transaction)
