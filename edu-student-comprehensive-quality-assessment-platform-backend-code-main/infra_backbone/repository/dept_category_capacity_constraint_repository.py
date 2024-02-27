from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.dept_category_capacity_constraint import (
    DeptCategoryCapacityConstraintEntity,
)
from infra_backbone.model.dept_category_capacity_constraint_model import (
    DeptCategoryCapacityConstraintModel,
)


class DeptCategoryCapacityConstraintRepository(BasicRepository):
    def insert_dept_category_capacity_constraint(
        self, data: DeptCategoryCapacityConstraintModel, transaction: Transaction
    ) -> str:
        """
        插入部门类型容量约束
        :param data:
        :param transaction:
        :return:
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=DeptCategoryCapacityConstraintEntity,
            entity_model=data,
            transaction=transaction,
        )

    def delete_dept_category_capacity_constraint_by_id(
        self, dept_category_capacity_constraint_id: str, transaction: Transaction
    ):
        """
        删除部门类型容量约束
        :param dept_category_capacity_constraint_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=DeptCategoryCapacityConstraintEntity,
            entity_id=dept_category_capacity_constraint_id,
            transaction=transaction,
        )
