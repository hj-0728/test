from dependency_injector import containers, providers
from infra_basic.redis_manager import RedisManager
from infra_basic.sqlalchemy_uow import SqlAlchemyUnitOfWork

from infra_backbone.repository.ability_permission_assign_repository import (
    AbilityPermissionAssignRepository,
)
from infra_backbone.repository.ability_permission_group_repository import (
    AbilityPermissionGroupRepository,
)
from infra_backbone.repository.ability_permission_repository import AbilityPermissionRepository
from infra_backbone.repository.ability_permission_tree_repository import (
    AbilityPermissionTreeRepository,
)
from infra_backbone.repository.access_log_repository import AccessLogRepository
from infra_backbone.repository.address_repository import AddressRepository
from infra_backbone.repository.area_repsoitory import AreaRepository
from infra_backbone.repository.capacity_repository import CapacityRepository
from infra_backbone.repository.contact_info_repository import ContactInfoRepository
from infra_backbone.repository.data_permission_repository import DataPermissionRepository
from infra_backbone.repository.dept_capacity_constraint_repository import (
    DeptCapacityConstraintRepository,
)
from infra_backbone.repository.dept_category_capacity_constraint_repository import (
    DeptCategoryCapacityConstraintRepository,
)
from infra_backbone.repository.dept_category_repository import DeptCategoryRepository
from infra_backbone.repository.dept_dept_category_map_repository import (
    DeptDeptCategoryMapRepository,
)
from infra_backbone.repository.dept_repository import DeptRepository
from infra_backbone.repository.dict_repository import DictRepository
from infra_backbone.repository.dimension_dept_tree_repository import DimensionDeptTreeRepository
from infra_backbone.repository.dimension_repository import DimensionRepository
from infra_backbone.repository.establishment_assign_repository import EstablishmentAssignRepository
from infra_backbone.repository.establishment_repository import EstablishmentRepository
from infra_backbone.repository.identity_number_repository import IdentityNumberRepository
from infra_backbone.repository.menu_repository import MenuRepository
from infra_backbone.repository.organization_repository import OrganizationRepository
from infra_backbone.repository.people_relationship_repository import PeopleRelationshipRepository
from infra_backbone.repository.people_repository import PeopleRepository
from infra_backbone.repository.people_user_repository import PeopleUserRepository
from infra_backbone.repository.position_repository import PositionRepository
from infra_backbone.repository.resource_contact_info_repository import ResourceContactInfoRepository
from infra_backbone.repository.robot_repository import RobotRepository
from infra_backbone.repository.role_repository import RoleRepository
from infra_backbone.repository.route_repository import RouteRepository
from infra_backbone.repository.scheduler_job_repository import SchedulerJobRepository
from infra_backbone.repository.site_message_context_repository import SiteMessageContextRepository
from infra_backbone.repository.site_message_repository import SiteMessageRepository
from infra_backbone.repository.tag_repository import TagRepository
from infra_backbone.repository.team_category_repository import TeamCategoryRepository
from infra_backbone.repository.team_goal_repository import TeamGoalRepository
from infra_backbone.repository.team_member_repository import TeamMemberRepository
from infra_backbone.repository.team_repository import TeamRepository
from infra_backbone.repository.user_repository import UserRepository
from infra_backbone.repository.user_role_repository import UserRoleRepository
from infra_backbone.service.ability_permission_service import AbilityPermissionService
from infra_backbone.service.access_log_service import AccessLogService
from infra_backbone.service.address_service import AddressService
from infra_backbone.service.area_service import AreaService
from infra_backbone.service.contact_info_service import ContactInfoService
from infra_backbone.service.data_permission_service import DataPermissionService
from infra_backbone.service.dept_category_service import DeptCategoryService
from infra_backbone.service.dept_dept_category_map_service import DeptDeptCategoryMapService
from infra_backbone.service.dept_service import DeptService
from infra_backbone.service.dict_service import DictService
from infra_backbone.service.dimension_dept_tree_service import DimensionDeptTreeService
from infra_backbone.service.dimension_service import DimensionService
from infra_backbone.service.establishment_assign_service import EstablishmentAssignService
from infra_backbone.service.establishment_service import EstablishmentService
from infra_backbone.service.menu_service import MenuService
from infra_backbone.service.organization_service import OrganizationService
from infra_backbone.service.people_service import PeopleService
from infra_backbone.service.robot_service import RobotService
from infra_backbone.service.role_service import RoleService
from infra_backbone.service.route_service import RouteService
from infra_backbone.service.scheduler_job_service import SchedulerJobsService
from infra_backbone.service.site_message_service import SiteMessageService
from infra_backbone.service.tag_service import TagService
from infra_backbone.service.team_category_service import TeamCategoryService
from infra_backbone.service.team_goal_service import TeamGoalService
from infra_backbone.service.team_member_service import TeamMemberService
from infra_backbone.service.team_service import TeamService
from infra_backbone.service.user_role_service import UserRoleService
from infra_backbone.service.user_service import UserService


