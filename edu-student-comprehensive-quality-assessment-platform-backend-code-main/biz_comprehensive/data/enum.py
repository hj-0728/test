from enum import Enum


class EnumDictMetaCode(Enum):
    """
    字典元数据 code
    """

    SYSTEM_COMMEND_OBSERVATION_POINT_ICON = "系统表扬观测点图标"
    SYSTEM_TO_BE_IMPROVED_OBSERVATION_POINT_ICON = "系统待改进观测点图标"
    STUDENT_DEFAULT_AVATAR = "学生默认头像"
    TEACHER_DEFAULT_AVATAR = "教师默认头像"
    DEPT_DEFAULT_AVATAR = "部门默认头像"


class EnumComprehensiveResource(Enum):
    """
    biz_comprehensive 资源
    """

    OBSERVATION_POINT = "观测点"
    POINTS_LOG = "积分日志"
    INDICATOR_SCORE_LOG = "指标得分日志"
    MEDAL_ISSUE_LOG = "勋章颁发"
    OBSERVATION_POINT_LOG = "观测点日志"
    OBSERVATION_ACTION = "观测点动作"
