from enum import Enum
from typing import Final

from infra_basic.basic_model import VersionedModel
from infra_basic.basic_resource import BasicResource


class RobotHandlerConst:
    RESOURCE_CATEGORY_ROBOT: Final[str] = "ROBOT"


class EnumRobot(str, Enum):
    SYSTEM = "系统"


class RobotModel(VersionedModel):
    """
    机器人
    """

    name: str
    code: str
    access_key: str
    secret_key: str
    is_activated: bool = True

    def to_basic_handler(self) -> BasicResource:
        return BasicResource(category=RobotHandlerConst.RESOURCE_CATEGORY_ROBOT, id=self.id)
