from loguru import logger

from domain_evaluation.model.edit.load_filler_em import LoadFillerEditModel


def test_load_filler(prepare_domain_evaluation_container):
    benchmark_manage_service = prepare_domain_evaluation_container.benchmark_manage_service()
    filler_list = benchmark_manage_service.load_benchmark_filler(
        params=LoadFillerEditModel(
            filler_calc_method="SelfBenchmark",
            benchmark_input_node_id="29caf9b6-71cf-4230-bae2-66ac8d9faf37",
            establishment_assign_id="8bde3c74-ea4a-4eef-a1b7-9998616c5cfb",
        )
    )
    logger.info(filler_list)
