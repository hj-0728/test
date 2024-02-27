from infra_basic.basic_model import BasePlusModel


class TokenViewModel(BasePlusModel):
    access_token: str
    refresh_token: str
