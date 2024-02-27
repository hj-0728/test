from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction

from infra_backbone.model.team_category_model import TeamCategoryModel
from infra_backbone.repository.team_category_repository import TeamCategoryRepository
from infra_backbone.model.params.team_category_query_params import TeamCategoryQueryParams


class TeamCategoryService:
    """
    小组类型 service
    """

    def __init__(
        self,
        team_category_repository: TeamCategoryRepository,
    ):
        self.__team_category_repository = team_category_repository

    def get_team_category_list_page(self, query_params: TeamCategoryQueryParams):
        """
        获取小组类型
        """
        return self.__team_category_repository.fetch_team_category_page(query_params=query_params)

    def get_team_category_detail(
        self,
        team_category_id: str,
    ):
        """
        获取小组类型详情
        :param team_category_id:
        """
        team_category_detail = self.__team_category_repository.get_team_category_detail(
            team_category_id=team_category_id
        )
        return team_category_detail

    def save_team_category(self, team_category: TeamCategoryModel, transaction: Transaction):
        """
        保存小组类型
        :param team_category:
        :param transaction:
        :return:
        """
        exist_team_category_info = self.__team_category_repository.get_team_category_by_name(
            name=team_category.name,
            team_category_id=team_category.id,
        )
        if exist_team_category_info:
            raise BusinessError("此小组类型名称已被使用")
        if team_category.id:
            self.__team_category_repository.update_team_category(
                team_category=team_category,
                transaction=transaction,
                limited_col_list=["name"],
            )
        else:
            team_category.id = self.__team_category_repository.insert_team_category(
                team_category=team_category,
                transaction=transaction,
            )

    def change_team_category_activated(
        self,
        team_category: TeamCategoryModel,
        transaction: Transaction,
    ):
        """
        改变激活状态
        :param team_category:
        :param transaction:
        :return:
        """
        self.__team_category_repository.update_team_category(
            team_category=team_category, transaction=transaction, limited_col_list=["is_activated"]
        )

    def judge_team_category_is_activated(
        self, team_category_id: str
    ) -> bool:
        """
        判断小组类型是否被激活
        :param team_category_id:
        :return:
        """

        team_category = self.__team_category_repository.fetch_team_category_by_id(
            team_category_id=team_category_id
        )

        if not team_category.is_activated:
            raise BusinessError("小组类型被禁用，无法修改")

        return True
