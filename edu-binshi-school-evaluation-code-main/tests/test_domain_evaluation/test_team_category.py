from infra_backbone.model.team_category_model import TeamCategoryModel


def test_save_team_category(prepare_domain_evaluation_container, prepare_robot):
    uow = prepare_domain_evaluation_container.uow()
    team_category_repo = prepare_domain_evaluation_container.team_category_repository()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action='test_save_team_category')
        team_category_repo.insert_team_category(
            team_category=TeamCategoryModel(
                name="道德与法治评分组"
            ),
            transaction=trans
        )

