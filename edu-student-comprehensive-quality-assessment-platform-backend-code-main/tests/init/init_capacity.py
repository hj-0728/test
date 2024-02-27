from infra_utility.enum_helper import enum_to_dict_list

from infra_backbone.model.capacity_model import EnumCapacityCode, CapacityModel


def test_add_capacity(prepare_backbone_container, prepare_robot):
    uow = prepare_backbone_container.uow()
    repo = prepare_backbone_container.capacity_repository()
    with uow:
        transaction = uow.log_transaction(handler=prepare_robot, action="test_add_capacity")
        capacity_list = enum_to_dict_list(enum_class=EnumCapacityCode, name_col="code", value_col="name")
        for capacity in capacity_list:
            repo.insert_capacity(
                data=CapacityModel(**capacity),
                transaction=transaction
            )
