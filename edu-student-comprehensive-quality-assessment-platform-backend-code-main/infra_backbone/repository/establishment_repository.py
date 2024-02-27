from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.establishment import EstablishmentEntity
from infra_backbone.model.establishment_model import EstablishmentModel


class EstablishmentRepository(BasicRepository):
    def insert_establishment(self, data: EstablishmentModel, transaction: Transaction) -> str:
        """
        插入人员
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=EstablishmentEntity,
            entity_model=data,
            transaction=transaction,
        )

    def get_establishment_max_seq(self, dimension_dept_tree_id: str) -> int:
        """
        :param dimension_dept_tree_id:
        :return:
        """
        sql = """
        SELECT COALESCE(MAX(se.seq), 0) AS max_seq
        FROM st_establishment se
        WHERE se.dimension_dept_tree_id = :dimension_dept_tree_id
        """

        data = self._execute_sql(
            sql=sql,
            params={
                "dimension_dept_tree_id": dimension_dept_tree_id,
            },
        )
        return data[0].get("max_seq")

    def delete_establishment_by_id(self, establishment_id: str, transaction: Transaction):
        """
        删除编制
        :param establishment_id:
        :param transaction:
        :return:
        """

        self._delete_versioned_entity_by_id(
            entity_cls=EstablishmentEntity,
            entity_id=establishment_id,
            transaction=transaction,
        )

    def get_establishment_by_capacity_code_and_dimension_dept_tree_id(
        self,
        capacity_code: str,
        dimension_dept_tree_id: str,
    ):
        """
        根据职责编码和维度获取职责
        """
        sql = """
        select se.* from st_establishment se
        join st_capacity sc on se.capacity_id = sc.id
        where sc.code = :capacity_code and se.dimension_dept_tree_id = :dimension_dept_tree_id
        """
        return self._fetch_first_to_model(
            sql=sql,
            model_cls=EstablishmentModel,
            params={
                "capacity_code": capacity_code,
                "dimension_dept_tree_id": dimension_dept_tree_id,
            },
        )
