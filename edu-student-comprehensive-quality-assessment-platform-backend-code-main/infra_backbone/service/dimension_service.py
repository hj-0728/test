from typing import Optional

from infra_backbone.model.dimension_model import DimensionModel
from infra_backbone.repository.dimension_repository import DimensionRepository
from infra_backbone.repository.organization_repository import OrganizationRepository


class DimensionService:
    def __init__(
        self,
        dimension_repository: DimensionRepository,
        organization_repository: OrganizationRepository,
    ):
        self.__dimension_repository = dimension_repository
        self.__organization_repository = organization_repository

    def get_dimension_by_category_code_and_organization_id(
        self,
        code: str,
        category: str,
        organization_id: str,
    ) -> Optional[DimensionModel]:
        """
        根据category、code、organization_id获取维度
        :return:
        """
        return self.__dimension_repository.get_dimension_by_category_code_and_organization_id(
            code=code,
            category=category,
            organization_id=organization_id,
        )

    def get_dimension_list(self, organization_id: str):
        """
        organization_id: str
        :return:
        """
        return self.__dimension_repository.fetch_organization_dimension_list(
            organization_id=organization_id,
        )

    def get_dimension_by_organization_code_and_category_code(
        self,
        organization_code: str,
        dimension_code: str,
        dimension_category: str,
    ) -> Optional[DimensionModel]:
        """
        根据organization_code、dimension_code、dimension_category获取维度
        :param organization_code:
        :param dimension_code:
        :param dimension_category:
        :return:
        """
        organization = self.__organization_repository.get_organization_by_code(
            code=organization_code
        )

        return self.get_dimension_by_category_code_and_organization_id(
            code=dimension_code,
            category=dimension_category,
            organization_id=organization.id,
        )
