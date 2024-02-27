from datetime import datetime
from time import time

from infra_basic.basic_resource import BasicResource

from domain_evaluation.model.benchmark_score_model import BenchmarkScoreModel
from domain_evaluation.model.evaluation_assignment_model import EvaluationAssignmentModel
from domain_evaluation.model.evaluation_criteria_plan_scope_model import (
    EvaluationCriteriaPlanScopeModel,
)
from edu_binshi.model.report_model import EnumReportCategory
from edu_binshi.model.report_record_model import (
    DimensionDeptTreeReportModel,
    EnumReportTargetCategory,
)
from infra_backbone.model.establishment_assign_model import EstablishmentAssignModel
from infra_backbone.model.tag_info_model import TagInfoModel
from infra_backbone.model.tag_ownership_model import TagOwnershipModel
from infra_backbone.model.tag_ownership_relationship_model import TagOwnershipRelationshipModel
from infra_backbone.service.robot_service import RobotService


def test_generate_report(prepare_edu_evaluation_container, prepare_robot):
    uow = prepare_edu_evaluation_container.uow()
    report_service = prepare_edu_evaluation_container.report_service()
    with uow:
        start_time = time()
        transaction = uow.log_transaction(handler=prepare_robot, action="test_generate_report")
        print()
        print("start ...")
        # args = ReportArgsBasicModel(
        #     report_category=EnumReportCategory.GROWTH_RECORD.name,
        #     target_category=EnumReportTargetCategory.ESTABLISHMENT_ASSIGN.name,
        #     target_id='265d4898-a0bc-43a1-b226-83a678131cd6',
        #     evaluation_criteria_plan_id='79024eaf-1226-4cd5-b942-e53b80096d00',
        # )
        args = DimensionDeptTreeReportModel(
            report_category=EnumReportCategory.GROWTH_RECORD.name,
            target_category=EnumReportTargetCategory.DIMENSION_DEPT_TREE.name,
            target_id="548da5ea-4242-446a-aef6-ffec2314cc3a",
            evaluation_criteria_plan_id="79024eaf-1226-4cd5-b942-e53b80096d00",
            current_role_code="TEACHER",
            current_people_id="7b767e80-41a4-42cb-a619-075c7f39455b",
        )
        file_url_list = report_service.generate_report(
            args=args,
            transaction=transaction,
        )
        end_time = time()
        print("time: ", end_time - start_time)
        print("file_url_list ...")
        print(file_url_list)


def test_get_file_url(prepare_edu_evaluation_container):
    object_storage_service = (
        prepare_edu_evaluation_container.object_storage_container.object_storage_service()
    )
    url = object_storage_service.get_file_url(file_id="8840bcb2-5aee-4a4c-a785-5e8806c73357")
    print(url)


def test_upload_file(prepare_edu_evaluation_container, prepare_robot):
    uow = prepare_edu_evaluation_container.uow()
    object_storage_service = (
        prepare_edu_evaluation_container.object_storage_container.object_storage_service()
    )
    with uow:
        data_list = [
            {"id": "0fa555a8-7514-4e3e-aacf-e40f15d14d21", "icon_name": "Star.png", "name": "星"},
            {
                "id": "6fb11451-e0b4-434a-bab7-1b801234f1d9",
                "icon_name": "gold (3).png",
                "name": "等级",
            },
            {"id": "f93ce594-314c-4680-bda1-8ab88e13c934", "icon_name": "LEVEL.png", "name": "等级"},
            {
                "id": "9926a210-bbaf-4d10-85f7-a4bbe85d0ae3",
                "icon_name": "sticker-pink66.png",
                "name": "贴纸",
            },
        ]
        for data in data_list:
            with open(r"D:\zb\download\\" + data.get("icon_name"), "rb") as f:
                file_blob = f.read()
            transaction = uow.log_transaction(handler=prepare_robot, action="test_upload_file")
            file_id = object_storage_service.upload_file_with_resource(
                file_name="tree.png",
                file_blob=file_blob,
                resource=BasicResource(id=data.get("id"), category="SCORE_SYMBOL"),
                relationship="ICON",
                transaction=transaction,
            )
            print(file_id)


def test_add_tag(prepare_robot, prepare_backbone_container):
    uow = prepare_backbone_container.uow()
    tag_repository = prepare_backbone_container.tag_repository()
    with uow:
        transaction = uow.log_transaction(handler=prepare_robot, action="test_add_tag")
        tag_repository.insert_tag_info(
            tag=TagInfoModel(name="等级"),
            transaction=transaction,
        )


