from biz_comprehensive.model.symbol_exchange_model import SymbolExchangeModel
from biz_comprehensive.model.symbol_model import SymbolModel, EnumSymbolCategory, EnumSymbolValueType, EnumSymbolCode
from biz_comprehensive.repository.symbol_repository import SymbolRepository
from infra_backbone.service.robot_service import RobotService


def test_init_symbol(prepare_backbone_container, prepare_biz_comprehensive):
    uow = prepare_biz_comprehensive.uow()
    robot_service: RobotService = prepare_backbone_container.robot_service()
    symbol_repository: SymbolRepository = prepare_biz_comprehensive.symbol_repository()
    with uow:
        robot = robot_service.get_system_robot().to_basic_handler()
        transaction = uow.log_transaction(handler=robot, action="test_init_symbol")
        data = SymbolModel(
            name="闪光点",
            code=EnumSymbolCode.BRIGHT_SPOT.name,
            value_type=EnumSymbolValueType.NUM.name,
            numeric_precision=0,
            category=EnumSymbolCategory.BRIGHT_SPOT.name
        )
        symbol_repository.insert_symbol(
            data=data, transaction=transaction
        )


def test_init_symbol_exchange(prepare_backbone_container, prepare_biz_comprehensive):
    uow = prepare_biz_comprehensive.uow()
    robot_service: RobotService = prepare_backbone_container.robot_service()
    symbol_repository: SymbolRepository = prepare_biz_comprehensive.symbol_repository()
    with uow:
        robot = robot_service.get_system_robot().to_basic_handler()
        transaction = uow.log_transaction(handler=robot, action="test_init_symbol_exchange")
        data = SymbolExchangeModel(
            source_symbol_id="851239af-9a87-4252-8f11-2b93c2121e7c",
            target_symbol_id="9c9cef12-f174-4adf-81b0-3858f1d3fdde",
            exchange_rate=625
        )
        symbol_repository.insert_symbol_exchange(
            data=data, transaction=transaction
        )
