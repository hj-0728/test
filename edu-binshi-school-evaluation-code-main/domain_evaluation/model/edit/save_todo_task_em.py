from typing import List
import re
from infra_basic.basic_model import BasePlusModel


class SaveTodoTaskEditModel(BasePlusModel):
    title_list: List[str]
    trigger_category: str
    trigger_id: str
    assign_category: str
    assign_id: str

    def make_title_beautiful(self):
        beautiful_title_list = []
        for title in self.title_list:
            def replacer(match):
                content = match.group(1)
                styled_content = f'<span style="color: #2d7dc9;font-weight: bold">{content}</span>'
                return f'【{styled_content}】'
            beautiful_title = re.sub(r'【(.*?)】', replacer, title)
            beautiful_title_list.append(beautiful_title)
        self.title_list = beautiful_title_list
