from infra_basic.message_carrier import MessageCarrier
from loguru import logger

from domain_evaluation.data.enum import EnumTagOwnerCategory, EnumTagOwnershipRelationship
from domain_evaluation.model.benchmark_strategy_model import BenchmarkStrategyModel, \
    EnumBenchmarkStrategyScoreSymbolScope, EnumBenchmarkStrategySourceCategory

from infra_utility.token_helper import generate_uuid_id

from domain_evaluation.model.edit.load_benchmark_schema_args_em import LoadBenchmarkSchemaArgsEditModel
from infra_backbone.model.edit.save_tag_em import SaveTagEditModel, SaveTagOwnershipRelationshipEditModel
from infra_backbone.model.tag_ownership_relationship_model import \
    TagOwnershipRelationshipModel


def test_insert_benchmark_strategy(prepare_domain_evaluation_container, prepare_robot):
    strategy_repo = prepare_domain_evaluation_container.benchmark_strategy_repository()
    uow = prepare_domain_evaluation_container.uow()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action='test_insert_benchmark_strategy')
        strategy_list = [
            {
                "name": "等级",
                "code": "GRADE",
                "process_params_type": "GradeProcessParamsType",
                "prepare_func": f"prepare_{'grade'}_schema",
                "build_node_func": f"build_{'grade'}_node",
                "score_symbol_scope": EnumBenchmarkStrategyScoreSymbolScope.STRING.name,
            }
        ]
        for strategy in strategy_list:
            strategy_repo.insert_benchmark_strategy(
                benchmark_strategy=BenchmarkStrategyModel(**strategy), transaction=trans
            )


def test_insert_benchmark_strategy_stats(
    prepare_domain_evaluation_container, prepare_robot, prepare_backbone_container
):
    strategy_repo = prepare_domain_evaluation_container.benchmark_strategy_repository()
    tag_repository = prepare_backbone_container.tag_repository()
    uow = prepare_domain_evaluation_container.uow()
    with uow:
        trans = uow.log_transaction(
            handler=prepare_robot,
            action='test_insert_benchmark_strategy_stats'
        )
        strategy = {
            "name": "本级评价项的评价分类相加",
            "code": "SAME_LEVEL_STATS",
            "process_params_type": "StatsProcessParamsType",
            "prepare_func": "prepare_same_level_stats_schema",
            "build_node_func": "build_stats_node",
            "score_symbol_scope": EnumBenchmarkStrategyScoreSymbolScope.NUM.name,
            "source_category": EnumBenchmarkStrategySourceCategory.CALC.name,
        }
        strategy_id = strategy_repo.insert_benchmark_strategy(
            benchmark_strategy=BenchmarkStrategyModel(**strategy), transaction=trans
        )
        tag_repository.insert_tag_ownership_relationship(
            tag_ownership_rel=TagOwnershipRelationshipModel(
                tag_ownership_id="611bc26f-01eb-47a9-bf2c-0c4203e79cfc",
                resource_category="BENCHMARK_STRATEGY",
                resource_id=strategy_id,
                relationship="EVALUATION",
            ),
            transaction=trans,
        )


def test_load_benchmark_strategy(prepare_domain_evaluation_container):
    strategy_service = prepare_domain_evaluation_container.benchmark_strategy_service()
    strategy_list = strategy_service.load_benchmark_strategy_list()
    carrier = MessageCarrier()
    carrier.push_succeed_data(data=strategy_list)
    res = carrier.dict(by_alias=True)
    logger.info(f'strategy_list: \n{res}')


def test_load_benchmark_input_schema(prepare_domain_evaluation_container):
    strategy_service = prepare_domain_evaluation_container.benchmark_strategy_service()
    params = strategy_service.load_benchmark_input_schema(
        load_args=LoadBenchmarkSchemaArgsEditModel(
            strategy_id="d1deac0b-cfa4-4d4d-abf2-c1d80f06991b",
            indicator_id="f2e84d55-40fc-406f-8858-03fa9c21ce20",
            score_symbol_id="0fa555a8-7514-4e3e-aacf-e40f15d14d21"
        )
    )

    carrier = MessageCarrier()
    carrier.push_succeed_data(data=params)
    res = carrier.dict(by_alias=True)
    logger.info(f'strategy_list: \n{res}')


def test_build_benchmark_node(prepare_domain_evaluation_container):
    strategy_service = prepare_domain_evaluation_container.benchmark_strategy_service()
    strategy_service.build_benchmark_node(
        benchmark_id="a6ae520f-803b-4687-8457-be933c1ca046",
        strategy_id="f2e84d55-40fc-406f-8858-03fa9c21ce20",
        params={
            "score_symbol_id": generate_uuid_id(),
            "source_benchmark": [
                {"source_benchmark_id": generate_uuid_id(), "weight": 1, "seq": 1},
                {"source_benchmark_id": generate_uuid_id(), "weight": 9, "seq": 2},
                {"source_benchmark_id": generate_uuid_id(), "weight": 17, "seq": 3},
            ],
        }
    )


def test_insert_benchmark_strategy_tag_relationship(prepare_domain_evaluation_container,prepare_backbone_container, prepare_robot):
    """
    插入策略和tag的关联关系，如果有原来的关联关系先删掉
    """
    strategy_repo = prepare_domain_evaluation_container.benchmark_strategy_repository()
    tag_service = prepare_backbone_container.tag_service()
    uow = prepare_domain_evaluation_container.uow()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action='test_insert_benchmark_strategy_tag_relationship')
        benchmark_strategy_tag_list = [
            # {
            #     "benchmark_strategy_code": 'CLASSMATES_FIXED_NUMBER',
            #     "tag_name": "他评",
            # },
            {
                "benchmark_strategy_code": 'SELF',
                "tag_name": "自评",
            },
            {
                "benchmark_strategy_code": 'ONLY_ONE_TEACHER',
                "tag_name": "他评",
            },
            {
                "benchmark_strategy_code": 'ONLY_ONE_TEAM_CATEGORY',
                "tag_name": "小组评",
            },
            {
                "benchmark_strategy_code": 'ONLY_ONE_HEAD_TEACHER',
                "tag_name": "他评",
            },
            {
                "benchmark_strategy_code": 'SAME_LEVEL_AGGREGATED',
                "tag_name": "综合",
            },
            {
                "benchmark_strategy_code": 'SUB_LEVEL_AGGREGATED',
                "tag_name": "总评",
            },
            {
                "benchmark_strategy_code": 'GRADE',
                "tag_name": "等级",
            },
        ]
        for item in benchmark_strategy_tag_list:
            benchmark_strategy_info = strategy_repo.fetch_benchmark_strategy_by_code(code=item['benchmark_strategy_code'])
            tag_service.save_tag_and_update_related_relationship(
                tag=SaveTagEditModel(
                    name=item['tag_name'],
                    tag_ownership_relationship_list=[
                        SaveTagOwnershipRelationshipEditModel(
                            resource_category=EnumTagOwnerCategory.BENCHMARK_STRATEGY.name,
                            resource_id=benchmark_strategy_info.id,
                            relationship=EnumTagOwnershipRelationship.EVALUATION.name,
                        )
                    ]
                ),
                transaction=trans
            )