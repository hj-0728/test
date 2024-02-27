from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.query_params import PageFilterParams

from edu_binshi.data.constant import EduBinShiConst
from infra_backbone.data.params.people_page_query_params import PeoplePageQueryParams
from infra_backbone.model.dimension_model import EnumDimensionCategory
from infra_backbone.model.view.people_page_vm import PeoplePageVm
from infra_backbone.repository.dimension_repository import DimensionRepository
from infra_backbone.repository.organization_repository import OrganizationRepository
from infra_backbone.service.people_service import PeopleService as BackbonePeopleService


class PeopleService:
    def __init__(
        self,
        backbone_people_service: BackbonePeopleService,
        organization_repository: OrganizationRepository,
        dimension_repository: DimensionRepository,
    ):
        self.__backbone_people_service = backbone_people_service
        self.__organization_repository = organization_repository
        self.__dimension_repository = dimension_repository

    def get_can_bind_user_people_page(
        self, params: PageFilterParams
    ) -> PaginationCarrier[PeoplePageVm]:
        """

        :param params:
        :return:
        """

        organization = self.__organization_repository.get_organization_by_code(
            code=EduBinShiConst.ORGANIZATION_CODE,
        )

        dimension = self.__dimension_repository.get_dimension_by_category_code_and_organization_id(
            category=EnumDimensionCategory.ADMINISTRATION.name,
            code=EduBinShiConst.DIMENSION_CODE_INNER,
            organization_id=organization.id,
        )

        params = params.cast_to(
            cast_type=PeoplePageQueryParams,
            organization_id=organization.id,
            dimension_id=dimension.id,
        )

        params.gender_list = None

        return self.__backbone_people_service.get_people_page(params=params)
