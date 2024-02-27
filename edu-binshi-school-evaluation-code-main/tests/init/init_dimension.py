from infra_backbone.model.dept_category_model import DeptCategoryModel
from infra_backbone.model.dimension_model import DimensionModel, EnumDimensionCategory
from infra_backbone.model.organization_model import OrganizationModel, \
    EnumOrganizationCategory
from infra_backbone.repository.dept_category_repository import DeptCategoryRepository
from infra_backbone.repository.dimension_repository import DimensionRepository
from infra_backbone.repository.organization_repository import OrganizationRepository


def test_init_organization(prepare_backbone_container, prepare_robot):
    uow = prepare_backbone_container.uow()
    organization_repository: OrganizationRepository = prepare_backbone_container.organization_repository()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_init_organization")
        org_id = organization_repository.insert_organization(
            data=OrganizationModel(
                name="滨江实验小学",
                code="BJSYXX",
                category=EnumOrganizationCategory.SCHOOL.name,
            ),
            transaction=trans
        )
        print(org_id)


def test_init_dimension(prepare_backbone_container, prepare_robot):
    uow = prepare_backbone_container.uow()
    dimension_repository: DimensionRepository = prepare_backbone_container.dimension_repository()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_init_dimension")
        dimension_repository.insert_dimension(
            data=DimensionModel(
                name="钉钉家校维度",
                code="DINGTALK_EDU",
                category=EnumDimensionCategory.EDU.name,
                organization_id='507eb296-3951-48ee-88e9-febaf10ffe44',
            ),
            transaction=trans
        )


def test_init_dept_category(prepare_backbone_container, prepare_robot):
    uow = prepare_backbone_container.uow()
    dept_category_repository: DeptCategoryRepository = prepare_backbone_container.dept_category_repository()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_init_dept_category")
        dept_category_repository.insert_dept_category(
            data=DeptCategoryModel(
                name="校区",
                code="CAMPUS",
                organization_id='507eb296-3951-48ee-88e9-febaf10ffe44',
            ),
            transaction=trans
        )
        dept_category_repository.insert_dept_category(
            data=DeptCategoryModel(
                name="学段",
                code="PERIOD",
                organization_id='507eb296-3951-48ee-88e9-febaf10ffe44',
            ),
            transaction=trans
        )
        dept_category_repository.insert_dept_category(
            data=DeptCategoryModel(
                name="年级",
                code="GRADE",
                organization_id='507eb296-3951-48ee-88e9-febaf10ffe44',
            ),
            transaction=trans
        )
        dept_category_repository.insert_dept_category(
            data=DeptCategoryModel(
                name="班级",
                code="CLASS",
                organization_id='507eb296-3951-48ee-88e9-febaf10ffe44',
            ),
            transaction=trans
        )
        dept_category_repository.insert_dept_category(
            data=DeptCategoryModel(
                name="普通节点",
                code="DEPT",
                organization_id='507eb296-3951-48ee-88e9-febaf10ffe44',
            ),
            transaction=trans
        )
