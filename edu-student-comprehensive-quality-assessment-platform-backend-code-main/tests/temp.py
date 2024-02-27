from infra_backbone.service.robot_service import RobotService


def test_save_img(prepare_backbone_container, prepare_app_container):
    uow = prepare_backbone_container.uow()
    robot_service: RobotService = prepare_backbone_container.robot_service()
    object_storage_service = prepare_app_container.object_storage_container.object_storage_service()
    with uow:
        robot = robot_service.get_system_robot().to_basic_handler()
        transaction = uow.log_transaction(
            handler=robot, action="save_img"
        )
        with open("04.jpg", "rb") as f:
            obj_data = f.read()

            file_info = object_storage_service.upload_file(
                file_name="04.jpg",
                file_blob=obj_data,
                transaction=transaction,
            )
            print(file_info)
