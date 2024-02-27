from enum import Enum
from typing import List

from infra_basic.basic_model import BasePlusModel


class EnumTriggerCategory(str, Enum):
    TEAM_CATEGORY = "team_category_id"
    SUBJECT = "subject_id"
    CONTEXT_SYNC = "context_sync"


class CommandGenerateInputScoreLogEditModel(BasePlusModel):
    trigger_category: str
    trigger_ids: List[str] = []
