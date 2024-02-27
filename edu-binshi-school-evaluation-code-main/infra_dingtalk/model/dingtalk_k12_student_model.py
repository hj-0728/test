from typing import List, Optional

from infra_basic.basic_model import BasicModel, VersionedModel

# from biz_integrated.model.points_conversion_log_model import PointsConversionLogModel


class DingtalkK12StudentModel(VersionedModel):
    """
    k12学生
    """

    dingtalk_corp_id: str
    name: str
    remote_user_id: str
    dingtalk_k12_dept_id: Optional[str]
    dingtalk_k12_dept_name: Optional[str]


class DingtalkK12StudentViewModel(BasicModel):
    """
    k12学生列表model
    """

    name: str
    sticker_points: int
    lucky_coin_points: int
    dept_name_list: List[str] = []
    # points_conversion_log_list: List[PointsConversionLogModel] = []
