from infra_basic.basic_model import BasicModel


class TeamCanSelectPeopleViewModel(BasicModel):
    """
    小组可选人员
    """

    id: str
    people_id: str
    people_name: str
    dept_name: str
    capacity_id: str
    capacity_name: str
