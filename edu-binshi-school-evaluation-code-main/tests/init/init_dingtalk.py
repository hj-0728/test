from infra_dingtalk.model.dingtalk_corp_model import DingtalkCorpModel
from infra_dingtalk.repository.dingtalk_corp_repository import DingtalkCorpRepository
from infra_dingtalk.model.dingtalk_agent_model import DingtalkAgentModel
from infra_dingtalk.repository.dingtalk_agent_repository import DingtalkAgentRepository


def test_init_dingtalk_corp(prepare_robot, prepare_dingtalk_container):
    uow = prepare_dingtalk_container.uow()
    dingtalk_corp_repository: DingtalkCorpRepository = prepare_dingtalk_container.dingtalk_corp_repository()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_init_dingtalk_corp")
        corp = DingtalkCorpModel(
            remote_corp_id="ding59671a103ffc8e344ac5d6980864d335", name="云迪中学"
        )
        dingtalk_corp_repository.insert_dingtalk_corp(
            corp=corp, transaction=trans
        )


def test_init_dingtalk_agent(prepare_robot, prepare_dingtalk_container):
    uow = prepare_dingtalk_container.uow()
    dingtalk_agent_repository: DingtalkAgentRepository = prepare_dingtalk_container.dingtalk_agent_repository()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_init_dingtalk_agent")
        agent = DingtalkAgentModel(
            dingtalk_corp_id="a878cd9e-bc3b-4acf-a953-c50074a75043",
            code="K12_SYNC",
            app_key="dingvhjoxjuky063hfrz",
            app_secret="VBcbx9OJOkxmrKr6nKt05_YBJYVrT2z7Bja4tMrysu-LasyHEp0ffu9S7msEEP5v",
            remote_agent_id="2627156980",
        )

        dingtalk_agent_repository.insert_dingtalk_agent(
            agent=agent, transaction=trans
        )
