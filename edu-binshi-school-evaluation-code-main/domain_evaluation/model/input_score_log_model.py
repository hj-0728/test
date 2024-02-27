from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import Field

from infra_basic.basic_model import VersionedModel
from infra_utility.datetime_helper import local_now

from domain_evaluation.model.edit.input_score_log_em import InputScoreLogEditModel


class EnumFillerCategory(Enum):
    """
    填写人目前只有people，filler_id为people_id
    """

    PEOPLE = "人员"


class EnumExpectedFillerCategory(Enum):
    """
    教师、学生、家长
    """

    ESTABLISHMENT_ASSIGN = "编制分配"  # 教师，学生
    PEOPLE_RELATIONSHIP = "人员关系"  # 家长
    TEAM = "小组"


class EnumInputScoreLogStatus(Enum):
    """
    状态
    """

    READY = "准备中"
    SUBMITTED = "已提交"


class InputScoreLogModel(VersionedModel):
    """
    输入分数的日志
    """

    evaluation_assignment_id: str
    benchmark_input_node_id: str
    generated_at: datetime = Field(default_factory=local_now)
    expected_filler_category: str
    expected_filler_id: str
    filler_category: Optional[str]
    filler_id: Optional[str]
    fill_start_at: datetime
    fill_finish_at: datetime
    filled_at: Optional[datetime]
    numeric_score: Optional[float]
    string_score: Optional[str]
    status: str
    comments: Optional[str]

    def to_update_data(self, input_score_log_em: InputScoreLogEditModel):
        self.version = input_score_log_em.version
        self.filler_id = input_score_log_em.people_id
        self.filler_category = EnumFillerCategory.PEOPLE.name
        self.filled_at = local_now()
        self.numeric_score = input_score_log_em.numeric_score
        self.string_score = input_score_log_em.string_score

