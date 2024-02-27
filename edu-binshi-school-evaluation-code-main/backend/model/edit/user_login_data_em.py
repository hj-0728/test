from infra_basic.basic_model import BasePlusModel


class UserLoginDataEditModel(BasePlusModel):
    name: str
    password: str
    validate_image_src: str
    validate_code: str
