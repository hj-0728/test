from edu_binshi.data.constant import EduBinShiDictConst
from infra_backbone.model.dict_data_model import EnumValueType
from infra_backbone.model.edit.dict_em import DictMetaEm, DictDataEm
from infra_backbone.service.robot_service import RobotService


def test_init_student_account(prepare_backbone_container):
    uow = prepare_backbone_container.uow()
    robot_service: RobotService = prepare_backbone_container.robot_service()
    dict_service = prepare_backbone_container.dict_service()
    with uow:
        handler = robot_service.get_system_robot().to_basic_handler()
        trans = uow.log_transaction(handler=handler, action="init_student_account")
        # 指定起始日期
        dict_service.save_dict_info(
            dict_info=DictMetaEm(
                name="账号",
                code=EduBinShiDictConst.ACCOUNT,
                dict_data_list=[DictDataEm(
                    name="学生初始账号",
                    code=EduBinShiDictConst.STUDENT_INIT_ACCOUNT,
                    value_type=EnumValueType.STRING.name,
                    value="binshi@12345",
                )]
            ),
            transaction=trans
        )
