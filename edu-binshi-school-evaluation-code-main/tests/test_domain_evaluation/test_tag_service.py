from domain_evaluation.data.enum import EnumTagOwnerCategory
from infra_utility.token_helper import generate_uuid_id

from infra_backbone.model.edit.save_tag_em import SaveTagEditModel


def test_save_tag(prepare_backbone_container, prepare_robot):
    tag_service = prepare_backbone_container.tag_service()
    uow = prepare_backbone_container.uow()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action='test_save_tag')
        tag_info = {
            "name": "X（变量）",
            "ownership_list": [
                {
                    "owner_category": EnumTagOwnerCategory.EVALUATION_CRITERIA_TREE.name,
                    "owner_id": generate_uuid_id(),
                },
                {
                    "owner_category": EnumTagOwnerCategory.EVALUATION_CRITERIA_TREE.name,
                    "owner_id": generate_uuid_id(),
                }
            ]

        }
        tag_service.save_tag(
            tag=SaveTagEditModel(**tag_info), transaction=trans
        )
