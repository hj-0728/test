from infra_basic.errors import BusinessError
from infra_basic.errors.input import DataNotFoundError
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.transaction import Transaction

from infra_backbone.model.organization_model import OrganizationModel
from infra_backbone.model.params.organization_params import OrganizationQueryParams
from infra_backbone.model.view.organization_address_area_vm import OrganizationAddressAreaViewModel
from infra_backbone.repository.organization_repository import OrganizationRepository
from infra_backbone.service.area_service import AreaService


class OrganizationService:
    def __init__(
        self,
        area_service: AreaService,
        organization_repository: OrganizationRepository,
    ):
        self.__area_service = area_service
        self.__organization_repository = organization_repository

    def get_organization_address_equal_level_area_list(
        self, organization_id: str, seq: int = 1, fetch_parent: bool = False
    ) -> OrganizationAddressAreaViewModel:
        """
        获取组织地址相同层级的地域列表
        :param organization_id:
        :param seq: 默认获取组织第一个地址
        :param fetch_parent: 是否获取父级地域列表
        :return:
        """
        area = self.__organization_repository.fetch_organization_address_belong_area(
            organization_id=organization_id, seq=seq
        )
        if not area:
            raise DataNotFoundError("未获取到组织所属区域")
        area_list = self.__area_service.get_area_list_group_by_initials(parent_id=area.parent_id)
        parent_area_list = []
        if fetch_parent:
            parent_area_list = self.__area_service.get_area_with_parent_list(area_id=area.parent_id)
        return OrganizationAddressAreaViewModel(
            area_list=area_list, parent_area_list=parent_area_list
        )

    def get_organization_by_code(self, code: str):
        """
        根据编码获取组织
        :param code:
        :return:
        """
        return self.__organization_repository.get_organization_by_code(
            code=code,
        )

    def get_organization_list_by_category(self, category: str):
        """
        根据组织类型获取组织列表
        :param category:
        :return:
        """
        return self.__organization_repository.get_organization_list_by_category(category=category)

    def get_organization_list(
        self,
        query_params: OrganizationQueryParams,
    ) -> PaginationCarrier[OrganizationModel]:
        """
        获取组织列表
        """
        result = self.__organization_repository.get_organization_list(
            query_params=query_params,
        )
        return result

    def add_organization(self, organization: OrganizationModel, transaction: Transaction) -> str:
        """
        添加组织
        :param organization:
        :param transaction:
        :return:
        """
        is_exist_name = self.__organization_repository.fetch_organization_by_name(
            name=organization.name
        )
        is_exist_code = self.__organization_repository.fetch_organization_by_code(
            code=organization.code
        )
        if is_exist_name:
            raise BusinessError("此组织名称已存在")
        elif is_exist_code:
            raise BusinessError("此组织编码已存在")
        return self.__organization_repository.insert_organization(
            data=organization,
            transaction=transaction,
        )

    def edit_organization(self, data: OrganizationModel, transaction: Transaction):
        """
        编辑组织
        """
        is_exist = self.__organization_repository.get_same_organization_name(
            name=data.name, organization_id=data.id
        )
        if is_exist:
            raise BusinessError("组织名称已存在，重新输入")

        return self.__organization_repository.update_organization(
            data=data,
            transaction=transaction,
            limited_col_list=["name", "category", "is_activated", "code"],
        )

    def update_activated(
        self,
        data: OrganizationModel,
        transaction: Transaction,
    ):
        return self.__organization_repository.update_organization(
            data=data, transaction=transaction, limited_col_list=["is_activated"]
        )
