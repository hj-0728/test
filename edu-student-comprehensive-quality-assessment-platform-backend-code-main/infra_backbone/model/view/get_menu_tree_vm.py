from typing import Optional

from infra_basic.basic_model import BasePlusModel


class GetMenuTreeViewModel(BasePlusModel):
    menu_category: str
    search_text: Optional[str]
