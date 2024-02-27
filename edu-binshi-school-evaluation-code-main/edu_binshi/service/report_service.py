import copy
import logging
import traceback
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from queue import Queue
from typing import List, Tuple, Optional

from infra_basic.basic_resource import BasicResource
from infra_basic.errors import BusinessError
from infra_basic.transaction import Transaction
from infra_object_storage.helper.object_storage_client import ObjectStorageClient
from infra_object_storage.service.object_storage_service import ObjectStorageService
from infra_utility.datetime_helper import local_now
from infra_utility.token_helper import generate_uuid_id

from edu_binshi.data.enum import EnumFileRelationshipRelationship, \
    EnumFileRelationshipResCategory
from edu_binshi.data.query_params.evaluation_report_assignment_query_params import \
    EvaluationReportAssignmentQueryParams
from edu_binshi.model.report_record_eval_assign_map_model import \
    ReportRecordEvalAssignMapModel
from edu_binshi.model.report_record_model import (
    EnumReportTargetCategory,
    ReportFileInfoModel,
    ReportRecordModel,
    UploadReportModel, EnumReportRecordStatus,
)
from edu_binshi.model.view.evaluation_report_assignment_vm import \
    EvaluationReportAssignmentViewModel
from edu_binshi.model.view.report_record_vm import ReportRecordViewModel
from edu_binshi.model.zip_model import ZipVm
from edu_binshi.repository.evaluation_repository import \
    EvaluationRepository
from edu_binshi.repository.report_repository import ReportRepository
from edu_binshi.service.report_service_v2 import ReportServiceV2
from edu_binshi.utility.file_helper import handle_file_name
from edu_binshi.utility.zip_helper import get_zip_file
from infra_backbone.model.dept_category_model import EnumDeptCategoryCode
from infra_backbone.model.site_message_context_model import (
    EnumSiteMessageContextRelationship,
    EnumSiteMessageContextResourceCategory,
    SiteMessageContextModel,
)
from infra_backbone.model.site_message_model import (
    EnumSiteMessageInitResourceCategory,
    SiteMessageModel,
)
from infra_backbone.repository.dimension_dept_tree_repository import \
    DimensionDeptTreeRepository
from infra_backbone.service.site_message_service import SiteMessageService


