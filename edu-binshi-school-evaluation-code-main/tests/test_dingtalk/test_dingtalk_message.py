"""
测试钉钉消息相关
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


def test_dingtalk_message(prepare_backend_container, prepare_handler):
    uow = prepare_backend_container.uow()
    message_service = prepare_backend_container.dingtalk_container.dingtalk_message_service()
    with uow:
        message_service.send_message_to_dingtalk_users(
            dingtalk_corp_id="a878cd9e-bc3b-4acf-a953-c50074a75043",
            dingtalk_user_ids=['1805260804734828', '4707060359774889'],
            title='小夏测试消息发送',
            description='这就是测试消息',
            url='https://www.baidu.com',
        )
