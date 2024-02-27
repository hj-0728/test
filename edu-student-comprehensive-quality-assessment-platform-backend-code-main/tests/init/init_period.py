import json
from datetime import datetime

from infra_utility.file_helper import build_abs_path_by_file

from biz_comprehensive.model.period_category_model import EnumPeriodCategoryCode, PeriodCategoryModel
from biz_comprehensive.model.period_model import PeriodModel


def test_init_period_category(prepare_biz_comprehensive, prepare_robot):
    """
    插入周期类型数据（period_category）
    :param prepare_biz_comprehensive:
    :return:
    """
    uow = prepare_biz_comprehensive.uow()
    period_category_repository = prepare_biz_comprehensive.period_category_repository()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_init_period_category")
        for category_code in EnumPeriodCategoryCode:
            period_category = PeriodCategoryModel(
                name=category_code.value,
                code=category_code.name
            )
            period_category_repository.insert_period_category(
                period_category=period_category, transaction=trans
            )


def test_init_period_year_or_semester(prepare_biz_comprehensive, prepare_robot):
    """
    插入学年或者学期数据（period）
    """
    uow = prepare_biz_comprehensive.uow()
    period_repository = prepare_biz_comprehensive.period_repository()
    period_category_repository = prepare_biz_comprehensive.period_category_repository()
    with uow:
        trans = uow.log_transaction(handler=prepare_robot, action="test_init_period_year_or_semester")
        file_path = build_abs_path_by_file(__file__, 'init_json/init_period.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            init_data = json.load(file)["academic_year_and_semester"]
        period_category_list = period_category_repository.get_period_category_list()
        period_category_dict = {period_category.code: period_category for period_category in period_category_list}
        year_period_id = period_repository.insert_period(
            period=PeriodModel(
                period_category_id=period_category_dict[EnumPeriodCategoryCode.ACADEMIC_YEAR.name].id,
                name=init_data["name"],
                started_on=datetime.strptime(init_data["started_on"], "%Y-%m-%d"),
                ended_on=datetime.strptime(init_data["ended_on"], "%Y-%m-%d"),
            ),
            transaction=trans
        )
        for semester in init_data["semester_list"]:
            period_repository.insert_period(
                period=PeriodModel(
                    period_category_id=period_category_dict[EnumPeriodCategoryCode.SEMESTER.name].id,
                    name=semester["name"],
                    started_on=datetime.strptime(semester["started_on"], "%Y-%m-%d"),
                    ended_on=datetime.strptime(semester["ended_on"], "%Y-%m-%d"),
                    parent_id=year_period_id
                ),
                transaction=trans
            )
