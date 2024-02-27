from typing import List

from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now

from infra_backbone.model.data_permission_model import (
    DataPermissionDetailModel,
    DataPermissionModel,
    EnumDataPermissionObjectCategory,
)
from infra_backbone.repository.data_permission_repository import DataPermissionRepository


class DataPermissionService:
    def __init__(self, data_permission_repository: DataPermissionRepository):
        self.__data_permission_repository = data_permission_repository

    def get_data_permission(
        self,
        subject_category: str,
        subject_id: str,
        aspect: str,
        transaction: Transaction,
        policy: str = "ALLOW",
    ):
        """
        获取数据权限
        :param subject_category:
        :param subject_id:
        :param aspect:
        :param transaction:
        :param policy:
        :return:
        """
        data_permission = self.__data_permission_repository.get_data_permission(
            subject_category=subject_category,
            subject_id=subject_id,
            aspect=aspect,
            policy=policy,
        )
        if not data_permission:
            return self.__data_permission_repository.insert_data_permission(
                data=DataPermissionModel(
                    subject_category=subject_category,
                    subject_id=subject_id,
                    aspect=aspect,
                    policy=policy,
                ),
                transaction=transaction,
            )
        return data_permission.id

    def delete_data_permission_detail_by_data_permission_id(
        self, data_permission_id: str, transaction: Transaction
    ):
        """
        根据数据权限id删除数据权限细节
        :param data_permission_id:
        :param transaction:
        :return:
        """
        detail_list = (
            self.__data_permission_repository.get_data_permission_detail_by_data_permission_id(
                data_permission_id=data_permission_id
            )
        )
        for detail in detail_list:
            self.__data_permission_repository.delete_data_permission_detail(
                data_permission_detail_id=detail.id, transaction=transaction
            )

    def delete_data_permission_detail_list_by_object_list(
        self,
        detail_list: List[DataPermissionDetailModel],
        object_list: List[str],
        transaction: Transaction,
    ):
        """
        根据id list删除数据权限细节
        :param detail_list:
        :param object_list:
        :param transaction:
        :return:
        """
        for detail in detail_list:
            if detail.object_id in object_list:
                self.__data_permission_repository.delete_data_permission_detail(
                    data_permission_detail_id=detail.id, transaction=transaction
                )

    def insert_organization_data_permission_detail_list(
        self, object_list: List[str], data_permission_id: str, transaction: Transaction
    ):
        """
        增加组织类型权限详情
        :param object_list:
        :param data_permission_id:
        :param transaction:
        :return:
        """
        for object_id in object_list:
            data = DataPermissionDetailModel(
                data_permission_id=data_permission_id,
                object_id=object_id,
                object_category=EnumDataPermissionObjectCategory.ORGANIZATION.name,
                start_at=local_now(),
            )
            self.__data_permission_repository.insert_data_permission_detail(
                data=data, transaction=transaction
            )

    def get_data_permission_detail_by_data_permission_id(self, data_permission_id: str):
        """
        根据数据权限id获取数据权限细节
        :param data_permission_id:
        :return:
        """
        return self.__data_permission_repository.get_data_permission_detail_by_data_permission_id(
            data_permission_id=data_permission_id
        )
