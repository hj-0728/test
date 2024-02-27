from typing import List, Optional

from infra_basic.basic_repository import PageFilterParams

from infra_backbone.model.people_model import EnumPeopleGender


class PeoplePageQueryParams(PageFilterParams):
    """
    人员列表 查询条件
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.gender_list is None:
            self.gender_list = [
                EnumPeopleGender.MALE.name,
                EnumPeopleGender.FEMALE.name,
            ]

    dimension_dept_tree_id: Optional[str]
    gender_list: Optional[List[str]] = [
        EnumPeopleGender.MALE.name,
        EnumPeopleGender.FEMALE.name,
    ]
    organization_id: Optional[str]
    dimension_id: Optional[str]
    not_show_children: bool = False
