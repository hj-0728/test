from datetime import datetime
from typing import Optional

from infra_basic.errors import BusinessError
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now

from infra_backbone.model.edit.team_em import TeamEditModal
from infra_backbone.model.params.team_query_params import TeamQueryParams
from infra_backbone.model.team_model import TeamModel
from infra_backbone.model.view.team_vm import TeamViewModel
from infra_backbone.repository.team_repository import TeamRepository
from infra_backbone.service.team_category_service import TeamCategoryService
from infra_backbone.service.team_goal_service import TeamGoalService


class TeamService:
    """
    小组 service
    """

    def __init__(
        self,
        team_repository: TeamRepository,
        team_goal_service: TeamGoalService,
        team_category_service: TeamCategoryService,
    ):
        self.__team_repository = team_repository
        self.__team_goal_service = team_goal_service
        self.__team_category_service = team_category_service

    def get_team_list_page(self, current_user_id: str, query_params: TeamQueryParams) -> PaginationCarrier[TeamViewModel]:
        """
        获取小组分页列表
        """
        team_list = self.__team_repository.get_team_page(
            current_user_id=current_user_id,
            query_params=query_params,
        )
        return team_list

    def save_team(self, team_em: TeamEditModal, transaction: Transaction):
        """
        保存小组
        :param team_em:
        :param transaction:
        :return:
        """
        self.__team_category_service.judge_team_category_is_activated(
            team_category_id=team_em.team_category_id
        )

        team_info = self.__team_repository.get_existed_team_by_name_except_current_id(
            name=team_em.name,
            team_category_id=team_em.team_category_id,
            team_id=team_em.id,
        )
        if team_info:
            raise BusinessError("此小组名称已被使用")
        if team_em.id:
            original_team = self.__team_repository.get_team_modal_by_team_id(team_id=team_em.id)
            if not original_team:
                raise BusinessError("此小组不存在")
            if original_team.name != team_em.name:
                self.__team_repository.update_team(
                    team=team_em.cast_to(TeamModel),
                    transaction=transaction,
                    col_list=["name"],
                )
        else:
            team_em.id = self.__team_repository.insert_team(
                team=team_em.cast_to(TeamModel),
                transaction=transaction,
            )
        self.__team_goal_service.save_or_update_team_goal(
            team_id=team_em.id,
            team_goal_list=team_em.team_goal_list,
            transaction=transaction,
        )
        return team_em.id

    def delete_team(
        self,
        team_id: str,
        transaction: Transaction,
    ):
        """
        删除小组
        :param team_id:
        :param transaction:
        :return:
        """

        team = self.__team_repository.get_team_modal_by_team_id(
            team_id=team_id,
        )
        if not team:
            raise BusinessError("此小组不存在")

        self.__team_category_service.judge_team_category_is_activated(
            team_category_id=team.team_category_id
        )

        team.finish_at = local_now()
        self.__team_repository.update_team(
            team=team,
            transaction=transaction,
            col_list=["finish_at"],
        )

    def get_team_detail(
        self,
        team_id: str,
    ):
        """
        获取小组类型详情
        :param team_id:
        """
        team_info = self.__team_repository.get_team_vm_by_team_id(team_id=team_id)
        if not team_info:
            raise BusinessError("此小组不存在")
        team_info.team_goal_list = self.__team_goal_service.get_team_goal_list_by_team_id(
            team_id=team_id,
        )
        return team_info
