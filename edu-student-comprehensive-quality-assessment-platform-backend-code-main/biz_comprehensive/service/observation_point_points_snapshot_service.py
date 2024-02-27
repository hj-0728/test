from infra_basic.transaction import Transaction

from biz_comprehensive.repository.observation_point_points_snapshot_repository import (
    ObservationPointPointsSnapshotRepository,
)


class ObservationPointPointsSnapshotService:
    def __init__(
        self,
        observation_point_points_snapshot_repository: ObservationPointPointsSnapshotRepository,
    ):
        self.__observation_point_points_snapshot_repository = (
            observation_point_points_snapshot_repository
        )

    def add_observation_point_points_snapshot(
        self, observation_point_log_id: str, transaction: Transaction
    ):
        """
        添加观测点积分快照
        :param observation_point_log_id:
        :param transaction:
        :return:
        """

        snapshot_source_data = self.__observation_point_points_snapshot_repository.fetch_observation_point_points_snapshot_source(
            observation_point_log_id=observation_point_log_id
        )
        for snapshot in snapshot_source_data:
            self.__observation_point_points_snapshot_repository.insert_observation_point_points_snapshot(
                data=snapshot, transaction=transaction
            )

    def delete_observation_point_points_snapshot(
        self, observation_action_id: str, transaction: Transaction
    ):
        """
        删除观测点积分快照
        """
        snapshot_list = self.__observation_point_points_snapshot_repository.fetch_observation_point_points_snapshot(
            observation_action_id=observation_action_id
        )
        for snapshot in snapshot_list:
            self.__observation_point_points_snapshot_repository.delete_observation_point_points_snapshot(
                snapshot_id=snapshot.id, transaction=transaction
            )
