"""
角色
"""
from typing import Optional

from infra_basic.errors.input import DataNotFoundError
from infra_basic.transaction import Transaction
from infra_utility.token_helper import generate_md5, generate_uuid_id

from infra_backbone.model.robot_model import EnumRobot, RobotModel
from infra_backbone.repository.robot_repository import RobotRepository


class RobotService:
    """
    角色
    """

    def __init__(
        self,
        robot_repository: RobotRepository,
    ):
        self.__robot_repository = robot_repository

    def prepare_system_robot(self, trans: Transaction):
        current_robot = self.get_system_robot(is_must=False)
        if not current_robot:
            robot = RobotModel(
                name=EnumRobot.SYSTEM.value,
                code=EnumRobot.SYSTEM.name,
                access_key=generate_md5(generate_uuid_id()),
                secret_key=generate_md5(generate_uuid_id()),
            )
            robot_id = self.__robot_repository.insert_robot(data=robot, transaction=trans)
            robot.id = robot_id

    def get_system_robot(self, is_must: bool = True) -> Optional[RobotModel]:
        """
        获取系统级全局机器人，如果没有就新建
        """
        robot_info = self.__robot_repository.get_robot_by_code(
            code=EnumRobot.SYSTEM.name,
        )
        if robot_info:
            return robot_info
        if not robot_info and is_must:
            raise DataNotFoundError("未获取到系统级全局机器人")
        return None
