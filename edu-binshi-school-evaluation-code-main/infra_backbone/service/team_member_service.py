from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now

from infra_backbone.model.edit.team_member_em import TeamMemberEm
from infra_backbone.model.params.team_can_select_people_query_params import (
    TeamCanSelectPeopleQueryParams,
)
from infra_backbone.model.params.team_member_query_params import TeamMemberQueryParams
from infra_backbone.model.team_member_model import TeamMemberModel
from infra_backbone.repository.team_member_repository import TeamMemberRepository
from infra_backbone.repository.team_repository import TeamRepository
from infra_backbone.service.team_category_service import TeamCategoryService


class TeamMemberService:
    """
    小组成员 service
    """

    def __init__(
        self,
        team_member_repository: TeamMemberRepository,
        team_repository: TeamRepository,
        team_category_service: TeamCategoryService,
    ):
        self.__team_member_repository = team_member_repository
        self.__team_repository = team_repository
        self.__team_category_service = team_category_service

    def get_team_member_list_page(self, query_params: TeamMemberQueryParams):
        return self.__team_member_repository.get_team_member_list_page(query_params)

    def save_team_member(self, team_member_em: TeamMemberEm, transaction: Transaction):
        """
        保存小组成员
        """

        team = self.__team_repository.get_team_modal_by_team_id(
            team_id=team_member_em.team_id,
        )

        self.__team_category_service.judge_team_category_is_activated(
            team_category_id=team.team_category_id
        )

        for team_member_list in team_member_em.member_group_by_capacity_list:
            max_seq = self.__team_member_repository.get_max_seq_by_team_id_and_capacity_code(
                team_id=team_member_em.team_id, capacity_code=team_member_list.capacity_code
            )
            for idx, member in enumerate(team_member_list.member_list):
                team_member = TeamMemberModel(
                    team_id=team_member_em.team_id,
                    people_id=member.people_id,
                    capacity_id=member.capacity_id,
                    seq=max_seq + idx + 1,
                    start_at=local_now(),
                )
                self.__team_member_repository.insert_team_member(team_member, transaction)

    def get_can_select_people_list_page(self, query_params: TeamCanSelectPeopleQueryParams):
        return self.__team_member_repository.get_can_select_people_list_page(query_params)

    def delete_team_member_by_team_member_id(self, team_member_id: str, transaction: Transaction):
        """
        删除小组成员
        """
        team_member = self.__team_member_repository.get_team_member_by_team_member_id(
            team_member_id
        )
        if not team_member:
            raise BusinessError("小组成员不存在")

        team = self.__team_repository.get_team_modal_by_team_id(
            team_id=team_member.team_id,
        )

        self.__team_category_service.judge_team_category_is_activated(
            team_category_id=team.team_category_id
        )

        team_member.finish_at = local_now()
        self.__team_member_repository.update_team_member(
            team_member=team_member, transaction=transaction, limited_col_list=["finish_at"]
        )
