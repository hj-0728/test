from collections import defaultdict
from typing import List, Optional

from pypinyin import lazy_pinyin

from infra_backbone.model.area_model import AreaModel
from infra_backbone.model.view.initials_group_area_list import InitialsGroupAreaList
from infra_backbone.repository.area_repsoitory import AreaRepository


class AreaService:
    def __init__(self, area_repository: AreaRepository):
        self.__area_repository = area_repository

    def get_area_list_group_by_initials(
        self, parent_id: Optional[str] = None
    ) -> List[InitialsGroupAreaList]:
        """
        获取区域列表
        :param parent_id: 上级领域id，默认为None，为None时查找省级区域
        :return:
        """
        area_list = self.__area_repository.fetch_area_list(parent_id=parent_id)
        result = []
        initials_area_dict = defaultdict(list)
        initials_set = set()
        for area in area_list:
            initials = lazy_pinyin(area.name)[0][0].upper()
            initials_set.add(initials)
            initials_area_dict[initials].append(area)
        for initials in sorted(initials_set):
            result.append(
                InitialsGroupAreaList(initials=initials, area_list=initials_area_dict[initials])
            )
        return result

    def get_area_with_parent_list(self, area_id: str) -> List[AreaModel]:
        """
        获取地域及父级地域列表
        :param area_id:
        :return:
        """
        return self.__area_repository.fetch_area_with_parent_list(area_id=area_id)
