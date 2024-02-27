import json

from infra_basic.basic_resource import BasicResource

from infra_backbone.model.ability_permission_assign_model import \
    EnumAbilityPermissionAssignResourceCategory
from infra_backbone.model.edit.ability_permission_em import AbilityPermissionEditModel
from infra_backbone.model.edit.granted_ability_permission_em import \
    AbilityPermissionAssignEm
from infra_backbone.model.menu_model import MenuModel
from infra_backbone.model.role_model import RoleModel
from infra_backbone.model.user_model import UserModel
from infra_backbone.repository.ability_permission_repository import \
    AbilityPermissionRepository
from infra_backbone.repository.role_repository import RoleRepository
from infra_backbone.service.ability_permission_service import AbilityPermissionService
from infra_backbone.service.robot_service import RobotService
from infra_backbone.service.user_service import UserService
from infra_utility.file_helper import build_abs_path_by_file


def test_init_robot(prepare_app_container):
    uow = prepare_app_container.backbone_container.uow()
    robot_service: RobotService = prepare_app_container.backbone_container.robot_service()
    with uow:
        handler = BasicResource(id="SYSTEM", category="SYSTEM")
        trans = uow.log_transaction(handler=handler, action="test_init_robot")
        robot_service.prepare_system_robot(trans=trans)


def test_init_ability_permission(prepare_backbone_container, prepare_handler):
    """
    初始化功能权限
    :param prepare_backbone_container:
    :param prepare_handler:
    :return:
    """
    uow = prepare_backbone_container.uow()
    ability_permission_service: AbilityPermissionService = prepare_backbone_container.ability_permission_service()
    with uow:
        transaction = uow.log_transaction(
            handler=prepare_handler, action="test_init_ability_permission"
        )
        file_path = build_abs_path_by_file(__file__, 'init_json/init_ability_permission.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            data_list = json.load(file)
        for data in data_list:
            ability_permission_service.create_ability_permission(
                ability_permission_em=AbilityPermissionEditModel(**data),
                transaction=transaction
            )


def test_init_role(prepare_backbone_container, prepare_handler):
    uow = prepare_backbone_container.uow()
    role_repository: RoleRepository = prepare_backbone_container.role_repository()
    ability_permission_service: AbilityPermissionService = prepare_backbone_container.ability_permission_service()
    ability_permission_repository: AbilityPermissionRepository = prepare_backbone_container.ability_permission_repository()
    with uow:
        transaction = uow.log_transaction(handler=prepare_handler, action="test_init_role")
        system_admin_role_id = role_repository.insert_role(
            data=RoleModel(
                name='系统管理员',
                code='SYSTEM_ADMIN',
                comments=None,
            ),
            transaction=transaction
        )
        admin_role_id = role_repository.insert_role(
            data=RoleModel(
                name='学校管理员',
                code='SCHOOL_ADMIN',
                comments=None,
            ),
            transaction=transaction
        )
        role_id_list = [system_admin_role_id, admin_role_id]
        ability_permission_list = ability_permission_repository.get_ability_permission()
        ability_permission_id_list = [x.id for x in ability_permission_list]

        for role_id in role_id_list:
            ability_permission_service.save_ability_permission_assign(
                ability_permission_assign_em=AbilityPermissionAssignEm(
                    assign_resource_category=EnumAbilityPermissionAssignResourceCategory.ROLE.name,
                    assign_resource_id=role_id,
                    ability_permission_id_list=ability_permission_id_list,
                ),
                transaction=transaction
            )


def test_init_user(
    prepare_backbone_container, prepare_handler
):
    """
    初始化用户
    :return:
    """
    uow = prepare_backbone_container.uow()
    user_service: UserService = prepare_backbone_container.user_service()
    role_repository: RoleRepository = prepare_backbone_container.role_repository()
    with uow:
        transaction = uow.log_transaction(
            handler=prepare_handler, action="test_init_user"
        )
        system_admin_role = role_repository.get_role_by_code(code='SYSTEM_ADMIN')
        admin_role = role_repository.get_role_by_code(code='SCHOOL_ADMIN')
        role_id_list = [system_admin_role.id, admin_role.id]
        user_service.add_user(
            user=UserModel(
                name="admin",
                password="admin@123456",
                password_reset=True,
                role_id_list=role_id_list,
            ),
            transaction=transaction
        )


def test_init_menu(prepare_backbone_container, prepare_handler):
    """

    :param prepare_backbone_container:
    :param prepare_handler:
    :return:
    """
    uow = prepare_backbone_container.uow()
    menu_service = prepare_backbone_container.menu_service()
    with uow:
        transaction = uow.log_transaction(
            handler=prepare_handler, action="test_init_menu"
        )
        file_path = build_abs_path_by_file(__file__, 'init_json/init_menu.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            data_list = json.load(file)
        for data in data_list:
            menu_service.add_menu(
                menu=MenuModel(**data),
                transaction=transaction
            )
