from infra_utility.token_helper import generate_uuid_id, generate_by_host_and_time

from domain_evaluation.model.edit.save_benchmark_em import SaveBenchmarkEditModel


def test_save_benchmark(prepare_domain_evaluation_container, prepare_robot):
    benchmark_service = prepare_domain_evaluation_container.benchmark_service()
    uow = prepare_domain_evaluation_container.uow()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action='test_save_benchmark')
        data = {
            "benchmark": {
                "indicator_id": generate_uuid_id(),
                "name": "测试",
                "guidance": generate_by_host_and_time(),
                "benchmark_strategy_id": "d1deac0b-cfa4-4d4d-abf2-c1d80f06991b",
                "benchmark_strategy_params": {
                    "score_symbol_id": generate_uuid_id(),
                    "input_score_symbol_id": generate_uuid_id(),
                    "source_benchmark_id": generate_uuid_id(),
                    "range_value_args": [
                        {"min_score": 1, "max_score": 3, "left_operator": ">", "right_operator": "<=", "match_value": "A"},
                        {"min_score": 4, "max_score": 7, "left_operator": ">", "right_operator": "<=", "match_value": "B"},
                        {"min_score": 8, "max_score": 10, "left_operator": ">", "right_operator": "<=", "match_value": "C"},
                        {"min_score": 11, "max_score": 16, "left_operator": ">", "right_operator": "<=", "match_value": "D"},
                    ],
                }
            },
            "tag_name": "Ha"
        }
        benchmark_service.save_benchmark(
            data=SaveBenchmarkEditModel(**data), transaction=trans
        )
