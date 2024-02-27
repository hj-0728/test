def test_add_observation_point_points_snapshot(prepare_biz_comprehensive, prepare_robot):
    service = prepare_biz_comprehensive.observation_point_points_snapshot_service()
    uow = prepare_biz_comprehensive.uow()
    transaction = uow.log_transaction(handler=prepare_robot, action="test_add_observation_point_points_snapshot")
    with uow:
        service.add_observation_point_points_snapshot(
            observation_point_log_id="24f42a11-33b6-4937-934a-d23c7321a41a",
            transaction=transaction,
        )
        