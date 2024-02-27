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


def test_sync_dept(prepare_backend_container, prepare_robot):
    uow = prepare_backend_container.uow()
    sync_service = prepare_backend_container.context_sync_containers.sync_dingtalk_service()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_sync")
        sync_service.sync_dingtalk_dept_to_master(
            dingtalk_corp_id="a878cd9e-bc3b-4acf-a953-c50074a75043",
            transaction=trans
        )


def test_sync_dingtalk_user(prepare_backend_container, prepare_robot):
    uow = prepare_backend_container.uow()
    sync_service = prepare_backend_container.context_sync_containers.sync_dingtalk_service()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_sync")
        sync_service.sync_dingtalk_user_to_master(
            dingtalk_corp_id="a878cd9e-bc3b-4acf-a953-c50074a75043", transaction=trans
        )


def test_sync_parent_and_student(prepare_backend_container, prepare_robot):
    uow = prepare_backend_container.uow()
    sync_service = prepare_backend_container.context_sync_containers.sync_dingtalk_service()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_sync")
        sync_service.sync_dingtalk_parent_and_student_to_master(
            dingtalk_corp_id="a878cd9e-bc3b-4acf-a953-c50074a75043",
            transaction=trans
        )


def test_add_student_avatar(prepare_backend_container, prepare_robot):
    uow = prepare_backend_container.uow()
    with uow:
        dingtalk_corp_id = "a878cd9e-bc3b-4acf-a953-c50074a75043"
        trans = uow.log_transaction(
            handler=prepare_robot,
            action="test_add_student_avatar",
            action_params={
                "dingtalk_corp_id": dingtalk_corp_id,
            }
        )
        sync_service = prepare_backend_container.context_sync_containers.sync_dingtalk_user_service()
        people_repository = prepare_backend_container.context_sync_containers.context_people_user_map_repository()
        student_list = people_repository.get_no_avatar_student_people()
        student_ids = [x.id for x in student_list]
        for people_id in student_ids:
            sync_service.add_student_avatar(
                people_id=people_id,
                transaction=trans
            )