def test_add_tag_ownership(prepare_robot, prepare_backbone_container):
    uow = prepare_backbone_container.uow()
    tag_repository = prepare_backbone_container.tag_repository()
    with uow:
        transaction = uow.log_transaction(handler=prepare_robot, action="test_add_tag_ownership")
        tag_repository.insert_tag_ownership(
            tag_ownership=TagOwnershipModel(
                tag_id="98ecabdb-a4cf-4c33-bfd2-8c09dd5ae916",
                owner_category="ROBOT",
                owner_id="1273fbb4-66b3-4b60-a61f-f31ed7de9ee0",
            ),
            transaction=transaction,
        )


def test_add_tag_ownership_relationship(prepare_backbone_container):
    uow = prepare_backbone_container.uow()
    robot_service: RobotService = prepare_backbone_container.robot_service()
    tag_repository = prepare_backbone_container.tag_repository()
    with uow:
        handler = robot_service.get_system_robot().to_basic_handler()
        trans = uow.log_transaction(handler=handler, action="test_add_tag_ownership_relationship")
        tree_id_list = [
            "aff4a3e8-226e-4f09-b460-645d85451cf8",
            "5c9e07ef-2eb9-4c50-92da-b92425843596",
            "d2fb5a92-e552-4e15-81e8-a00ae6db5002",
        ]
        for tree_id in tree_id_list:
            tag_repository.insert_tag_ownership_relationship(
                tag_ownership_rel=TagOwnershipRelationshipModel(
                    tag_ownership_id="6d8722b0-0ce6-4f33-ba7a-ad57f2f40a4c",
                    resource_category="EVALUATION_CRITERIA_TREE",
                    resource_id=tree_id,
                    relationship="REPORT",
                ),
                transaction=trans,
            )

        # const_evaluation_criteria_tree_id_list = [
        #     '5c9e07ef-2eb9-4c50-92da-b92425843596',
        #     'c4fbe989-0555-4261-9e13-2afce4e22108',
        #     'b88e5ae2-affa-4cbb-8588-6ee0d2c8a5d1',
        #     '7097e40a-70d5-4813-9acf-da6a6f49a6e1',
        #     '7a186408-fa29-4e7d-8721-6e436cabe8f6',
        #     '54730494-5dcf-42b0-93a0-f8067bc3594a',
        #     '3e9f0d04-494a-400d-b2d2-635d2d4df7c9',
        #     '2907a22f-7357-4b06-8c98-c1f94966c193',
        #     'ebd807ef-f9c7-4396-9670-107a420159d1',
        #     'b4a36b03-1168-440f-ac77-f7ffbb5379ec',
        #     'd2fb5a92-e552-4e15-81e8-a00ae6db5002',
        #     'fb90695c-178e-4f10-a984-4aa38ed588a2',
        #     'cace5edc-add8-43a9-9099-45ae23d96c4d',
        #     'df5ac610-e548-461d-8a8f-e22ec93036a9',
        #     'b769bb39-080b-4e1e-a0cb-4b3324cc842e',
        #     '63efcfe7-b6af-4e00-8830-228a34e14259',
        #     'f65a157b-1220-498d-9480-2c5ad7bf64a6',
        #     '3b1f69b5-5562-4778-b1ef-5af9dd78dd0b'
        # ]
        # for tree_id in const_evaluation_criteria_tree_id_list:
        #     tag_repository.insert_tag_ownership_relationship(
        #             tag_ownership_rel=TagOwnershipRelationshipModel(
        #                 tag_ownership_id="7da749e7-5c27-4b01-9617-5af5bf9382b2",
        #                 resource_category="EVALUATION_CRITERIA_TREE",
        #                 resource_id=tree_id,
        #                 relationship="REPORT",
        #             ),
        #             transaction=trans
        #         )
        # var_evaluation_criteria_tree_id_list = [
        #     'aff4a3e8-226e-4f09-b460-645d85451cf8',
        #     '01d475a1-1d47-42fa-970b-4ad16a29218f',
        #     '4b2a659e-ca2e-40df-8e58-1ea47b18adb1',
        #     '2de347ab-5ca0-47c3-af84-c96a6b881165',
        #     '8f30c1fb-99b8-4855-b775-77c51e77759f',
        #     '456bb822-aa82-48a7-beee-400d58205d7a',
        #     'e47fbcce-2cfd-4ee5-8dac-5ead7f7058e2',
        #     '038fdbb3-b225-4813-8b47-527399b2ff17',
        #     '65a0d31d-0c39-4f11-842d-a785aa4a9ca4',
        #     '4538121a-9ced-49f3-bcf8-0196fc1e2a6a',
        #     'b5d3c323-3663-4be0-83c8-3f2bd51aba8d',
        #     '61b7e156-f64c-4f5f-babc-156b828f281c'
        # ]
        # for tree_id in var_evaluation_criteria_tree_id_list:
        #     tag_repository.insert_tag_ownership_relationship(
        #             tag_ownership_rel=TagOwnershipRelationshipModel(
        #                 tag_ownership_id="6d8722b0-0ce6-4f33-ba7a-ad57f2f40a4c",
        #                 resource_category="EVALUATION_CRITERIA_TREE",
        #                 resource_id=tree_id,
        #                 relationship="REPORT",
        #             ),
        #             transaction=trans
        #         )


