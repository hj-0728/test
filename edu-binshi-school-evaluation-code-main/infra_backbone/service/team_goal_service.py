from typing import List

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.algorithm.tree import list_to_tree
from infra_utility.datetime_helper import local_now

from infra_backbone.data.constant import DimensionCodeConst, OrganizationCodeConst
from infra_backbone.model.dimension_model import EnumDimensionCategory
from infra_backbone.model.edit.team_goal_em import TeamGoalEditModel
from infra_backbone.model.params.team_goal_query_params import TeamGoalQueryParams
from infra_backbone.model.team_goal_model import TeamGoalModel

# from infra_backbone.model.dept_tree_model import DeptTreeModel
from infra_backbone.model.view.team_goal_tree_vm import TeamGoalTreeViwModel
from infra_backbone.repository.dept_repository import DeptRepository
from infra_backbone.repository.dimension_dept_tree_repository import DimensionDeptTreeRepository
from infra_backbone.repository.dimension_repository import DimensionRepository
from infra_backbone.repository.position_repository import PositionRepository
from infra_backbone.repository.team_goal_repository import TeamGoalRepository
from infra_backbone.service.dept_dept_category_map_service import DeptDeptCategoryMapService
from infra_backbone.service.dimension_service import DimensionService
from infra_backbone.service.organization_service import OrganizationService


class TeamGoalService:
    """
    小组目标service
    """

    def __init__(
        self,
        team_goal_repository: TeamGoalRepository,
        dimension_dept_tree_repository: DimensionDeptTreeRepository,
        dimension_repository: DimensionRepository,
        position_repository: PositionRepository,
        dept_dept_category_map_service: DeptDeptCategoryMapService,
        organization_service: OrganizationService,
        dimension_service: DimensionService,
        dept_repository: DeptRepository,
    ):
        self.__dept_repository = dept_repository
        self.__team_goal_repository = team_goal_repository
        self.__dimension_dept_tree_repository = dimension_dept_tree_repository
        self.__dimension_repository = dimension_repository
        self.__dept_dept_category_map_service = dept_dept_category_map_service
        self.__organization_service = organization_service
        self.__dimension_service = dimension_service
        self.__position_repository = position_repository

    def get_team_goal_tree(
        self,
        query_params: TeamGoalQueryParams,
    ):
        """
        获取部门树
        :return:
        """
        organization = self.__organization_service.get_organization_by_code(
            code=OrganizationCodeConst.BJSYXX
        )
        dimension = self.__dimension_service.get_dimension_by_category_code_and_organization_id(
            code=DimensionCodeConst.DINGTALK_EDU,
            category=EnumDimensionCategory.EDU.name,
            organization_id=organization.id,
        )
        if not dimension:
            raise BusinessError("未找到部门所在维度")
        team_goal_tree_list = self.__team_goal_repository.get_team_goal_tree(
            dimension_id=dimension.id,
            team_id=query_params.team_id,
            team_category_id=query_params.team_category_id,
        )
        tree = list_to_tree(
            original_list=team_goal_tree_list,
            tree_node_type=TeamGoalTreeViwModel,
        )
        # 用组织做假根
        tree_root = [
            TeamGoalTreeViwModel(
                id=organization.id,
                key=organization.id,
                name=organization.name,
                level=0,
                parent_id=None,
                parent_name=None,
                dimension_dept_tree_id=None,
                comments=None,
                dept_category_code="ORGANIZATION",
                seq=0,
                children=tree,
            )
        ]
        return tree_root

    def save_or_update_team_goal(
        self,
        team_id: str,
        team_goal_list: List[TeamGoalEditModel],
        transaction: Transaction,
    ):
        original_team_goal_list = self.__team_goal_repository.get_team_goal_list_by_team_id(
            team_id=team_id
        )
        original_team_goal_dict = {
            f"{item.goal_category}&&{item.goal_id}&&{item.activity}": item
            for item in original_team_goal_list
        }
        new_team_goal_dict = {
            f"{item.goal_category}&&{item.goal_id}&&{item.activity}": item
            for item in team_goal_list
        }
        for k, v in new_team_goal_dict.items():
            if not original_team_goal_dict.get(k):
                team_goal = TeamGoalModel(
                    team_id=team_id,
                    goal_category=v.goal_category,
                    goal_id=v.goal_id,
                    activity=v.activity,
                    start_at=local_now(),
                )
                self.__team_goal_repository.insert_team_goal(
                    team_goal=team_goal,
                    transaction=transaction,
                )
        for k, v in original_team_goal_dict.items():
            if not new_team_goal_dict.get(k):
                v.finish_at = local_now()
                self.__team_goal_repository.update_team_goal(
                    team_goal=v.cast_to(TeamGoalModel),
                    transaction=transaction,
                    limited_col_list=["finish_at"],
                )

    def get_team_goal_list_by_team_id(self, team_id: str):
        """
        根据team_id获得team_goal的数据
        """
        return self.__team_goal_repository.get_team_goal_list_by_team_id(
            team_id=team_id,
        )
