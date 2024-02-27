from infra_basic.basic_resource import BasicResource

from infra_backbone.model.ability_permission_assign_model import \
    EnumAbilityPermissionAssignResourceCategory
from infra_backbone.model.edit.ability_permission_em import AbilityPermissionEditModel
from infra_backbone.model.edit.granted_ability_permission_em import \
    AbilityPermissionAssignEm
from infra_backbone.model.menu_model import MenuModel, EnumMenuCategory
from infra_backbone.model.role_model import RoleModel
from infra_backbone.model.user_model import UserModel
from infra_backbone.repository.ability_permission_repository import \
    AbilityPermissionRepository
from infra_backbone.repository.role_repository import RoleRepository
from infra_backbone.service.ability_permission_service import AbilityPermissionService
from infra_backbone.service.robot_service import RobotService
from infra_backbone.service.user_service import UserService


def test_init_robot(prepare_backbone_container):
    uow = prepare_backbone_container.uow()
    robot_service: RobotService = prepare_backbone_container.robot_service()
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
        user_ability_permission_id = ability_permission_service.create_ability_permission(
            ability_permission_em=AbilityPermissionEditModel(
                name='用户管理',
                code='USER_MANAGEMENT_GROUP',
                is_permission=False,
                seq=1,
            ),
            transaction=transaction,
        )
        system_ability_permission_id = ability_permission_service.create_ability_permission(
            ability_permission_em=AbilityPermissionEditModel(
                name='系统管理',
                code='SYSTEM_MANAGEMENT',
                is_permission=False,
                seq=2,
            ),
            transaction=transaction,
        )
        ability_permission_service.create_ability_permission(
            ability_permission_em=AbilityPermissionEditModel(
                name='用户管理',
                code='USER_MANAGEMENT',
                parent_id=user_ability_permission_id,
                is_permission=True,
                seq=1,
            ),
            transaction=transaction,
        )
        ability_permission_service.create_ability_permission(
            ability_permission_em=AbilityPermissionEditModel(
                name='角色管理',
                code='ROLE_MANAGEMENT',
                parent_id=system_ability_permission_id,
                is_permission=True,
                seq=1,
            ),
            transaction=transaction,
        )
        ability_permission_service.create_ability_permission(
            ability_permission_em=AbilityPermissionEditModel(
                name='菜单管理',
                code='MENU_MANAGEMENT',
                parent_id=system_ability_permission_id,
                is_permission=True,
                seq=2,
            ),
            transaction=transaction,
        )
        ability_permission_service.create_ability_permission(
            ability_permission_em=AbilityPermissionEditModel(
                name='路由管理',
                code='ROUTE_MANAGE',
                parent_id=system_ability_permission_id,
                is_permission=True,
                seq=3,
            ),
            transaction=transaction,
        )
        ability_permission_service.create_ability_permission(
            ability_permission_em=AbilityPermissionEditModel(
                name='功能权限',
                code='FUNCTIONAL_PERMISSIONS',
                parent_id=system_ability_permission_id,
                is_permission=True,
                seq=4,
            ),
            transaction=transaction,
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
                name='管理员',
                code='ADMIN',
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
        admin_role = role_repository.get_role_by_code(code='ADMIN')
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
    ability_permission_service: AbilityPermissionService = prepare_backbone_container.ability_permission_service()
    ability_permission_repository: AbilityPermissionRepository = prepare_backbone_container.ability_permission_repository()
    with uow:
        transaction = uow.log_transaction(
            handler=prepare_handler, action="test_init_menu"
        )
        user_menu_id = menu_service.add_menu(
            menu=MenuModel(
                name="用户管理",
                path="/user/list",
                icon="material-symbols:manage-accounts-outline",
                category=EnumMenuCategory.WEB.name,
                seq=1,
            ),
            transaction=transaction
        )
        system_menu_id = menu_service.add_menu(
            menu=MenuModel(
                name="系统管理",
                path="#",
                icon="mdi:file-tree-outline",
                category=EnumMenuCategory.WEB.name,
                seq=2,
            ),
            transaction=transaction
        )
        role_menu_id = menu_service.add_menu(
            menu=MenuModel(
                name="角色管理",
                path="/role/list",
                parent_id=system_menu_id,
                icon="ph:chalkboard-teacher-fill",
                category=EnumMenuCategory.WEB.name,
                seq=1,
            ),
            transaction=transaction
        )
        ability_permission_menu_id = menu_service.add_menu(
            menu=MenuModel(
                name="功能权限",
                path="/ability-permission/tree",
                parent_id=system_menu_id,
                icon="icon-park-outline:permissions",
                category=EnumMenuCategory.WEB.name,
                seq=2,
            ),
            transaction=transaction
        )
        route_menu_id = menu_service.add_menu(
            menu=MenuModel(
                name="路由管理",
                path="/route/list",
                icon="ion:git-compare",
                parent_id=system_menu_id,
                category=EnumMenuCategory.WEB.name,
                seq=3,
            ),
            transaction=transaction
        )
        menu_menu_id = menu_service.add_menu(
            menu=MenuModel(
                name="菜单管理",
                path="/menu/tree",
                icon="ant-design:menu-outlined",
                parent_id=system_menu_id,
                category=EnumMenuCategory.WEB.name,
                seq=4,
            ),
            transaction=transaction
        )

