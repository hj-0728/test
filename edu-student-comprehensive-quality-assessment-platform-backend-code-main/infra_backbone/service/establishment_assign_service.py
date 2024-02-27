from typing import List

from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now

from infra_backbone.model.edit.add_people_em import EstablishmentAssignViewModel
from infra_backbone.model.establishment_assign_model import EstablishmentAssignModel
from infra_backbone.repository.establishment_assign_repository import EstablishmentAssignRepository
from infra_backbone.service.dimension_dept_tree_service import DimensionDeptTreeService
from infra_backbone.service.establishment_service import EstablishmentService


class EstablishmentAssignService:
    def __init__(
        self,
        dimension_dept_tree_service: DimensionDeptTreeService,
        establishment_service: EstablishmentService,
        establishment_assign_repository: EstablishmentAssignRepository,
    ):
        self.__dimension_dept_tree_service = dimension_dept_tree_service
        self.__establishment_service = establishment_service
        self.__establishment_assign_repository = establishment_assign_repository

    def add_establishment_assign(
        self,
        establishment_assign_list: List[EstablishmentAssignViewModel],
        people_id: str,
        transaction: Transaction,
    ):
        """
        获取人职责维度部门树关系
        :param establishment_assign_list:
        :param people_id:
        :param transaction:
        :return:
        """
        establishment_dict = {}
        for establishment_assign in establishment_assign_list:
            key = f"{establishment_assign.dimension_dept_tree_id}&&{establishment_assign.capacity_code}"
            if establishment_assign.establishment_id:
                establishment_id = establishment_assign.establishment_id
            elif establishment_dict.get(key):
                establishment_id = establishment_dict[key]
            else:
                establishment = self.__establishment_service.fetch_establishment_info(
                    capacity_code=establishment_assign.capacity_code,
                    dimension_dept_tree_id=establishment_assign.dimension_dept_tree_id,
                    transaction=transaction,
                )
                establishment_id = establishment.id
                establishment_dict[key] = establishment.id
            self.__establishment_assign_repository.insert_establishment_assign(
                data=EstablishmentAssignModel(
                    establishment_id=establishment_id,
                    people_id=people_id,
                ),
                transaction=transaction,
            )

    def update_people_establishment_assign(
        self,
        establishment_assign_list: List[EstablishmentAssignViewModel],
        organization_id: str,
        people_id: str,
        transaction: Transaction,
    ):
        """
        获取人职责维度部门树关系
        :param establishment_assign_list:
        :param organization_id:
        :param people_id:
        :param transaction:
        :return:
        """
        handle_time = local_now()
        exist_establishment_assign_list = (
            self.__establishment_assign_repository.get_people_establishment_assign(
                organization_id=organization_id, people_id=people_id
            )
        )
        exist_assign_dict = {}
        for exist_establishment_assign in exist_establishment_assign_list:
            if not exist_assign_dict.get(
                exist_establishment_assign.establishment_id
                + exist_establishment_assign.dimension_category
            ):
                exist_assign_dict[
                    exist_establishment_assign.establishment_id
                    + exist_establishment_assign.dimension_category
                ] = exist_establishment_assign
            else:
                self.__establishment_assign_repository.delete_establishment_assign_by_id(
                    establishment_assign_id=exist_establishment_assign.id,
                    transaction=transaction,
                )
        establishment_assign_dict = {}
        for establishment_assign in establishment_assign_list:
            if not establishment_assign.establishment_id:
                establishment = self.__establishment_service.fetch_establishment_info(
                    capacity_code=establishment_assign.capacity_code,
                    dimension_dept_tree_id=establishment_assign.dimension_dept_tree_id,
                    transaction=transaction,
                )
                establishment_assign.establishment_id = establishment.id
            establishment_assign_dict[
                establishment_assign.establishment_id + establishment_assign.dimension_category
            ] = establishment_assign
        # 添加
        for k, v in establishment_assign_dict.items():
            if not exist_assign_dict.get(k):
                self.__establishment_assign_repository.insert_establishment_assign(
                    data=EstablishmentAssignModel(
                        establishment_id=v.establishment_id,
                        people_id=people_id,
                        started_on=handle_time,
                    ),
                    transaction=transaction,
                )
        # 删除
        for k, v in exist_assign_dict.items():
            if not establishment_assign_dict.get(k):
                self.__establishment_assign_repository.delete_establishment_assign_by_id(
                    establishment_assign_id=v.id, transaction=transaction
                )
