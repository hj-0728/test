from infra_utility.base_plus_model import BasePlusModel


class StudentUserEm(BasePlusModel):
    """
    学生账号em
    """

    people_id: str
    student_name: str
