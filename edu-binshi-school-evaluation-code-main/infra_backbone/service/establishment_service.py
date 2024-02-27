from typing import Optional

from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now

from infra_backbone.model.capacity_model import CapacityModel
from infra_backbone.model.establishment_model import EstablishmentModel
from infra_backbone.repository.capacity_repository import CapacityRepository
from infra_backbone.repository.establishment_repository import EstablishmentRepository


class EstablishmentService:
    def __init__(
        self,
        establishment_repository: EstablishmentRepository,
        capacity_repository: CapacityRepository,
    ):
        self.__establishment_repository = establishment_repository
        self.__capacity_repository = capacity_repository

    def add_establishment(self, establishment: EstablishmentModel, transaction: Transaction):
        exist_establishment = self.__establishment_repository.get_establishment(
            dimension_dept_tree_id=establishment.dimension_dept_tree_id,
            position_id=establishment.position_id,
            people_id=establishment.people_id,
        )
        if exist_establishment:
            raise BusinessError("请勿重复添加")
        max_seq = self.__establishment_repository.get_establishment_max_seq(
            establishment.dimension_dept_tree_id,
        )
        establishment.seq = max_seq + 1
        self.__establishment_repository.insert_establishment(
            data=establishment,
            transaction=transaction,
        )

    def fetch_establishment_info(
        self,
        capacity_name: Optional[str],
        capacity_code: str,
        dimension_dept_tree_id: str,
        transaction: Transaction,
    ) -> EstablishmentModel:
        """
        获取职责
        :param capacity_name:
        :param capacity_code:
        :param dimension_dept_tree_id:
        :param transaction:
        :return:
        """
        assignment = self.__establishment_repository.get_establishment_by_capacity_code_and_dimension_dept_tree_id(
            dimension_dept_tree_id=dimension_dept_tree_id,
            capacity_code=capacity_code,
        )
        if not assignment:
            capacity = self.__capacity_repository.get_capacity_model_by_code(
                capacity_code=capacity_code,
            )
            capacity_id = capacity.id
            if not capacity:
                capacity_id = self.__capacity_repository.insert_capacity(
                    data=CapacityModel(name=capacity_name, code=capacity_code),
                    transaction=transaction,
                )
            assignment = EstablishmentModel(
                dimension_dept_tree_id=dimension_dept_tree_id,
                capacity_id=capacity_id,
                start_at=local_now(),
            )
            assignment.id = self.__establishment_repository.insert_establishment(
                data=assignment,
                transaction=transaction,
            )

        return assignment

    def delete_establishment_by_id(self, establishment_id: str, transaction: Transaction):
        self.__establishment_repository.delete_establishment_by_id(
            establishment_id=establishment_id,
            transaction=transaction,
        )
