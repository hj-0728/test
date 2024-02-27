import json

from infra_utility.file_helper import build_abs_path_by_file

from infra_backbone.model.edit.dict_em import DictMetaEm


def test_init_dict_meta(prepare_backbone_container, prepare_robot):
    uow = prepare_backbone_container.uow()
    dict_service = prepare_backbone_container.dict_service()
    with uow:
        transaction = uow.log_transaction(
            handler=prepare_robot, action="init_system_observation_point_icon_dict"
        )
        file_path = build_abs_path_by_file(__file__, 'init_json/init_dict_meta.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            data_list = json.load(file)
        for data in data_list:
            dict_service.save_dict_info(
                dict_info=DictMetaEm(**data), transaction=transaction
            )
