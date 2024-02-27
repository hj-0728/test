"""
如果以后有多个快照，需要中转的就从这个service转
以避免像backend中的tasks_service.py收到任务需要添加或删除快照的时候，引入不同的快照service
"""
from infra_basic.transaction import Transaction

from biz_comprehensive.data.enum import EnumComprehensiveResource
from biz_comprehensive.service.observation_point_points_snapshot_service import (
    ObservationPointPointsSnapshotService,
)


class SnapshotService:
    def __init__(
        self,
        observation_point_points_snapshot_service: ObservationPointPointsSnapshotService,
    ):
        self.__observation_point_points_snapshot_service = observation_point_points_snapshot_service

    def add_snapshot(self, source_res_category: str, source_res_id: str, transaction: Transaction):
        """
        添加快照
        :param source_res_category:
        :param source_res_id:
        :param transaction:
        :return:
        """
        if source_res_category == EnumComprehensiveResource.OBSERVATION_POINT_LOG.name:
            self.__observation_point_points_snapshot_service.add_observation_point_points_snapshot(
                observation_point_log_id=source_res_id, transaction=transaction
            )

    def delete_snapshot(
        self, source_res_category: str, source_res_id: str, transaction: Transaction
    ):
        """
        删除快照
        :param source_res_category:
        :param source_res_id:
        :param transaction:
        :return:
        """
        if source_res_category == EnumComprehensiveResource.OBSERVATION_ACTION.name:
            self.__observation_point_points_snapshot_service.delete_observation_point_points_snapshot(
                observation_action_id=source_res_id, transaction=transaction
            )
