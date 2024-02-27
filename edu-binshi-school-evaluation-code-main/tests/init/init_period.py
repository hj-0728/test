import datetime
import calendar

from edu_binshi.model.period_category_model import PeriodCategoryModel, \
    EnumPeriodCategoryCode
from edu_binshi.model.period_model import PeriodModel
from infra_backbone.service.robot_service import RobotService


def test_init_period_week_and_month(prepare_backbone_container, prepare_edu_evaluation_container):
    uow = prepare_backbone_container.uow()
    robot_service: RobotService = prepare_backbone_container.robot_service()
    period_repository = prepare_edu_evaluation_container.period_repository()
    period_category_repository = prepare_edu_evaluation_container.period_category_repository()
    with uow:
        handler = robot_service.get_system_robot().to_basic_handler()
        trans = uow.log_transaction(handler=handler, action="set_period")
        # 指定起始日期
        period_list = period_repository.get_period_list_by_category_code_list(
            period_category_code_list=[EnumPeriodCategoryCode.ACADEMIC_YEAR.name, EnumPeriodCategoryCode.SEMESTER.name]
        )

        period_category_week = period_category_repository.get_period_category_by_code(
            period_category_code=EnumPeriodCategoryCode.WEEK.name
        )

        period_category_month = period_category_repository.get_period_category_by_code(
            period_category_code=EnumPeriodCategoryCode.MONTH.name
        )

        for period in period_list:

            is_continue_wek = True

            week_start_at = period.start_at
            while is_continue_wek:
                week_end = datetime.timedelta(
                    days=6 - week_start_at.weekday(), hours=23, minutes=59, seconds=59
                )
                end_at = week_start_at + week_end
                if end_at > period.finish_at:
                    is_continue_wek = False
                    end_at = period.finish_at
                period_repository.insert_period(
                    period=PeriodModel(
                        period_category_id=period_category_week.id,
                        name=f'{week_start_at.strftime("%Y/%m/%d")}-{end_at.strftime("%Y/%m/%d")}',
                        start_at=week_start_at,
                        finish_at=end_at,
                        parent_id=period.id
                    ),
                    transaction=trans
                )
                print(f"Week starting from {week_start_at} to {end_at}")
                week_start_at = end_at + datetime.timedelta(seconds=1)

            is_continue_month = True

            month_start_at = period.start_at

            while is_continue_month:
                last_day = calendar.monthrange(month_start_at.year, month_start_at.month)[1]
                days = last_day - month_start_at.day
                end_at = month_start_at + datetime.timedelta(
                    days=days, hours=23, minutes=59, seconds=59
                )
                if end_at > period.finish_at:
                    is_continue_month = False
                    end_at = period.finish_at
                period_repository.insert_period(
                    period=PeriodModel(
                        period_category_id=period_category_month.id,
                        name=f'{month_start_at.month}月',
                        start_at=month_start_at,
                        finish_at=end_at,
                        parent_id=period.id
                    ),
                    transaction=trans
                )
                print(f"month starting from {month_start_at} to {end_at}")
                month_start_at = end_at + datetime.timedelta(seconds=1)


def test_init_period_category(
    prepare_backbone_container, prepare_edu_evaluation_container
):
    uow = prepare_backbone_container.uow()
    robot_service: RobotService = prepare_backbone_container.robot_service()
    period_category_repository = prepare_edu_evaluation_container.period_category_repository()
    with uow:
        handler = robot_service.get_system_robot().to_basic_handler()
        trans = uow.log_transaction(handler=handler, action="init_period_category")
        period_category_repository.insert_period_category(
            period_category=PeriodCategoryModel(
                name=EnumPeriodCategoryCode.ACADEMIC_YEAR.value,
                code=EnumPeriodCategoryCode.ACADEMIC_YEAR.name
            ),
            transaction=trans
        )
        period_category_repository.insert_period_category(
            period_category=PeriodCategoryModel(
                name=EnumPeriodCategoryCode.SEMESTER.value,
                code=EnumPeriodCategoryCode.SEMESTER.name
            ),
            transaction=trans
        )
        period_category_repository.insert_period_category(
            period_category=PeriodCategoryModel(
                name=EnumPeriodCategoryCode.MONTH.value,
                code=EnumPeriodCategoryCode.MONTH.name
            ),
            transaction=trans
        )
        period_category_repository.insert_period_category(
            period_category=PeriodCategoryModel(
                name=EnumPeriodCategoryCode.WEEK.value,
                code=EnumPeriodCategoryCode.WEEK.name
            ),
            transaction=trans
        )


def test_init_period_year_or_semester(
    prepare_backbone_container, prepare_edu_evaluation_container
):
    """
    插入学年或者学期数据（period）
    """
    uow = prepare_backbone_container.uow()
    robot_service: RobotService = prepare_backbone_container.robot_service()
    period_repository = prepare_edu_evaluation_container.period_repository()
    with uow:
        handler = robot_service.get_system_robot().to_basic_handler()
        trans = uow.log_transaction(handler=handler, action="test_init_period_year_or_semester")
        year_period_id = period_repository.insert_period(
            period=PeriodModel(
                period_category_id='05cc8a30-f1af-44dd-9d39-7de94b1c2c6e',
                name='2022-2023学年',
                start_at=datetime.datetime(2022, 9, 1),
                finish_at=datetime.datetime(2023, 7, 1),
            ),
            transaction=trans
        )
        period_repository.insert_period(
            period=PeriodModel(
                period_category_id='da1fce60-4a34-475f-a4e7-18779420f63f',
                name='2022-2023学年上学期',
                start_at=datetime.datetime(2022, 9, 1),
                finish_at=datetime.datetime(2023, 2, 1),
                parent_id=year_period_id
            ),
            transaction=trans
        )
        period_repository.insert_period(
            period=PeriodModel(
                period_category_id='da1fce60-4a34-475f-a4e7-18779420f63f',
                name='2022-2023学年下学期',
                start_at=datetime.datetime(2022, 3, 1),
                finish_at=datetime.datetime(2023, 7, 1),
                parent_id=year_period_id
            ),
            transaction=trans
        )
        year_period_id = period_repository.insert_period(
            period=PeriodModel(
                period_category_id='05cc8a30-f1af-44dd-9d39-7de94b1c2c6e',
                name='2023-2024学年',
                start_at=datetime.datetime(2023, 7, 3),
                finish_at=datetime.datetime(2024, 7, 1),
            ),
            transaction=trans
        )
        period_repository.insert_period(
            period=PeriodModel(
                period_category_id='da1fce60-4a34-475f-a4e7-18779420f63f',
                name='2023-2024学年上学期',
                start_at=datetime.datetime(2023, 7, 3),
                finish_at=datetime.datetime(2024, 2, 1),
                parent_id=year_period_id
            ),
            transaction=trans
        )
