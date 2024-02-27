"""
测试同步相关
"""
from infra_dingtalk.agent_plugin.sync_plugin import SyncAgentPlugin
from infra_dingtalk.data.agent_plugin.setup_options import AgentPluginSetupOptions

redis_url = "redis://:redis@10.10.10.103:6379/30"
setup_options = AgentPluginSetupOptions(
    corp_id="ding59671a103ffc8e344ac5d6980864d335",
    app_key="dingvhjoxjuky063hfrz",
    app_secret="VBcbx9OJOkxmrKr6nKt05_YBJYVrT2z7Bja4tMrysu-LasyHEp0ffu9S7msEEP5v",
    redis_url=redis_url,
)
sync_plugin = SyncAgentPlugin(setup_options=setup_options)


def test_sync_k12(prepare_backend_container, prepare_robot):
    uow = prepare_backend_container.uow()
    sync_service = prepare_backend_container.dingtalk_container.sync_service()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_sync_k12")
        sync_service.sync_k12_from_remote(dingtalk_corp_id="a878cd9e-bc3b-4acf-a953-c50074a75043", transaction=trans)


def test_inner_sync(prepare_backend_container, prepare_robot):
    uow = prepare_backend_container.uow()
    sync_service = prepare_backend_container.dingtalk_container.sync_service()
    with uow:
        transaction = uow.log_transaction(handler=prepare_robot, action="test_inner_sync")
        sync_service.sync_inner_from_remote(
            dingtalk_corp_id="a878cd9e-bc3b-4acf-a953-c50074a75043",
            transaction=transaction
        )
