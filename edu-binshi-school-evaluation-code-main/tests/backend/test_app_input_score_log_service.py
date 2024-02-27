from backend.model.edit.command_generate_input_score_log_em import CommandGenerateInputScoreLogEditModel, \
    EnumTriggerCategory


def test_handle_generate_input_score_log(prepare_backend_container, prepare_robot):
    uow = prepare_backend_container.uow()
    log_service = prepare_backend_container.app_input_score_log_service()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_handle_generate_input_score_log")
        log_service.handle_generate_input_score_log(
            data=CommandGenerateInputScoreLogEditModel(
                trigger_category=EnumTriggerCategory.CONTEXT_SYNC.name,
                trigger_ids=[],
            ),
            transaction=trans
        )
