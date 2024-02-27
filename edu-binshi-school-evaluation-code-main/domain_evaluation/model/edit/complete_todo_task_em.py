from typing import Optional
from datetime import datetime

from infra_basic.basic_model import BasePlusModel


class CompleteTodoTaskEditModel(BasePlusModel):

    id: str
    version: int
    completed_by: Optional[str]
    completed_at: Optional[datetime]
