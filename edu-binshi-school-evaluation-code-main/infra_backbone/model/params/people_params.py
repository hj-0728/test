from typing import List, Optional

from infra_basic.query_params import PageFilterParams

from infra_backbone.model.people_model import EnumPeopleGender


class PeopleQueryParams(PageFilterParams):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.gender_list is None:
            self.gender_list = [
                EnumPeopleGender.MALE.name,
                EnumPeopleGender.FEMALE.name,
            ]

    name: Optional[str]
    gender_list: Optional[List[str]] = [
        EnumPeopleGender.MALE.name,
        EnumPeopleGender.FEMALE.name,
    ]
