from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now

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

    def fetch_establishment_info(
        self,
        capacity_code: str,
        dimension_dept_tree_id: str,
        transaction: Transaction,
    ) -> EstablishmentModel:
        """
        获取职责
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
            if not capacity:
                raise BusinessError(f"职责【{capacity_code}】不存在")
            capacity_id = capacity.id
            assignment = EstablishmentModel(
                dimension_dept_tree_id=dimension_dept_tree_id,
                capacity_id=capacity_id,
                started_on=local_now(),
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
