"""
测试同步相关
"""


def test_inner_sync_from_dd(prepare_dingtalk_container, prepare_robot):
    uow = prepare_dingtalk_container.uow()
    sync_service = prepare_dingtalk_container.sync_service()
    with uow:
        transaction = uow.log_transaction(handler=prepare_robot, action="test_inner_sync_from_dd")
        sync_service.sync_inner_from_remote(
            dingtalk_corp_id="b51e6648-7947-4969-8c1f-52051ecb5673",
            transaction=transaction
        )


def test_sync_k12_from_dd(prepare_dingtalk_container, prepare_robot):
    uow = prepare_dingtalk_container.uow()
    sync_service = prepare_dingtalk_container.sync_service()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_sync_k12_from_dd")
        sync_service.sync_k12_from_remote(dingtalk_corp_id="b51e6648-7947-4969-8c1f-52051ecb5673", transaction=trans)



