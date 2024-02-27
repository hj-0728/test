from infra_backbone.model.edit.save_tag_em import SaveTagEditModel
from infra_backbone.service.robot_service import RobotService


def test_init_tag(prepare_backbone_container):
    uow = prepare_backbone_container.uow()
    robot_service: RobotService = prepare_backbone_container.robot_service()
    tag_service = prepare_backbone_container.tag_service()
    tag_name_list = ['X（变量）', '自评', '他评']
    with uow:
        handler = robot_service.get_system_robot().to_basic_handler()
        trans = uow.log_transaction(handler=handler, action="init_tag")
        for tag_name in tag_name_list:
            tag_service.save_tag_and_related_relationship(
                tag=SaveTagEditModel(
                    name=tag_name,
                    tag_ownership_relationship_list=[]
                ),
                transaction=trans
            )
