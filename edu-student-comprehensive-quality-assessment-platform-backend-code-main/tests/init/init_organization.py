import json

from infra_utility.file_helper import build_abs_path_by_file

from context_sync.model.context_organization_corp_map_model import ContextOrganizationCorpMapModel, \
    EnumContextOrgCorpMapResCategory
from infra_backbone.model.dept_category_model import DeptCategoryModel
from infra_backbone.model.dimension_model import DimensionModel, EnumDimensionCategory, EnumDimensionCode
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
                name="建兰小学",
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
                name="K12维度",
                code=EnumDimensionCode.K12.name,
                category=EnumDimensionCategory.EDU.name,
                organization_id='35df32a8-2cbe-4d39-8b1e-cf59afa5fce1',
            ),
            transaction=trans
        )
        dimension_repository.insert_dimension(
            data=DimensionModel(
                name="内部维度",
                code=EnumDimensionCode.INNER.name,
                category=EnumDimensionCategory.ADMINISTRATION.name,
                organization_id='35df32a8-2cbe-4d39-8b1e-cf59afa5fce1',
            ),
            transaction=trans
        )


def test_init_dept_category(prepare_backbone_container, prepare_robot):
    uow = prepare_backbone_container.uow()
    dept_category_repository: DeptCategoryRepository = prepare_backbone_container.dept_category_repository()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_init_dept_category")
        file_path = build_abs_path_by_file(__file__, 'init_json/init_dept_category.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            data_list = json.load(file)
        for data in data_list:
            data['organization_id'] = '35df32a8-2cbe-4d39-8b1e-cf59afa5fce1'
            dept_category_repository.insert_dept_category(
                data=DeptCategoryModel(**data),
                transaction=trans
            )


def test_init_context_organization_corp_map(prepare_app_container, prepare_robot):
    uow = prepare_app_container.uow()
    repo = prepare_app_container.context_sync_container.context_org_corp_map_repository()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_init_context_organization_corp_map")
        repo.insert_context_organization_corp_map(
            context_org_corp_map=ContextOrganizationCorpMapModel(
                organization_id='35df32a8-2cbe-4d39-8b1e-cf59afa5fce1',
                res_category=EnumContextOrgCorpMapResCategory.DINGTALK.name,
                res_id="b51e6648-7947-4969-8c1f-52051ecb5673"
            ),
            transaction=trans
        )
