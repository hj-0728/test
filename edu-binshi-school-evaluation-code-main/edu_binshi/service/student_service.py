from typing import List

from infra_basic.errors import BusinessError
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.transaction import Transaction

from edu_binshi.data.constant import EduBinShiDictConst
from edu_binshi.data.query_params.student_query_params import StudentPageQueryParams
from edu_binshi.model.edit.student_user_em import StudentUserEm
from edu_binshi.model.view.student_page_vm import StudentPageVm
from edu_binshi.model.view.student_user_page_vm import StudentUserPageVm
from edu_binshi.repository.student_repository import StudentRepository
from infra_backbone.data.constant import DimensionCodeConst, OrganizationCodeConst
from infra_backbone.model.dimension_model import EnumDimensionCategory
from infra_backbone.model.role_model import EnumRoleCode
from infra_backbone.model.user_model import UserModel
from infra_backbone.repository.dict_repository import DictRepository
from infra_backbone.repository.role_repository import RoleRepository
from infra_backbone.service.dimension_service import DimensionService
from infra_backbone.service.user_service import UserService


class StudentService:
    def __init__(
        self,
        student_repository: StudentRepository,
        dimension_service: DimensionService,
        user_service: UserService,
        role_repository: RoleRepository,
        dict_repository: DictRepository,
    ):
        self.__student_repository = student_repository
        self.__dimension_service = dimension_service
        self.__user_service = user_service
        self.__role_repository = role_repository
        self.__dict_repository = dict_repository

    def get_student_page(
        self,
        params: StudentPageQueryParams,
    ) -> PaginationCarrier[StudentPageVm]:
        """
        获取学生分页
        :return:
        """

        dimension = self.__dimension_service.get_dimension_by_organization_code_and_category_code(
            dimension_code=DimensionCodeConst.DINGTALK_EDU,
            dimension_category=EnumDimensionCategory.EDU.name,
            organization_code=OrganizationCodeConst.BJSYXX,
        )

        params.dimension_id = dimension.id
        return self.__student_repository.get_student_page(params=params)

    def get_student_info_list_by_establishment_assign_id_list(
        self, establishment_assign_id_list: List[str]
    ):
        """
        根据编制分配id列表获取学生信息
        """

        dimension = self.__dimension_service.get_dimension_by_organization_code_and_category_code(
            dimension_code=DimensionCodeConst.DINGTALK_EDU,
            dimension_category=EnumDimensionCategory.EDU.name,
            organization_code=OrganizationCodeConst.BJSYXX,
        )

        return self.__student_repository.get_student_info_list_by_establishment_assign_id_list(
            establishment_assign_id_list=establishment_assign_id_list, dimension_id=dimension.id
        )

    def get_student_user_page(
        self,
        params: StudentPageQueryParams,
    ) -> PaginationCarrier[StudentUserPageVm]:
        """
        获取学生用户分页
        :return:
        """

        dimension = self.__dimension_service.get_dimension_by_organization_code_and_category_code(
            dimension_code=DimensionCodeConst.DINGTALK_EDU,
            dimension_category=EnumDimensionCategory.EDU.name,
            organization_code=OrganizationCodeConst.BJSYXX,
        )

        params.dimension_id = dimension.id

        return self.__student_repository.get_student_user_page(params=params)

    def create_student_user(self, student_user: StudentUserEm, transaction: Transaction):
        """
        创建学生用户
        :param student_user:
        :param transaction:
        :return:
        """

        role = self.__role_repository.get_role_by_code(code=EnumRoleCode.STUDENT.name)

        student_password_info = self.get_student_init_password()

        # 处理学生用户名
        student_name = self.get_student_user_name(
            student_user=student_user,
        )

        user = UserModel(
            people_id=student_user.people_id,
            name=student_name,
            password=student_password_info,
            role_id_list=[role.id],
        )

        self.__user_service.add_user(
            user=user,
            transaction=transaction,
        )

    def get_student_user_name(
        self, student_user: StudentUserEm, student_name_list: List[str] = None
    ) -> str:
        """
        获取学生用户名(处理重名)
        判断st_user 表中是否已经出现此用户名，若出现了加上家长手机号后四位
        :param student_user:
        :param student_name_list: 没有保存到数据库的学生用户名列表
        :return:
        """

        user = self.__user_service.get_user_by_name(name=student_user.student_name)

        if not user and (
            not student_name_list or student_user.student_name not in student_name_list
        ):
            return student_user.student_name

        # 学生用户名已存在，加上家长手机号后四位

        parent_list = self.__student_repository.get_student_parent(people_id=student_user.people_id)

        if parent_list and parent_list[0].phone_detail:
            return f"{student_user.student_name}_{parent_list[0].phone_detail[-4:]}"

        return f"{student_user.student_name}_{student_user.people_id[-4:]}"

    def batch_create_student_user(self, params: StudentPageQueryParams, transaction: Transaction):
        """
        批量创建学生用户
        :param params:
        :param transaction:
        :return:
        """

        params.page_size = 100000
        params.page_index = 0

        student_user_page = self.get_student_user_page(params=params)

        role = self.__role_repository.get_role_by_code(code=EnumRoleCode.STUDENT.name)

        student_password_info = self.get_student_init_password()

        student_name_list = []

        for student_user in student_user_page.data:
            if not student_user.user:
                # 处理学生用户名
                student_name = self.get_student_user_name(
                    student_user=StudentUserEm(
                        people_id=student_user.people_id,
                        student_name=student_user.student_name,
                    ),
                    student_name_list=student_name_list,
                )

                student_name_list.append(student_name)

                user = UserModel(
                    people_id=student_user.people_id,
                    name=student_name,
                    password=student_password_info,
                    role_id_list=[role.id],
                )

                self.__user_service.add_user(
                    user=user,
                    transaction=transaction,
                )

    def get_student_init_password(self) -> str:
        """
        获取学生初始密码
        """
        student_password_info = self.__dict_repository.get_dict_by_meta_code_and_dict_data_code(
            dict_meta_code=EduBinShiDictConst.ACCOUNT,
            dict_data_code=EduBinShiDictConst.STUDENT_INIT_ACCOUNT,
        )
        if not student_password_info:
            raise BusinessError("学生初始密码不存在")
        return student_password_info.value