def test_add_evaluation_criteria_plan_scope(prepare_robot, prepare_domain_evaluation_container):
    uow = prepare_domain_evaluation_container.uow()
    evaluation_criteria_plan_scope_repository = (
        prepare_domain_evaluation_container.evaluation_criteria_plan_scope_repository()
    )
    with uow:
        transaction = uow.log_transaction(
            handler=prepare_robot, action="test_add_evaluation_criteria_plan_scope"
        )
        evaluation_criteria_plan_scope_repository.insert_evaluation_criteria_plan_scope(
            data=EvaluationCriteriaPlanScopeModel(
                evaluation_criteria_plan_id="79024eaf-1226-4cd5-b942-e53b80096d00",
                scope_category="ESTABLISHMENT_ASSIGN",
                scope_id="265d4898-a0bc-43a1-b226-83a678131cd6",
                start_at="2023-08-11 00:00:00",
                finish_at="2023-08-11 11:00:00",
            ),
            transaction=transaction,
        )


def test_add_evaluation_assignment(prepare_robot, prepare_domain_evaluation_container):
    uow = prepare_domain_evaluation_container.uow()
    evaluation_assignment_repository = (
        prepare_domain_evaluation_container.evaluation_assignment_repository()
    )
    with uow:
        transaction = uow.log_transaction(
            handler=prepare_robot, action="test_add_evaluation_assignment"
        )
        evaluation_assignment_repository.insert_evaluation_assignment(
            data=EvaluationAssignmentModel(
                evaluation_criteria_plan_id="79024eaf-1226-4cd5-b942-e53b80096d00",
                effected_category="ESTABLISHMENT_ASSIGN",
                effected_id="265d4898-a0bc-43a1-b226-83a678131cd6",
                start_at="2023-08-11 00:00:00",
                finish_at="2023-08-11 11:00:00",
            ),
            transaction=transaction,
        )


def test_add_benchmark_score(prepare_robot, prepare_domain_evaluation_container):
    uow = prepare_domain_evaluation_container.uow()
    benchmark_score_repository = prepare_domain_evaluation_container.benchmark_score_repository()
    with uow:
        transaction = uow.log_transaction(handler=prepare_robot, action="test_add_benchmark_score")
        data_list = [
            {"id": "3ace8b04-7fef-48ad-a483-a63d95ee4c3c", "score": "2"},
        ]
        for data in data_list:
            numeric_score = data.get("score")
            string_score = None
            if numeric_score in ["优秀", "良好", "合格"]:
                string_score = data.get("score")
                numeric_score = None
            benchmark_score_repository.insert_benchmark_score(
                benchmark_score=BenchmarkScoreModel(
                    evaluation_assignment_id="cd57980c-bd40-4786-ac1b-89c4c7f3a696",
                    numeric_score=numeric_score,
                    string_score=string_score,
                    benchmark_id=data.get("id"),
                    source_score_log_category="方便开发生成报告",
                    source_score_log_id="所以这里先随便写了一下",
                ),
                transaction=transaction,
            )


def test_add(prepare_robot, prepare_backbone_container):
    uow = prepare_backbone_container.uow()
    establishment_assign_repository = prepare_backbone_container.establishment_assign_repository()
    with uow:
        transaction = uow.log_transaction(
            handler=prepare_robot, action="test_add_establishment_assign"
        )
        establishment_assign_repository.insert_establishment_assign(
            data=EstablishmentAssignModel(
                establishment_id="cf2a5df9-7fb2-45d5-bc42-a92e7547850a",
                people_id="7b767e80-41a4-42cb-a619-075c7f39455b",
                start_at=datetime.now(),
            ),
            transaction=transaction,
        )
