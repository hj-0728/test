from typing import Optional

from infra_basic.basic_model import BasicModel


class FileViewModel(BasicModel):
    id: Optional[str]
    file_url: Optional[str]
