from infra_utility.datetime_helper import local_now

from domain_evaluation.model.evaluation_criteria_plan_scope_model import EvaluationCriteriaPlanScopeModel, \
    EnumGroupCategory


def test_save_evaluation_assignment(prepare_backend_container, prepare_robot):
    uow = prepare_backend_container.uow()
    app_evaluation_assignment_service = prepare_backend_container.app_evaluation_assignment_service()
    with uow:
        transaction = uow.log_transaction(handler=prepare_robot, action='test_save_evaluation_assignment')

        evaluation_criteria_plan_scope_list = [
            EvaluationCriteriaPlanScopeModel(
                evaluation_criteria_plan_id='3ae9b2d6-6d67-4bda-ae14-ba7b9b8684b3',
                scope_category=EnumGroupCategory.PERSONAL.name,
                scope_id='a26c5e99-582c-4f46-8ee4-0d4a1856f593',
                start_at=local_now(),
            ),
            EvaluationCriteriaPlanScopeModel(
                evaluation_criteria_plan_id='3ae9b2d6-6d67-4bda-ae14-ba7b9b8684b3',
                scope_category=EnumGroupCategory.PERSONAL.name,
                scope_id='d845ad37-43f1-4f72-b682-5289fba66a6b',
                start_at=local_now(),
            )
        ]
        app_evaluation_assignment_service.save_evaluation_assignment_relationship(
            evaluation_criteria_plan_id='3ae9b2d6-6d67-4bda-ae14-ba7b9b8684b3',
            evaluation_criteria_plan_scope_list=evaluation_criteria_plan_scope_list,
            transaction=transaction
        )
