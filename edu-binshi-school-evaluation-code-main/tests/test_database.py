import domain_evaluation.entity as entities


def test_create_all_tables(prepare_database):
    prepare_database.create_tables(scan_module=entities)
