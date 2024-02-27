from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.dimension import DimensionEntity
from infra_backbone.model.dimension_model import DimensionModel


class DimensionRepository(BasicRepository):
    def insert_dimension(self, data: DimensionModel, transaction: Transaction) -> str:
        """
        插入维度
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DimensionEntity, entity_model=data, transaction=transaction
        )

    def get_dimension_by_category_code_and_organization_id(
        self, category: str, code: str, organization_id: str
    ) -> Optional[DimensionModel]:
        """
        根据category、code获取维度
        :param category:
        :param code:
        :param organization_id:
        :return:
        """

        sql = """select * from st_dimension where category = :category and code = :code
        and organization_id = :organization_id"""
        return self._fetch_first_to_model(
            model_cls=DimensionModel,
            sql=sql,
            params={
                "category": category,
                "code": code,
                "organization_id": organization_id,
            },
        )

    def fetch_organization_dimension_list(self, organization_id: str) -> List[DimensionModel]:
        """
        获取组织的维度
        :return:
        """

        sql = """select * from st_dimension where organization_id = :organization_id"""
        return self._fetch_all_to_model(
            model_cls=DimensionModel,
            sql=sql,
            params={"organization_id": organization_id},
        )

    def get_dimension_by_category_and_organization_id(
        self, category: str, organization_id: str
    ) -> Optional[DimensionModel]:
        """
        根据category、organization_id 获取维度
        :param category:
        :param organization_id:
        :return:
        """

        sql = """select * from st_dimension where category = :category
        and organization_id = :organization_id"""
        return self._fetch_first_to_model(
            model_cls=DimensionModel,
            sql=sql,
            params={
                "category": category,
                "organization_id": organization_id,
            },
        )