class BackboneContainer(containers.DeclarativeContainer):
    uow = providers.Dependency(instance_of=SqlAlchemyUnitOfWork)  # type: ignore
    redis_manager = providers.ThreadLocalSingleton(RedisManager)  # type: ignore

    dict_repository = providers.ThreadLocalSingleton(DictRepository, db_session=uow.provided.db_session)  # type: ignore

    robot_repository = providers.ThreadLocalSingleton(
        RobotRepository, db_session=uow.provided.db_session
    )  # type: ignore

    user_repository = providers.ThreadLocalSingleton(UserRepository, db_session=uow.provided.db_session)  # type: ignore

    people_user_repository = providers.ThreadLocalSingleton(
        PeopleUserRepository, db_session=uow.provided.db_session
    )  # type: ignore

    address_repository = providers.ThreadLocalSingleton(
        AddressRepository, db_session=uow.provided.db_session
    )  # type: ignore

    area_repository = providers.ThreadLocalSingleton(AreaRepository, db_session=uow.provided.db_session)  # type: ignore

    data_permission_repository = providers.ThreadLocalSingleton(
        DataPermissionRepository, db_session=uow.provided.db_session
    )  # type: ignore

    role_repository = providers.ThreadLocalSingleton(RoleRepository, db_session=uow.provided.db_session)  # type: ignore

    menu_repository = providers.ThreadLocalSingleton(MenuRepository, db_session=uow.provided.db_session)  # type: ignore

    people_repository = providers.ThreadLocalSingleton(  # type: ignore
        PeopleRepository, db_session=uow.provided.db_session
    )

    organization_repository = providers.ThreadLocalSingleton(
        OrganizationRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dimension_repository = providers.ThreadLocalSingleton(
        DimensionRepository, db_session=uow.provided.db_session
    )  # type: ignore

    dept_repository = providers.ThreadLocalSingleton(DeptRepository, db_session=uow.provided.db_session)  # type: ignore

    dimension_dept_tree_repository = providers.ThreadLocalSingleton(
        DimensionDeptTreeRepository, db_session=uow.provided.db_session
    )  # type: ignore

    position_repository = providers.ThreadLocalSingleton(
        PositionRepository, db_session=uow.provided.db_session
    )  # type: ignore

    establishment_repository = providers.ThreadLocalSingleton(
        EstablishmentRepository, db_session=uow.provided.db_session
    )  # type: ignore

    contact_info_repository = providers.ThreadLocalSingleton(
        ContactInfoRepository, db_session=uow.provided.db_session
    )  # type: ignore

    resource_contact_info_repository = providers.ThreadLocalSingleton(
        ResourceContactInfoRepository, db_session=uow.provided.db_session
    )  # type: ignore

    identity_number_repository = providers.ThreadLocalSingleton(
        IdentityNumberRepository, db_session=uow.provided.db_session
    )  # type: ignore

    site_message_repository = providers.ThreadLocalSingleton(
        SiteMessageRepository, db_session=uow.provided.db_session
    )  # type: ignore

    site_message_context_repository = providers.ThreadLocalSingleton(
        SiteMessageContextRepository, db_session=uow.provided.db_session
    )  # type: ignore

    route_repository = providers.ThreadLocalSingleton(
        RouteRepository, db_session=uow.provided.db_session
    )  # type: ignore

    user_role_repository = providers.ThreadLocalSingleton(
        UserRoleRepository, db_session=uow.provided.db_session
    )  # type: ignore

    access_log_repository = providers.ThreadLocalSingleton(
        AccessLogRepository, db_session=uow.provided.db_session
    )  # type: ignore

    scheduler_job_repository = providers.ThreadLocalSingleton(  # type: ignore
        SchedulerJobRepository, db_session=uow.provided.db_session
    )

    dept_category_repository = providers.ThreadLocalSingleton(  # type: ignore
        DeptCategoryRepository, db_session=uow.provided.db_session
    )

    dept_dept_category_map_repository = providers.ThreadLocalSingleton(  # type: ignore
        DeptDeptCategoryMapRepository, db_session=uow.provided.db_session
    )

    people_relationship_repository = providers.ThreadLocalSingleton(  # type: ignore
        PeopleRelationshipRepository, db_session=uow.provided.db_session
    )

    capacity_repository = providers.ThreadLocalSingleton(  # type: ignore
        CapacityRepository, db_session=uow.provided.db_session
    )

    establishment_assign_repository = providers.ThreadLocalSingleton(  # type: ignore
        EstablishmentAssignRepository, db_session=uow.provided.db_session
    )

    team_member_repository = providers.ThreadLocalSingleton(  # type: ignore
        TeamMemberRepository, db_session=uow.provided.db_session
    )

    team_goal_repository = providers.ThreadLocalSingleton(
        TeamGoalRepository, db_session=uow.provided.db_session
    )  # type: ignore

    robot_service = providers.ThreadLocalSingleton(RobotService, robot_repository=robot_repository)  # type: ignore

    user_service = providers.ThreadLocalSingleton(
        UserService,
        user_repository=user_repository,
        role_repository=role_repository,
        user_role_repository=user_role_repository,
        people_user_repository=people_user_repository,
    )  # type: ignore

    address_service = providers.ThreadLocalSingleton(
        AddressService,
        address_repository=address_repository,
    )  # type: ignore

    area_service = providers.ThreadLocalSingleton(
        AreaService,
        area_repository=area_repository,
    )  # type: ignore

    data_permission_service = providers.Factory(
        DataPermissionService,
        data_permission_repository=data_permission_repository,
    )  # type: ignore

    menu_service = providers.ThreadLocalSingleton(MenuService, menu_repository=menu_repository)  # type: ignore

    establishment_service = providers.ThreadLocalSingleton(
        EstablishmentService,
        establishment_repository=establishment_repository,
        capacity_repository=capacity_repository,
    )  # type: ignore

    contact_info_service = providers.ThreadLocalSingleton(
        ContactInfoService,
        contact_info_repository=contact_info_repository,
        resource_contact_info_repository=resource_contact_info_repository,
    )  # type: ignore

    dept_category_service = providers.ThreadLocalSingleton(
        DeptCategoryService,
        dept_category_repository=dept_category_repository,
    )  # type: ignore

    dept_dept_category_map_service = providers.ThreadLocalSingleton(
        DeptDeptCategoryMapService,
        dept_dept_category_map_repository=dept_dept_category_map_repository,
        dept_category_service=dept_category_service,
    )  # type: ignore

    dimension_dept_tree_service = providers.ThreadLocalSingleton(
        DimensionDeptTreeService,
        dept_repository=dept_repository,
        dimension_dept_tree_repository=dimension_dept_tree_repository,
        dimension_repository=dimension_repository,
    )  # type: ignore

    dimension_service = providers.ThreadLocalSingleton(
        DimensionService,
        dimension_repository=dimension_repository,
        organization_repository=organization_repository,
    )  # type: ignore

    establishment_assign_service = providers.ThreadLocalSingleton(
        EstablishmentAssignService,
        establishment_assign_repository=establishment_assign_repository,
        establishment_service=establishment_service,
        dimension_dept_tree_service=dimension_dept_tree_service,
    )  # type: ignore

    people_service = providers.ThreadLocalSingleton(
        PeopleService,
        people_repository=people_repository,
        identity_number_repository=identity_number_repository,
        resource_contact_info_repository=resource_contact_info_repository,
        position_repository=position_repository,
        people_relationship_repository=people_relationship_repository,
        establishment_assign_service=establishment_assign_service,
        dimension_service=dimension_service,
        contact_info_service=contact_info_service,
    )  # type: ignore

    organization_service = providers.ThreadLocalSingleton(
        OrganizationService,
        area_service=area_service,
        organization_repository=organization_repository,
    )  # type: ignore

    dept_service = providers.ThreadLocalSingleton(
        DeptService,
        dept_repository=dept_repository,
        dimension_dept_tree_repository=dimension_dept_tree_repository,
        people_service=people_service,
        establishment_service=establishment_service,
        position_repository=position_repository,
        dimension_repository=dimension_repository,
        dept_dept_category_map_service=dept_dept_category_map_service,
        organization_service=organization_service,
        dimension_service=dimension_service,
    )  # type: ignore

    role_service = providers.ThreadLocalSingleton(
        RoleService,
        role_repository=role_repository,
    )  # type: ignore

    site_message_service = providers.ThreadLocalSingleton(
        SiteMessageService,
        site_message_repository=site_message_repository,
        site_message_context_repository=site_message_context_repository,
    )  # type: ignore

    ability_permission_repository = providers.ThreadLocalSingleton(  # type: ignore
        AbilityPermissionRepository, db_session=uow.provided.db_session
    )

    ability_permission_group_repository = providers.ThreadLocalSingleton(  # type: ignore
        AbilityPermissionGroupRepository, db_session=uow.provided.db_session
    )

    ability_permission_tree_repository = providers.ThreadLocalSingleton(  # type: ignore
        AbilityPermissionTreeRepository, db_session=uow.provided.db_session
    )
    ability_permission_assign_repository = providers.ThreadLocalSingleton(  # type: ignore
        AbilityPermissionAssignRepository, db_session=uow.provided.db_session
    )

    dept_capacity_constraint_repository = providers.ThreadLocalSingleton(  # type: ignore
        DeptCapacityConstraintRepository, db_session=uow.provided.db_session
    )

    dept_category_capacity_constraint_repository = providers.ThreadLocalSingleton(  # type: ignore
        DeptCategoryCapacityConstraintRepository, db_session=uow.provided.db_session
    )

    tag_repository = providers.ThreadLocalSingleton(
        TagRepository, db_session=uow.provided.db_session
    )

    ability_permission_service = providers.ThreadLocalSingleton(
        AbilityPermissionService,
        ability_permission_repository=ability_permission_repository,
        ability_permission_group_repository=ability_permission_group_repository,
        ability_permission_tree_repository=ability_permission_tree_repository,
        ability_permission_assign_repository=ability_permission_assign_repository,
    )  # type: ignore

    route_service = providers.ThreadLocalSingleton(
        RouteService,
        route_repository=route_repository,
    )  # type: ignore

    user_role_service = providers.ThreadLocalSingleton(
        UserRoleService, user_role_repository=user_role_repository
    )  # type: ignore

    access_log_service = providers.ThreadLocalSingleton(
        AccessLogService, access_log_repository=access_log_repository
    )  # type: ignore

    dict_service = providers.ThreadLocalSingleton(DictService, dict_repository=dict_repository)  # type: ignore

    scheduler_job_service = providers.ThreadLocalSingleton(
        SchedulerJobsService,
        scheduler_job_repository=scheduler_job_repository,
    )  # type: ignore

    team_category_repository = providers.ThreadLocalSingleton(
        TeamCategoryRepository, db_session=uow.provided.db_session
    )  # type: ignore

    team_category_service = providers.ThreadLocalSingleton(
        TeamCategoryService,
        team_category_repository=team_category_repository,
    )  # type: ignore

    team_repository = providers.ThreadLocalSingleton(
        TeamRepository, db_session=uow.provided.db_session
    )  # type: ignore

    team_member_service = providers.ThreadLocalSingleton(
        TeamMemberService,
        team_member_repository=team_member_repository,
        team_repository=team_repository,
        team_category_service=team_category_service,
    )  # type: ignore

    team_goal_service = providers.ThreadLocalSingleton(
        TeamGoalService,
        team_goal_repository=team_goal_repository,
        dimension_dept_tree_repository=dimension_dept_tree_repository,
        dimension_repository=dimension_repository,
        dept_dept_category_map_service=dept_dept_category_map_service,
        organization_service=organization_service,
        dimension_service=dimension_service,
        dept_repository=dept_repository,
        position_repository=position_repository,
    )  # type: ignore

    team_service = providers.ThreadLocalSingleton(
        TeamService,
        team_repository=team_repository,
        team_goal_service=team_goal_service,
        team_category_service=team_category_service
    )  # type: ignore

    tag_service = providers.ThreadLocalSingleton(
        TagService,
        tag_repository=tag_repository,
    )  # type: ignore
