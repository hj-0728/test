from typing import List

from infra_basic.errors import BusinessError
from infra_basic.pagination_carrier import PaginationCarrier

from biz_comprehensive.model.param.student_report_query_params import (
    StudentReportPageFilterParams,
    StudentReportQueryParams,
)
from biz_comprehensive.model.scene_model import SceneModel
from biz_comprehensive.model.view.student_comprehensive_radar_vm import (
    RadarDataViewModel,
    RadarIndicatorViewModel,
    StudentComprehensiveRadarViewModel,
)
from biz_comprehensive.model.view.student_growth_trend_vm import (
    StackedLineDataViewModel,
    StudentGrowthTrendViewModel,
)
from biz_comprehensive.model.view.student_info_vm import StudentInfoViewModel
from biz_comprehensive.model.view.student_observation_point_log_vm import (
    StudentObservationPointLogViewModel,
)
from biz_comprehensive.model.view.student_statistics_vm import StudentStatisticsViewModel
from biz_comprehensive.repository.student_report_repository import StudentReportRepository


class StudentReportService:
    def __init__(self, student_report_repository: StudentReportRepository):
        self.__student_report_repository = student_report_repository

    def get_student_info(self, establishment_assign_id: str) -> StudentInfoViewModel:
        """
        获取学生信息
        """
        student = self.__student_report_repository.fetch_student_info(
            establishment_assign_id=establishment_assign_id
        )
        if not student:
            raise BusinessError("未获取到学生信息")
        return student

    def get_student_statistics(
        self, params: StudentReportQueryParams
    ) -> StudentStatisticsViewModel:
        """
        获取学生统计信息
        """
        data = self.__student_report_repository.fetch_student_statistics(params=params)
        if not data:
            return StudentStatisticsViewModel(total_points=0, total_bright_spot=0, percentage=100)
        return data

    def get_student_comprehensive_radar_data(
        self, params: StudentReportQueryParams
    ) -> StudentComprehensiveRadarViewModel:
        """
        获取学生综合雷达图数据
        """
        source_data_list = self.__student_report_repository.fetch_student_comprehensive_radar_data(
            params=params
        )
        indicator_list = []
        student_data = RadarDataViewModel(name="学生表现", value=[])
        class_data = RadarDataViewModel(name="班级平均", value=[])
        for scene_points in source_data_list:
            # 创建并添加 RadarIndicatorViewModel 到 indicator_list
            indicator = RadarIndicatorViewModel(name=scene_points.scene_name)
            indicator_list.append(indicator)

            student_data.value.append(scene_points.student_total_points)
            class_data.value.append(scene_points.class_avg_points)
        radar_data = StudentComprehensiveRadarViewModel(
            indicator_list=indicator_list, data_list=[student_data, class_data]
        )
        return radar_data

    def get_student_growth_trend_data(
        self, params: StudentReportQueryParams
    ) -> StudentGrowthTrendViewModel:
        """
        获取学生成长趋势数据
        """
        source_data_list = self.__student_report_repository.fetch_student_growth_trend_data(
            params=params
        )
        observation_date_list = []
        student_data = StackedLineDataViewModel(name="学生表现", data=[])
        class_data = StackedLineDataViewModel(name="班级平均", data=[])
        for source_data in source_data_list:
            observation_date_list.append(source_data.observation_on)

            student_data.data.append(source_data.student_total_points)
            class_data.data.append(source_data.class_avg_points)
        line_data = StudentGrowthTrendViewModel(
            observation_date_list=observation_date_list, data_list=[student_data, class_data]
        )
        return line_data

    def get_student_observation_scene_list(
        self, params: StudentReportQueryParams
    ) -> List[SceneModel]:
        """
        获取学生观察场景列表
        """
        return self.__student_report_repository.fetch_student_observation_scene_list(params=params)

    def get_student_observation_point_log_page_list(
        self, params: StudentReportPageFilterParams
    ) -> PaginationCarrier[StudentObservationPointLogViewModel]:
        """
        获取学生观察积分日志分页列表
        """
        return self.__student_report_repository.fetch_student_observation_point_log_page_list(
            params=params
        )
