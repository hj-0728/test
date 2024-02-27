from dependency_injector import containers, providers
from infra_basic.sqlalchemy_uow import SqlAlchemyUnitOfWork

from edu_binshi.repository.docx_table_style_config_repository import DocxTableStyleConfigRepository
from edu_binshi.repository.evaluation_repository import \
    EvaluationRepository
from edu_binshi.repository.k12_teacher_subject_repository import K12TeacherSubjectRepository
from edu_binshi.repository.period_category_repository import PeriodCategoryRepository
from edu_binshi.repository.period_repository import PeriodRepository
from edu_binshi.repository.report_record_eval_assign_map_repository import \
    ReportRecordEvalAssignMapRepository
from edu_binshi.repository.report_record_repository import ReportRecordRepository
from edu_binshi.repository.report_repository import ReportRepository
from edu_binshi.repository.report_repository_v2 import ReportRepositoryV2
from edu_binshi.repository.student_repository import StudentRepository
from edu_binshi.repository.subject_repository import SubjectRepository
from edu_binshi.service.k12_teacher_subject_service import K12TeacherSubjectService
from edu_binshi.service.people_service import PeopleService
from edu_binshi.service.period_category_service import PeriodCategoryService
from edu_binshi.service.period_service import PeriodService
from edu_binshi.service.report_record_service import ReportRecordService
from edu_binshi.service.report_service import ReportService
from edu_binshi.service.report_service_v2 import ReportServiceV2
from edu_binshi.service.student_service import StudentService
from infra_backbone.backbone_container import BackboneContainer
from infra_backbone.object_storage_container import ObjectStorageContainer


class EduEvaluationContainer(containers.DeclarativeContainer):
    uow = providers.Dependency(instance_of=SqlAlchemyUnitOfWork)  # type: ignore

    backbone_container: BackboneContainer = providers.Container(
        BackboneContainer, uow=uow
    )  # type: ignore

    object_storage_container: ObjectStorageContainer = providers.Container(
        ObjectStorageContainer, uow=uow
    )  # type: ignore

    period_category_repository = providers.ThreadLocalSingleton(
        PeriodCategoryRepository, db_session=uow.provided.db_session
    )  # type: ignore

    period_repository = providers.ThreadLocalSingleton(
        PeriodRepository, db_session=uow.provided.db_session
    )  # type: ignore

    student_repository = providers.ThreadLocalSingleton(
        StudentRepository, db_session=uow.provided.db_session
    )  # type: ignore

    subject_repository = providers.ThreadLocalSingleton(
        SubjectRepository, db_session=uow.provided.db_session
    )  # type: ignore

    k12_teacher_subject_repository = providers.ThreadLocalSingleton(
        K12TeacherSubjectRepository, db_session=uow.provided.db_session
    )  # type: ignore

    docx_table_style_config_repository = providers.ThreadLocalSingleton(
        DocxTableStyleConfigRepository, db_session=uow.provided.db_session
    )  # type: ignore

    report_record_repository = providers.ThreadLocalSingleton(
        ReportRecordRepository, db_session=uow.provided.db_session
    )  # type: ignore

    report_repository = providers.ThreadLocalSingleton(
        ReportRepository, db_session=uow.provided.db_session
    )  # type: ignore

    report_record_eval_assign_map_repository = providers.ThreadLocalSingleton(
        ReportRecordEvalAssignMapRepository, db_session=uow.provided.db_session
    )  # type: ignore

    evaluation_repository = providers.ThreadLocalSingleton(
        EvaluationRepository, db_session=uow.provided.db_session
    )  # type: ignore

    report_repository_v2 = providers.ThreadLocalSingleton(
        ReportRepositoryV2, db_session=uow.provided.db_session
    )  # type: ignore

    k12_teacher_subject_service = providers.ThreadLocalSingleton(
        K12TeacherSubjectService,
        subject_repository=subject_repository,
        k12_teacher_subject_repository=k12_teacher_subject_repository,
    )  # type: ignore

    student_service = providers.ThreadLocalSingleton(
        StudentService,
        student_repository=student_repository,
        dimension_service=backbone_container.dimension_service,
        user_service=backbone_container.user_service,
        role_repository=backbone_container.role_repository,
        dict_repository=backbone_container.dict_repository,
    )  # type: ignore

    people_service = providers.ThreadLocalSingleton(
        PeopleService,
        backbone_people_service=backbone_container.people_service,
        organization_repository=backbone_container.organization_repository,
        dimension_repository=backbone_container.dimension_repository,
    )  # type: ignore

    period_service = providers.ThreadLocalSingleton(
        PeriodService,
        period_repository=period_repository,
    )  # type: ignore

    period_category_service = providers.ThreadLocalSingleton(
        PeriodCategoryService,
        period_category_repository=period_category_repository,
    )  # type: ignore

    report_record_service = providers.ThreadLocalSingleton(
        ReportRecordService,
        report_record_repository=report_record_repository,
    )  # type: ignore

    report_service_v2 = providers.ThreadLocalSingleton(
        ReportServiceV2,
        report_repository_v2=report_repository_v2,
    )  # type: ignore

    report_service = providers.ThreadLocalSingleton(
        ReportService,
        object_storage_service=object_storage_container.object_storage_service,
        report_repository=report_repository,
        site_message_service=backbone_container.site_message_service,
        report_service_v2=report_service_v2,
        dimension_dept_tree_repository=backbone_container.dimension_dept_tree_repository,
        object_storage_client=object_storage_container.object_storage_client,
        evaluation_repository=evaluation_repository,
    )  # type: ignore