class ReportService:
    """
    报告 service
    """

    def __init__(
        self,
        object_storage_service: ObjectStorageService,
        report_repository: ReportRepository,
        site_message_service: SiteMessageService,
        report_service_v2: ReportServiceV2,
        dimension_dept_tree_repository: DimensionDeptTreeRepository,
        object_storage_client: ObjectStorageClient,
        evaluation_repository: EvaluationRepository,
    ):
        self.__object_storage_service = object_storage_service
        self.__report_repository = report_repository
        self.__site_message_service = site_message_service
        self.__report_service_v2 = report_service_v2
        self.__dimension_dept_tree_repository = dimension_dept_tree_repository
        self.__object_storage_client = object_storage_client
        self.__evaluation_repository = evaluation_repository

    def before_generate_report_check(
        self,
        args: ReportRecordModel,
        transaction: Transaction,
        not_insert: bool = True
    ) -> Optional[ReportFileInfoModel]:
        """
        生成报告前检查（检查报告是否已经生成）
        :param args:
        :param transaction:
        :param not_insert:
        :return:
        """
        report_file = self.__report_repository.get_exist_report_file(
            args=args,
        )

        file_url = None
        if report_file:
            url = self.__object_storage_service.build_url(
                bucket_name=report_file.bucket_name,
                object_name=report_file.object_name,
            )
            file_url = ReportFileInfoModel(
                id=report_file.file_id,
                url=url,
                relationship=report_file.file_relationship_relationship,
            )
        if not file_url and not not_insert:
            return None

        if file_url:
            args.status = EnumReportRecordStatus.SUCCEED.name

        if file_url or args.target_category != EnumReportTargetCategory.EVALUATION_ASSIGNMENT.name:
            self.save_report_record_link_file(
                report_record=args,
                not_insert=not_insert,
                transaction=transaction,
                file_url=file_url,
            )

        return file_url

    def generate_report(
        self,
        report_record: ReportRecordViewModel,
        transaction: Transaction,
    ) -> Tuple[Optional[ReportFileInfoModel], Optional[ReportRecordViewModel]]:
        """
        生成报告
        :param report_record:
        :param transaction:
        :return:
        """

        if report_record.target_category == EnumReportTargetCategory.EVALUATION_ASSIGNMENT.name:
            return self.handle_generate_evaluation_assignment_report(
                report_record=report_record,
                transaction=transaction,
            )

        else:
            report_record_list = self.__report_repository.get_report_record_by_report_record_id_and_status(
                report_record_id=report_record.id,
                status=EnumReportRecordStatus.PENDING.name
            )
            if len(report_record_list) == 1 and report_record_list[0].status == EnumReportRecordStatus.PENDING.name:
                return self.handle_generate_dimension_dept_tree_report(
                    report_record=report_record,
                    transaction=transaction,
                )
        return None, None

    def handle_generate_evaluation_assignment_report(
        self,
        report_record: ReportRecordViewModel,
        transaction: Transaction,
    ) -> Tuple[Optional[ReportFileInfoModel], ReportRecordViewModel]:
        """
        生成个人报告
        :param report_record:
        :param transaction:
        :return:
        """
        file_url = None
        not_insert = False
        if not report_record.id:
            report_record.id = generate_uuid_id()
            not_insert = True
        try:
            file_url, _ = self.generate_evaluation_assignment_report(
                report_record_id=report_record.id,
                evaluation_assignment_id=report_record.target_id,
                transaction=transaction,
            )
            report_record.status = EnumReportRecordStatus.SUCCEED.name

        except Exception as e:
            traceback.print_exc()
            report_record.error = str(e)
            report_record.status = EnumReportRecordStatus.FAILED.name
        self.save_report_record_link_file(
            report_record=report_record,
            not_insert=not_insert,
            transaction=transaction,
            file_url=file_url,
        )
        return file_url, report_record

    def generate_evaluation_assignment_report(
        self,
        evaluation_assignment_id: str,
        report_record_id: str,
        transaction: Transaction,
        report_file_name: str = None,
    ) -> Tuple[ReportFileInfoModel, bytes]:
        """
        保存 评价分配 报告
        :param evaluation_assignment_id:
        :param report_record_id:
        :param transaction:
        :param report_file_name: 可不填
        :return:
        """

        if not report_file_name:
            # 获取文件名
            report_file_name = self.get_report_file_name(
                target_category=EnumReportTargetCategory.EVALUATION_ASSIGNMENT.name,
                target_id=evaluation_assignment_id,
            )
        logging.info(f"为【{evaluation_assignment_id}】生成报告")
        # 获取报告二进制
        doc_data, pdf_data = self.__report_service_v2.generate_report(
            evaluation_assignment_id=evaluation_assignment_id,
        )

        # 保存 st_report_record_eval_assign_map

        self.__report_repository.insert_report_record_eval_assign_map(
            report_record_eval_assign_map=ReportRecordEvalAssignMapModel(
                report_record_id=report_record_id,
                evaluation_assignment_id=evaluation_assignment_id,
            ),
            transaction=transaction,
        )

        # 保存报告文件
        file_url_list = self.save_report_file(
            report_file_list=[
                UploadReportModel(
                    file_resource_id=evaluation_assignment_id,
                    file_resource_category=EnumFileRelationshipResCategory.EVALUATION_ASSIGNMENT.name,
                    file_bytes=doc_data,
                    file_name=report_file_name + '.docx',
                    file_relationship_relationship=EnumFileRelationshipRelationship.REPORT_WORD.name,
                ),
                UploadReportModel(
                    file_resource_id=evaluation_assignment_id,
                    file_resource_category=EnumFileRelationshipResCategory.EVALUATION_ASSIGNMENT.name,
                    file_bytes=pdf_data,
                    file_name=report_file_name + '.pdf',
                    file_relationship_relationship=EnumFileRelationshipRelationship.REPORT_PDF.name,
                ),
            ],
            transaction=transaction,
        )

        file_pdf = [x for x in file_url_list if x.relationship == EnumFileRelationshipRelationship.REPORT_PDF.name]

        if file_pdf:
            return file_pdf[0], pdf_data

    def handle_generate_dimension_dept_tree_report(
        self, report_record: ReportRecordViewModel, transaction: Transaction
    ) -> Tuple[Optional[ReportFileInfoModel], ReportRecordViewModel]:
        """
        生成维度部门报告
        :param report_record:
        :param transaction:
        :return:
        """
        file_url = None
        not_insert = False
        try:
            if not report_record.id:
                report_record.id = generate_uuid_id()
                not_insert = True

            evaluation_assignment_list = self.fetch_plan_dept_evaluation_report_assignment(
                report_record=report_record
            )

            # 生成报告文件
            error_list, zip_file_list = self.generate_dimension_dept_tree_report(
                report_record=report_record,
                evaluation_assignment_list=evaluation_assignment_list,
                transaction=transaction,
            )
            if not error_list:

                report_file_name = self.get_report_file_name(
                    target_category=report_record.target_category,
                    target_id=report_record.target_id,
                    plan_id=report_record.evaluation_criteria_plan_id,
                )

                file_url_list = self.save_report_file(
                    report_file_list=[
                        UploadReportModel(
                            file_resource_id=report_record.id,
                            file_resource_category=EnumFileRelationshipResCategory.REPORT_RECORD.name,
                            file_bytes=get_zip_file(zip_file_list),
                            file_name=f"{report_file_name}.zip",
                            file_relationship_relationship=EnumFileRelationshipRelationship.REPORT_ZIP.name,
                        ),
                    ],
                    transaction=transaction,
                )
                file_url = file_url_list[0]

            report_record.status = EnumReportRecordStatus.SUCCEED.name
            if error_list:
                report_record.error = str("；".join(error_list))
                report_record.status = EnumReportRecordStatus.FAILED.name

        except Exception as e:
            report_record.error = str(e)
            report_record.status = EnumReportRecordStatus.FAILED.name
        self.save_report_record_link_file(
            report_record=report_record,
            not_insert=not_insert,
            transaction=transaction,
        )
        return file_url, report_record

    def fetch_plan_dept_evaluation_report_assignment(
        self, report_record: ReportRecordViewModel
    ) -> List[EvaluationReportAssignmentViewModel]:
        """
        获取计划某个部门的评价分配及报告情况
        :param report_record:
        :return:
        """
        params = report_record.cast_to(
            EvaluationReportAssignmentQueryParams,
            dimension_dept_tree_id=report_record.target_id,
            page_size=100000,
        )
        if report_record.target_category == EnumReportTargetCategory.ORGANIZATION.name:
            params.dimension_dept_tree_id = None
        evaluation_criteria_plan = self.__report_repository.get_evaluation_criteria_plan_by_id(
            evaluation_criteria_plan_id=report_record.evaluation_criteria_plan_id
        )
        params.compared_time = min(
            evaluation_criteria_plan.executed_finish_at,
            evaluation_criteria_plan.handled_at
        )

        # 获取部门下面所以的学生（评价分配）、学生的年级/班级、学生是否有报告
        evaluation_assignment_report = self.__report_repository.fetch_evaluation_report_assignment(
            params=params,
        )

        logging.error(f"共有{len(evaluation_assignment_report.data)}条数据需被导出")

        return evaluation_assignment_report.data

    def generate_dimension_dept_tree_report(
        self,
        report_record: ReportRecordModel,
        evaluation_assignment_list: List[EvaluationReportAssignmentViewModel],
        transaction: Transaction,
    ):
        """
        生成维度部门报告
        :param report_record:
        :param evaluation_assignment_list:
        :param transaction:
        :return:
        """

        zip_file_list = []
        error_list = []

        plan_info = self.__evaluation_repository.fetch_evaluation_criteria_plan_by_id(
            evaluation_criteria_plan_id=report_record.evaluation_criteria_plan_id
        )

        # 判断选择的部门类型：为组织、...、年级、班级
        dept_type = report_record.target_category

        if report_record.target_category == EnumReportTargetCategory.DIMENSION_DEPT_TREE.name:
            dept_info = self.__dimension_dept_tree_repository.get_dept_info_by_dimension_dept_tree_id(
                dimension_dept_tree_id=report_record.target_id
            )
            dept_type = dept_info.category_code

        for idx, evaluation_assignment in enumerate(evaluation_assignment_list):
            try:
                logging.error(evaluation_assignment.evaluation_assignment_id)
                logging.error(evaluation_assignment.people_name)
                if evaluation_assignment.report_file_id:
                    file_url, file_bytes = self.get_report_file_by_resource(
                        resource=BasicResource(
                            id=evaluation_assignment.evaluation_assignment_id,
                            category=EnumFileRelationshipResCategory.EVALUATION_ASSIGNMENT.name
                        )
                    )
                else:
                    report_file_name = f"{plan_info.period_name}-{plan_info.name}-{evaluation_assignment.people_name}-评价报告"
                    file_url, file_bytes = self.generate_evaluation_assignment_report(
                        evaluation_assignment_id=evaluation_assignment.evaluation_assignment_id,
                        report_record_id=report_record.id,
                        transaction=transaction,
                        report_file_name=handle_file_name(name=report_file_name),
                    )
                if dept_type == EnumDeptCategoryCode.CLASS.name:
                    pdf_name = evaluation_assignment.people_name + '.pdf'
                elif dept_type == EnumDeptCategoryCode.GRADE.name:
                    pdf_name = f"{evaluation_assignment.class_name}/{evaluation_assignment.people_name}.pdf"
                else:
                    pdf_name = evaluation_assignment.dept_name + '/' + evaluation_assignment.people_name + '.pdf'
                logging.error(f'报告_name:{file_url.name}, {pdf_name}')
                zip_file_list.append(
                    ZipVm(
                        file_name=pdf_name,
                        stream_data=file_bytes,
                    )
                )
            except Exception as error:
                logging.error(error)
                error_list.append(str(error))

        return list(set(error_list)), zip_file_list

    def get_report_file_by_resource(
        self, resource: BasicResource
    ) -> Optional[Tuple[ReportFileInfoModel, bytes]]:
        """
        根据文件id 获取报告信息
        :param resource:
        :return:
        """

        file_info_list = self.__object_storage_service.get_resource_related_file_list(
            resource=resource,
            relationship=EnumFileRelationshipRelationship.REPORT_PDF.name,
        )

        if not file_info_list:
            return None
        file_info = file_info_list[0]

        file_bytes = self.__object_storage_client.download_file(
            object_name=file_info.object_name,
            bucket_name=file_info.bucket_name,
        )

        return ReportFileInfoModel(
            id=file_info.id,
            url=file_info.url,
            name=file_info.original_name,
            relationship=EnumFileRelationshipRelationship.REPORT_PDF.name,
        ), file_bytes

    def save_report_record_link_file(
        self,
        report_record: ReportRecordModel,
        not_insert: bool,
        transaction: Transaction,
        file_url: ReportFileInfoModel = None,
    ):
        """
        修改报告记录 并添加 file relationship
        :param report_record:
        :param not_insert:
        :param transaction:
        :param file_url:
        :return:
        """

        if not_insert:
            report_record.args = copy.deepcopy(report_record.dict())
            report_record.id = self.__report_repository.insert_report_record(
                report_record=report_record,
                transaction=transaction
            )
        else:
            self.__report_repository.update_report_record(
                report_record=report_record,
                transaction=transaction,
                limited_col_list=["status", "error"]
            )

        if file_url:
            self.__object_storage_service.link_file_and_resource(
                file_id=file_url.id,
                resource=BasicResource(
                    id=report_record.id,
                    category=EnumFileRelationshipResCategory.REPORT_RECORD.name,
                ),
                relationship=file_url.relationship,
                transaction=transaction
            )

    def save_report_file(
        self,
        report_file_list: List[UploadReportModel],
        transaction: Transaction,
    ) -> List[ReportFileInfoModel]:
        """
        上传报告文件
        :param report_file_list:
        :param transaction:
        :return:
        """
        file_url_list = []
        for report_file in report_file_list:
            file = self.__object_storage_service.upload_file_with_resource(
                file_name=report_file.file_name,
                file_blob=report_file.file_bytes,
                resource=BasicResource(
                    id=report_file.file_resource_id,
                    category=report_file.file_resource_category,
                ),
                relationship=report_file.file_relationship_relationship,
                transaction=transaction,
            )
            file_url_list.append(
                ReportFileInfoModel(
                    id=file.id,
                    url=file.url,
                    name=report_file.file_name,
                    relationship=report_file.file_relationship_relationship,
                )
            )
        return file_url_list

    def get_report_file_name(
        self, target_category: str, target_id: str, plan_id: str = None
    ) -> str:
        """
        获取报告文件名称
        :param target_category:
        :param target_id:
        :param plan_id: 当 target_category 为 EVALUATION_ASSIGNMENT 时不用传
        :return:
        """
        file_name = ""
        if target_category == EnumReportTargetCategory.EVALUATION_ASSIGNMENT.name:
            eval_assignment = self.__evaluation_repository.fetch_evaluation_assignment_info(
                evaluation_assignment_id=target_id
            )
            if not eval_assignment:
                raise BusinessError("未获取到学生报告信息")
            file_name = (
                f"{eval_assignment.people_name}_"
                f"{eval_assignment.plan_name}_评价报告"
            )
        if target_category == EnumReportTargetCategory.DIMENSION_DEPT_TREE.name:
            report_info = self.__report_repository.get_dimension_dept_tree_report_info(
                evaluation_criteria_plan_id=plan_id,
                dimension_dept_tree_id=target_id,
            )
            if not report_info:
                raise BusinessError("未获取到部门报告信息")
            file_name = (
                f"{report_info.dept_name}_"
                f"{report_info.evaluation_criteria_plan_name}_评价报告"
            )
        if target_category == EnumReportTargetCategory.ORGANIZATION.name:
            report_info = self.__report_repository.get_organization_report_info(
                evaluation_criteria_plan_id=plan_id,
                organization_id=target_id,
            )
            if not report_info:
                raise BusinessError("未获取到组织报告信息")
            file_name = (
                f"{report_info.organization_name}_"
                f"{report_info.evaluation_criteria_plan_name}_评价报告"
            )

        return handle_file_name(name=file_name)

    def send_site_message(
        self,
        args: ReportRecordViewModel,
        transaction: Transaction,
        file_info: ReportFileInfoModel = None,
    ):
        """
        发送站内信
        :param args:
        :param transaction:
        :param file_info:
        :return:
        """
        try:
            if file_info and file_info.name:
                file_name = file_info.name
            else:
                try:
                    file_name = self.get_report_file_name(
                        target_category=args.target_category,
                        target_id=args.target_id,
                        plan_id=args.evaluation_criteria_plan_id,
                    )
                except Exception as error:
                    logging.error(error)
                    plan_info = self.__evaluation_repository.fetch_evaluation_criteria_plan_by_id(
                        evaluation_criteria_plan_id=args.evaluation_criteria_plan_id
                    )
                    if not plan_info:
                        file_name = "评价报告"
                    else:
                        file_name = f"{plan_info.name}_评价报告"
            content = {"title": f"{file_name[:-4]}"}
            if args.error:
                content["content"] = f"生成【{file_name[:-4]}】失败，原因：{args.error}"

            if file_info:
                content["file_id"] = file_info.id
                content["content"] = f"生成【{file_name[:-4]}】成功。"
            self.__site_message_service.add_site_message(
                site_message=SiteMessageModel(
                    receive_user_id=args.user_id,
                    send_user_id=args.user_id,
                    init_resource_category=EnumSiteMessageInitResourceCategory.REPORT_RECORD.name,
                    init_resource_id=args.id,
                    content=content,
                    created_at=local_now(),
                    site_message_context_list=[
                        SiteMessageContextModel(
                            relationship=EnumSiteMessageContextRelationship.UNKNOWN.name,
                            resource_category=EnumSiteMessageContextResourceCategory.ROLE.name,
                            resource_id=args.role_id,
                        )
                    ],
                ),
                transaction=transaction,
            )
        except Exception as error:
            logging.error(error)
