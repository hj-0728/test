from biz_comprehensive.data.enum import EnumDictMetaCode


dingtalk_corp_id = "b51e6648-7947-4969-8c1f-52051ecb5673"


def test_log_transaction(prepare_app_container, prepare_robot):
    uow = prepare_app_container.uow()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_log_transaction")
        print(f"Transaction logged with ID: {trans.id}")


def test_sync_dept(prepare_app_container, prepare_robot):
    uow = prepare_app_container.uow()
    sync_service = prepare_app_container.context_sync_container.sync_dingtalk_service()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_sync_dept")
        sync_service.sync_dingtalk_dept_to_master(
            dingtalk_corp_id=dingtalk_corp_id,
            transaction=trans
        )


def test_sync_dingtalk_user(prepare_app_container, prepare_robot):
    uow = prepare_app_container.uow()
    sync_service = prepare_app_container.context_sync_container.sync_dingtalk_service()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_sync_dingtalk_user")
        sync_service.sync_dingtalk_user_to_master(
            dingtalk_corp_id=dingtalk_corp_id, transaction=trans
        )


def test_sync_parent_and_student(prepare_app_container, prepare_robot):
    uow = prepare_app_container.uow()
    sync_service = prepare_app_container.context_sync_container.sync_dingtalk_service()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_sync_parent_and_student")
        sync_service.sync_dingtalk_parent_and_student_to_master(
            dingtalk_corp_id=dingtalk_corp_id,
            transaction=trans
        )


def test_add_student_avatar(prepare_app_container, prepare_robot):
    uow = prepare_app_container.uow()
    with uow:
        trans = uow.log_transaction(
            handler=prepare_robot,
            action="test_add_student_avatar",
            action_params={
                "dingtalk_corp_id": dingtalk_corp_id,
            }
        )
        sync_service = prepare_app_container.context_sync_container.sync_dingtalk_user_service()
        people_repository = prepare_app_container.context_sync_container.context_people_user_map_repository()
        student_list = people_repository.get_no_avatar_student_people()
        student_ids = [x.id for x in student_list]
        sync_service.add_people_default_avatar(
            people_ids=student_ids,
            category=EnumDictMetaCode.STUDENT_DEFAULT_AVATAR.name,
            transaction=trans
        )


def test_add_dept_avatar(prepare_app_container, prepare_robot):
    uow = prepare_app_container.uow()
    with uow:
        trans = uow.log_transaction(
            handler=prepare_robot,
            action="test_add_dept_avatar",
        )
        dept_service = prepare_app_container.context_sync_container.sync_dingtalk_dept_service()
        repo = prepare_app_container.context_sync_container.context_dept_map_repository()
        class_list = repo.get_no_avatar_class_list()
        class_ids = [x.id for x in class_list]
        dept_service.add_dept_default_avatar(
            dept_ids=class_ids,
            transaction=trans
        )
