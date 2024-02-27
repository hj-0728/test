from typing import List

from infra_utility.base_plus_model import BasePlusModel


class MemberEm(BasePlusModel):
    """
    成员
    """

    people_id: str
    capacity_id: str
    seq: int = 1


class MemberGroupByCapacityCodeEm(BasePlusModel):
    """
    按职责分组的成员
    """

    capacity_code: str
    member_list: List[MemberEm] = []


class TeamMemberEm(BasePlusModel):
    """
    小组成员
    """

    team_id: str
    member_group_by_capacity_list: List[MemberGroupByCapacityCodeEm] = []
