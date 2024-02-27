from typing import Optional

from infra_basic.basic_model import BasePlusModel


class DeptTreeQueryParams(BasePlusModel):
    dimension_code: str
    category: str
    organization_id: str
    search_text: Optional[str]
    is_available: Optional[bool]
