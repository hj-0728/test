from enum import Enum

from infra_basic.basic_model import VersionedModel


class EnumLogClueLogResCategory(Enum):
    """
    日志的线索日志资源的category
    """

    POINTS_LOG = "points_log"
    INDICATOR_SCORE_LOG = "indicator_score_log"
    MEDAL_ISSUE_LOG = "medal_issue_log"


class EnumLogClueClueResCategory(Enum):
    """
    日志的线索线索资源的category
    """

    CALC_LOG = "calc_log"


class LogClueModel(VersionedModel):
    """
    日志的线索
    """

    log_res_category: str
    log_res_id: str
    clue_res_category: str
    clue_res_id: str
