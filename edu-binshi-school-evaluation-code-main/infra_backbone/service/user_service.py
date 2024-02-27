import re
from typing import List, Optional

from infra_basic.errors import BusinessError
from infra_basic.errors.input import DataNotFoundError
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.transaction import Transaction
from infra_utility import encryption_helper
from infra_utility.encryption_helper import encrypt_md5
from infra_utility.token_helper import generate_random_string

from infra_backbone.model.edit.user_password_em import (
    ImproveUserPasswordEditModel,
    UserPasswordEditModel,
)
from infra_backbone.model.params.user_params import UserQueryParams
from infra_backbone.model.people_model import PeopleUserModel
from infra_backbone.model.role_model import EnumRoleCode
from infra_backbone.model.user_model import UserModel
from infra_backbone.model.user_role_model import UserRoleModel
from infra_backbone.model.view.user_vm import UserViewModel
from infra_backbone.repository.people_user_repository import PeopleUserRepository
from infra_backbone.repository.role_repository import RoleRepository
from infra_backbone.repository.user_repository import UserRepository
from infra_backbone.repository.user_role_repository import UserRoleRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        user_role_repository: UserRoleRepository,
        people_user_repository: PeopleUserRepository,
    ):
        self.__user_repository = user_repository
        self.__role_repository = role_repository
        self.__user_role_repository = user_role_repository
        self.__people_user_repository = people_user_repository

    def verify_user_name_and_password(
        self, name: str, password: str, transaction: Transaction
    ) -> UserModel:
        """
        验证用户、密码信息
        :param name:
        :param password:
        :param transaction:
        :return:
        """
        user_info = self.__user_repository.get_user_by_name(name=name)
        if not user_info:
            raise BusinessError("用户名或密码错误")
        if not user_info.is_activated:
            raise BusinessError("用户已被禁用")
        if user_info.try_count is None:
            user_info.try_count = 0
        cur_password = encrypt_md5(password, user_info.salt)
        if cur_password == user_info.password:
            if user_info.try_count != 0:
                user_info.try_count = 0
                self.__user_repository.update_user(
                    data=user_info,
                    limited_col_list=["try_count"],
                    transaction=transaction,
                )
        else:
            user_info.try_count += 1
            self.__user_repository.update_user(
                data=user_info,
                limited_col_list=["try_count"],
                transaction=transaction,
            )
            raise BusinessError("用户名或密码错误")
        return user_info

    def add_user(
        self,
        user: UserModel,
        transaction: Transaction,
    ) -> str:
        """
        添加用户信息
        :param user:
        :param transaction:
        :return:
        """
        if not user.name:
            raise DataNotFoundError("用户名不能为空")
        exist_user_info = self.__user_repository.get_user_by_name(
            name=user.name,
        )
        if exist_user_info:
            raise BusinessError("此用户名已被注册")
        if user.password:
            password_check = re.compile("[\u4e00-\u9fa5]").search(user.password)
            if password_check:
                raise BusinessError("密码不能包含中文")
        password_reg = r"(?=.*?\d)(?=.*?[a-zA-Z])(?=.*?[^\w\s]|.*?[_]).{8,30}"
        password_check = re.match(password_reg, user.password)
        if not password_check:
            raise BusinessError("密码必须包含字母、数字、特殊字符，至少8个字符，最多30个字符")
        if not user.role_id_list:
            raise BusinessError("请选择对应角色")
        salt = encryption_helper.generate_salt()
        cur_password = encryption_helper.encrypt_md5(user.password, salt)
        user.password = cur_password
        user.salt = salt
        user_id = self.__user_repository.insert_user(
            data=user,
            transaction=transaction,
        )
        for role_id in user.role_id_list:
            self.__user_role_repository.insert_user_role(
                data=UserRoleModel(
                    user_id=user_id,
                    role_id=role_id,
                ),
                transaction=transaction,
            )

        if user.people_id:
            self.__people_user_repository.insert_people_user(
                data=PeopleUserModel(
                    people_id=user.people_id,
                    user_id=user_id,
                ),
                transaction=transaction,
            )
        return user_id

    def get_user_info(self, user_id: str, role_id: str) -> UserViewModel:
        """
        获取用户信息
        :param user_id:
        :param role_id:
        :return:
        """
        user_info = self.__user_repository.get_user_by_id(user_id=user_id)
        if not user_info:
            raise DataNotFoundError("未获取到用户信息")
        role_list = self.__role_repository.get_role_list_by_user_id(user_id=user_id)
        if not role_list:
            raise DataNotFoundError("未获取到用户角色信息")
        current_role = [x for x in role_list if x.id == role_id][0]
        user_detail = user_info.cast_to(
            cast_type=UserViewModel,
            role_id=role_id,
            role_name=current_role.name,
            role_code=current_role.code,
        )
        user_detail.current_role = current_role
        user_detail.role_list = role_list
        # 其实不应该写在这里面，只不过系统里面这种情况已经无法拯救了，将错就错吧……
        user_detail.home_path = "/home"
        if current_role.code == EnumRoleCode.STUDENT.name:
            user_detail.home_path = "/evaluation-record/about-me"
        elif current_role.code == EnumRoleCode.TEACHER.name:
            user_detail.home_path = "/evaluation-record/todo-list"
        return user_detail

    def change_user_password(
        self,
        user_password: UserPasswordEditModel,
        transaction: Transaction,
        user_id: str,
    ) -> bool:
        """
        修改用户密码
        :param user_password:
        :param transaction:
        :param user_id:
        :return:
        """
        password = user_password.password.strip()
        new_password = user_password.new_password.strip()
        verify_new_password = user_password.verify_new_password.strip()

        if password == "":
            raise BusinessError("请输入原密码")

        if new_password:
            password_check = re.compile("[\u4e00-\u9fa5]").search(new_password)
            if password_check:
                raise BusinessError("密码不能包含中文")
        else:
            raise BusinessError("请输入新密码")
        if new_password != verify_new_password:
            raise BusinessError("新密码和确认密码不一致")
        if password == new_password:
            raise BusinessError("输入的原密码与新密码一致")

        password_reg = r"(?=.*?\d)(?=.*?[a-zA-Z])(?=.*?[^\w\s]|.*?[_]).{8,30}"
        password_check = re.match(password_reg, new_password)
        if not password_check:
            raise BusinessError("密码必须包含字母、数字、特殊字符，至少8个字符，最多30个字符")
        master_user = self.__user_repository.get_user_by_id(user_id=user_id)
        if not master_user:
            raise DataNotFoundError("未获取到用户信息")
        if master_user.try_count is None:
            master_user.try_count = 0
        before_password = encryption_helper.encrypt_md5(clear_text=password, salt=master_user.salt)
        master_user.salt = encryption_helper.generate_salt()
        if before_password == master_user.password:
            master_user.try_count = 0
            cur_new_password = encryption_helper.encrypt_md5(new_password, master_user.salt)
            master_user.password = cur_new_password
            master_user.password_reset = False
            self.__user_repository.update_user(
                data=master_user,
                transaction=transaction,
                limited_col_list=["password", "salt", "try_count", "password_reset"],
            )
            return True
        master_user.try_count += 1
        self.__user_repository.update_user(
            data=master_user,
            transaction=transaction,
            limited_col_list=["try_count"],
        )
        raise BusinessError("原密码错误")

    def get_user_list(
        self,
        params: UserQueryParams,
    ) -> PaginationCarrier[UserModel]:
        """
        获取用户列表
        """
        return self.__user_repository.get_user_list(
            params=params,
        )

    def edit_user(
        self,
        data: UserModel,
        transaction: Transaction,
    ):
        """
        编辑用户信息
        """
        if not data.name:
            raise DataNotFoundError("用户名不能为空")
        is_exist = self.__user_repository.get_same_user_name(name=data.name, user_id=data.id)
        if is_exist:
            raise BusinessError("用户名已经存在，重新输入")
        user = self.__user_repository.get_user_by_id(user_id=data.id)
        if not user:
            raise DataNotFoundError("用户不存在")
        user.name = data.name
        self.__user_repository.update_user(
            data=user, transaction=transaction, limited_col_list=["name"]
        )
        self.update_user_role(
            user_id=data.id, role_id_list=data.role_id_list, transaction=transaction
        )

    def update_user_role(self, user_id: str, role_id_list: List[str], transaction: Transaction):
        """
        更新用户的角色
        :param user_id:
        :param role_id_list:
        :param transaction:
        :return:
        """
        user_role_list = self.__user_role_repository.get_user_role_list_by_user_id(
            user_id=user_id,
        )
        for user_role in user_role_list:
            if user_role.role_id not in role_id_list:
                self.__user_role_repository.delete_user_role(
                    user_role_id=user_role.id,
                    transaction=transaction,
                )
            else:
                role_id_list.remove(user_role.role_id)
        for new_role_id in role_id_list:
            self.__user_role_repository.insert_user_role(
                data=UserRoleModel(
                    user_id=user_id,
                    role_id=new_role_id,
                ),
                transaction=transaction,
            )

    def reset_password(
        self,
        data: UserModel,
        transaction: Transaction,
        new_password: str = None
    ) -> str:
        """
        重置密码
        """
        if not new_password:
            new_password = generate_random_string(size=8)
        salt = encryption_helper.generate_salt()
        init_password = encryption_helper.encrypt_md5(new_password, salt)
        data.salt = salt
        data.password = init_password
        data.password_reset = True
        self.__user_repository.update_user(
            data=data,
            transaction=transaction,
            limited_col_list=["password", "salt", "password_reset"],
        )
        return new_password

    def improve_user_password(
        self,
        user_password: ImproveUserPasswordEditModel,
        transaction: Transaction,
        user_id: str,
    ):
        """
        完善用户密码
        :param user_password:
        :param transaction:
        :param user_id:
        :return:
        """
        new_password = user_password.new_password.strip()
        verify_new_password = user_password.verify_new_password.strip()

        if new_password:
            password_check = re.compile("[\u4e00-\u9fa5]").search(new_password)
            if password_check:
                raise BusinessError("密码不能包含中文")
        else:
            raise BusinessError("请输入新密码")
        if new_password != verify_new_password:
            raise BusinessError("新密码和确认密码不一致")

        password_reg = r"(?=.*?\d)(?=.*?[a-zA-Z])(?=.*?[^\w\s]|.*?[_]).{8,30}"
        password_check = re.match(password_reg, new_password)
        if not password_check:
            raise BusinessError("密码必须包含字母、数字、特殊字符，至少8个字符，最多30个字符")
        master_user = self.__user_repository.get_user_by_id(user_id=user_id)
        if not master_user:
            raise DataNotFoundError("未获取到用户信息")
        if master_user.password == encryption_helper.encrypt_md5(new_password, master_user.salt):
            raise BusinessError("新密码不能与原密码一致")
        master_user.salt = encryption_helper.generate_salt()
        master_user.try_count = 0
        cur_new_password = encryption_helper.encrypt_md5(new_password, master_user.salt)
        master_user.password = cur_new_password
        master_user.password_reset = False
        self.__user_repository.update_user(
            data=master_user,
            transaction=transaction,
            limited_col_list=["password", "salt", "try_count", "password_reset"],
        )

    def update_user_activated(
        self,
        user: UserModel,
        transaction: Transaction,
    ):
        """
        启用、禁用用户
        :param user:
        :param transaction:
        :return:
        """
        self.__user_repository.update_user(
            data=user, transaction=transaction, limited_col_list=["is_activated"]
        )

    def get_user_list_by_people_id_list(self, people_id_list: List[str]) -> List[UserModel]:
        """
        根据人员id列表获取用户列表
        :param people_id_list:
        :return:
        """

        return self.__user_repository.get_user_list_by_people_id_list(people_id_list=people_id_list)

    def get_user_by_name(self, name: str) -> Optional[UserModel]:
        """
        根据用户名获取用户信息
        :param name:
        :return:
        """
        return self.__user_repository.get_user_by_name(name=name)
