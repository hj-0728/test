from infra_utility.enum_helper import enum_to_dict_list

from infra_dingtalk.model.dingtalk_agent_model import DingtalkAgentModel, EnumDingtalkAgent
from infra_dingtalk.model.dingtalk_corp_model import DingtalkCorpModel


def test_add_corp_and_agent(prepare_dingtalk_container, prepare_robot):
    uow = prepare_dingtalk_container.uow()
    corp = prepare_dingtalk_container.dingtalk_corp_repository()
    agent = prepare_dingtalk_container.dingtalk_agent_repository()
    with uow:
        transaction = uow.log_transaction(handler=prepare_robot, action="test_add_corp")
        corp_id = corp.insert_dingtalk_corp(
            corp=DingtalkCorpModel(
                remote_corp_id="ding293ae30a4ee6a2ad4ac5d6980864d335",
                name="建兰小学"
            ),
            transaction=transaction
        )
        code_list = enum_to_dict_list(enum_class=EnumDingtalkAgent)
        for code in code_list:
            agent.insert_dingtalk_agent(
                agent=DingtalkAgentModel(
                    dingtalk_corp_id=corp_id,
                    remote_agent_id="2825317926",
                    code=code["name"],
                    app_key="dingib69tohtfmpvjcmp",
                    app_secret="cUtPReJ4AMEuhX6go-BJkT-zvkvB_61y0AM3cU5mUc6-u2yPIyRSPVi9MDTZRBkF",
                ),
                transaction=transaction
            )
