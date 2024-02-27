
from biz_comprehensive.model.edit.scene_em import SceneEditModel


def test_add_scene(prepare_app_container, prepare_handler):
    scene_service = prepare_app_container.comprehensive_container.scene_service()
    uow = prepare_app_container.uow()
    transaction = uow.log_transaction(handler=prepare_handler, action="insert_scene")
    with uow:
        scene_service.add_or_update_scene(
            scene_em=SceneEditModel(
                name="社会实践",
                code="SOCIAL_PRACTICE",
                terminal_category_list=["CLASS_PC", "TEACHER_MOBILE", "PARENT_MOBILE"],
            ),
            transaction=transaction,
        )
        