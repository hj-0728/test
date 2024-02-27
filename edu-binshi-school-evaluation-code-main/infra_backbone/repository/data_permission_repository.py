from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from infra_backbone.entity.data_permission import DataPermissionEntity
from infra_backbone.entity.data_permission_detail import DataPermissionDetailEntity
from infra_backbone.model.data_permission_model import (
    DataPermissionDetailModel,
    DataPermissionModel,
)


class DataPermissionRepository(BasicRepository):
    def insert_data_permission(self, data: DataPermissionModel, transaction: Transaction) -> str:
        """
        插入数据权限
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DataPermissionEntity,
            entity_model=data,
            transaction=transaction,
        )

    def insert_data_permission_detail(
        self, data: DataPermissionDetailModel, transaction: Transaction
    ) -> str:
        """
        插入数据权限细节
        :param data:
        :param transaction:
        :return:
        """

        return self._insert_versioned_entity_by_model(
            entity_cls=DataPermissionDetailEntity,
            entity_model=data,
            transaction=transaction,
        )

    def get_data_permission(
        self, subject_category: str, subject_id: str, aspect: str, policy: str = "ALLOW"
    ) -> Optional[DataPermissionModel]:
        """
        获取数据权限
        :param subject_category:
        :param subject_id:
        :param aspect:
        :param policy:
        :return:
        """
        sql = """
        select * from st_data_permission where subject_category=:subject_category 
        and subject_id=:subject_id
        and aspect=:aspect and policy=:policy
        """
        return self._fetch_first_to_model(
            model_cls=DataPermissionModel,
            sql=sql,
            params={
                "subject_category": subject_category,
                "subject_id": subject_id,
                "aspect": aspect,
                "policy": policy,
            },
        )

    def get_data_permission_detail_by_data_permission_id(
        self, data_permission_id: str
    ) -> List[DataPermissionDetailModel]:
        """
        根据数据权限id获得数据权限细节
        :param data_permission_id:
        :return:
        """
        sql = """
        SELECT * FROM st_data_permission_detail
        WHERE data_permission_id = :data_permission_id 
        AND object_category = 'ORGANIZATION'
        AND start_at <= now() and finish_at > now()
        """
        return self._fetch_all_to_model(
            model_cls=DataPermissionDetailModel,
            sql=sql,
            params={
                "data_permission_id": data_permission_id,
            },
        )

    def delete_data_permission_detail(self, data_permission_detail_id, transaction: Transaction):
        """
        根据id删除数据权限详情
        :param data_permission_detail_id:
        :param transaction:
        :return:
        """
        self._delete_versioned_entity_by_id(
            entity_cls=DataPermissionDetailEntity,
            entity_id=data_permission_detail_id,
            transaction=transaction,
        )
