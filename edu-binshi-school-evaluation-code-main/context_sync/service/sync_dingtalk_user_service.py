import glob
import random
from typing import Dict, List

from infra_basic.basic_resource import BasicResource
from infra_basic.transaction import Transaction
from infra_object_storage.service.object_storage_service import ObjectStorageService
from infra_utility.enum_helper import get_enum_value_by_name
from infra_utility.file_helper import build_abs_path_by_file
from infra_utility.token_helper import generate_uuid_id

from context_sync.data.enum import EnumFileRelationship, EnumResource
from context_sync.model.context_people_user_map_model import (
    ContextPeopleUserMapModel,
    EnumContextPeopleUserMapResCategory,
)
from context_sync.model.view.context_people_user_detail_vm import (
    ContextPeopleStudentDetailViewModel,
    ContextPeopleUserDetailViewModel,
)
from context_sync.repository.context_people_user_map_repository import (
    ContextPeopleUserMapRepository,
)
from infra_backbone.model.capacity_model import EnumCapacityCode
from infra_backbone.model.contact_info_model import ContactInfoModel, EnumContactInfoCategory
from infra_backbone.model.dimension_model import EnumDimensionCategory
from infra_backbone.model.edit.add_people_em import (
    AddPeopleViewModel,
    EstablishmentAssignViewModel,
    PeopleRelationshipViewModel,
)
from infra_backbone.model.people_model import PeopleModel
from infra_backbone.model.resource_contact_info_model import ResourceContactInfoModel
from infra_backbone.service.contact_info_service import ContactInfoService
from infra_backbone.service.people_service import PeopleService
from infra_dingtalk.model.dingtalk_user_model import DingtalkUserModel
from infra_dingtalk.model.view.dingtalk_k12_parent_vm import DingtalkK12ParentViewModel
from infra_dingtalk.model.view.dingtalk_k12_student_info_vm import DingtalkK12StudentInfoViewModel
from infra_dingtalk.repository.dingtalk_k12_parent_repository import DingtalkK12ParentRepository
from infra_dingtalk.repository.dingtalk_k12_student_repository import DingtalkK12StudentRepository
from infra_dingtalk.repository.dingtalk_user_repository import DingtalkUserRepository


class SyncDingtalkUserService:
    def __init__(
        self,
        context_people_user_map_repository: ContextPeopleUserMapRepository,
        dingtalk_k12_parent_repository: DingtalkK12ParentRepository,
        dingtalk_k12_student_repository: DingtalkK12StudentRepository,
        dingtalk_user_repository: DingtalkUserRepository,
        people_service: PeopleService,
        object_storage_service: ObjectStorageService,
        contact_info_service: ContactInfoService,
    ):
        self.__context_people_user_map_repository = context_people_user_map_repository
        self.__dingtalk_k12_parent_repository = dingtalk_k12_parent_repository
        self.__dingtalk_k12_student_repository = dingtalk_k12_student_repository
        self.__dingtalk_user_repository = dingtalk_user_repository
        self.__people_service = people_service
        self.__object_storage_service = object_storage_service
        self.__contact_info_service = contact_info_service

    def sync_dingtalk_parent_and_student(
        self,
        dingtalk_corp_id: str,
        organization_id: str,
        context_dept_map: Dict[str, str],
        transaction: Transaction,
    ):
        """
        同步钉钉学生和家长
        :param dingtalk_corp_id:
        :param organization_id:
        :param context_dept_map:
        :param transaction:
        :return:
        """
        # 同步家长
        context_people_parent_map = self.sync_dingtalk_parent(
            dingtalk_corp_id=dingtalk_corp_id, transaction=transaction
        )

        # 同步学生
        self.sync_dingtalk_student(
            dingtalk_corp_id=dingtalk_corp_id,
            organization_id=organization_id,
            context_dept_map=context_dept_map,
            context_people_parent_map=context_people_parent_map,
            transaction=transaction,
        )

    def sync_dingtalk_inner_people(
        self,
        dingtalk_corp_id: str,
        organization_id: str,
        context_dept_map: Dict[str, str],
        context_k12_dept_map: Dict[str, str],
        transaction: Transaction,
    ):
        """
        同步钉钉人员
        :param dingtalk_corp_id:
        :param organization_id:
        :param context_dept_map:
        :param context_k12_dept_map:
        :param transaction:
        :return:
        """
        dingtalk_user_list = self.__dingtalk_user_repository.get_corp_all_dingtalk_user(
            dingtalk_corp_id=dingtalk_corp_id
        )
        context_inner_people_list = (
            self.__context_people_user_map_repository.fetch_context_people_detail_by_corp_id(
                dingtalk_corp_id=dingtalk_corp_id
            )
        )
        user_id_list = [x.id for x in dingtalk_user_list]

        context_res_user_id_list = [x.res_id for x in context_inner_people_list]

        # 不在 上下文，添加

        add_context_people_map = self.__add_inner_people(
            dingtalk_user_list=dingtalk_user_list,
            organization_id=organization_id,
            context_res_user_id_list=context_res_user_id_list,
            context_dept_map=context_dept_map,
            context_k12_dept_map=context_k12_dept_map,
            transaction=transaction,
        )

        # 在 k12 ，在 上下文，判断是否需要修改

        context_people_map = {x.res_id: x.people_id for x in context_inner_people_list}

        context_people_map |= add_context_people_map

        self.__update_dingtalk_people(
            dingtalk_user_list=dingtalk_user_list,
            organization_id=organization_id,
            context_people_list=context_inner_people_list,
            context_dept_map=context_dept_map,
            context_k12_dept_map=context_k12_dept_map,
            dimension_category=EnumDimensionCategory.ADMINISTRATION.name,
            transaction=transaction,
        )

        # 不在的禁用

        self.__remove_people(
            user_id_list=user_id_list,
            context_people_list=context_inner_people_list,
            transaction=transaction,
        )

    def sync_dingtalk_parent(
        self, dingtalk_corp_id: str, transaction: Transaction
    ) -> Dict[str, str]:
        """
        同步家长
        :param dingtalk_corp_id:
        :param transaction:
        :return:
        """
        k12_parent_list = self.__dingtalk_k12_parent_repository.get_dingtalk_k12_parent_by_corp_id(
            dingtalk_corp_id=dingtalk_corp_id
        )

        context_parent_list = (
            self.__context_people_user_map_repository.fetch_context_people_parent_detail_by_corp_id(
                dingtalk_corp_id=dingtalk_corp_id
            )
        )

        k12_parent_id_list = [x.id for x in k12_parent_list]

        context_res_user_id_list = [x.res_id for x in context_parent_list]

        # 不在的禁用

        self.__remove_people(
            user_id_list=k12_parent_id_list,
            context_people_list=context_parent_list,
            transaction=transaction,
        )

        # 在 k12 ，不在 上下文，添加

        add_context_people_parent_map = self.__add_k12_parent(
            k12_parent_list=k12_parent_list,
            context_res_user_id_list=context_res_user_id_list,
            transaction=transaction,
        )

        # 在 k12 ，在 上下文，判断是否需要修改

        context_people_parent_map = {x.res_id: x.people_id for x in context_parent_list}

        context_people_parent_map |= add_context_people_parent_map

        self.__update_k12_parent(
            k12_parent_list=k12_parent_list,
            context_parent_list=context_parent_list,
            transaction=transaction,
        )

        return context_people_parent_map

    def __remove_people(
        self,
        user_id_list: List[str],
        context_people_list: List[ContextPeopleUserDetailViewModel],
        transaction: Transaction,
    ):
        """
        禁用删除的people
        :param user_id_list:
        :param context_people_list:
        :param transaction:
        :return:
        """

        for context_people in context_people_list:
            if context_people.res_id not in user_id_list:
                if not context_people.dingtalk_user_id:
                    self.__people_service.update_people(
                        people=PeopleModel(
                            id=context_people.people_id,
                            version=context_people.people_version,
                            name=context_people.name,
                            is_available=False,
                        ),
                        transaction=transaction,
                        limited_col_list=["is_available"],
                    )
                self.__context_people_user_map_repository.delete_context_people_user_map(
                    context_people_user_map_id=context_people.id, transaction=transaction
                )

    def __add_k12_parent(
        self,
        k12_parent_list: List[DingtalkK12ParentViewModel],
        context_res_user_id_list: List[str],
        transaction: Transaction,
    ) -> Dict[str, str]:
        """
        添加k12家长
        :param k12_parent_list:
        :param context_res_user_id_list:
        :param transaction:
        :return:
        """

        need_add_people_dict = {}

        for k12_parent in k12_parent_list:
            if k12_parent.id not in context_res_user_id_list:
                data = AddPeopleViewModel(
                    id=generate_uuid_id(),
                    mobile=k12_parent.mobile,
                    name=k12_parent.name,
                    remote_user_id=k12_parent.remote_user_id,
                )
                need_add_people_dict[k12_parent.id] = data
        context_parent_map = {}
        for k12_parent_id, people_em in need_add_people_dict.items():
            people_id = self.__people_service.add_people_info(
                people=people_em, transaction=transaction
            )
            self.__context_people_user_map_repository.insert_context_people_user_map(
                context_org_corp_map=ContextPeopleUserMapModel(
                    people_id=people_id,
                    res_category=EnumContextPeopleUserMapResCategory.DINGTALK_K12_PARENT.name,
                    res_id=k12_parent_id,
                ),
                transaction=transaction,
            )
            context_parent_map[k12_parent_id] = people_em.id

        return context_parent_map

    def __update_k12_parent(
        self,
        k12_parent_list: List[DingtalkK12ParentViewModel],
        context_parent_list: List[ContextPeopleUserDetailViewModel],
        transaction: Transaction,
    ):
        k12_parent_dict = {x.id: x for x in k12_parent_list}

        for parent in context_parent_list:
            k12_parent = k12_parent_dict.get(parent.res_id)
            if k12_parent:
                if k12_parent.name != parent.name and not parent.dingtalk_user_id:
                    self.__people_service.update_people(
                        people=PeopleModel(
                            id=parent.people_id,
                            version=parent.people_version,
                            name=k12_parent.name,
                            is_available=True,
                        ),
                        transaction=transaction,
                        limited_col_list=["name", "is_available"],
                    )
                if k12_parent.mobile:
                    self.__contact_info_service.save_resource_contact_info(
                        data=ResourceContactInfoModel(
                            resource_id=parent.people_id,
                            resource_category=EnumResource.PEOPLE.name,
                            contact_info_list=[
                                ContactInfoModel(
                                    category=EnumContactInfoCategory.PHONE.name,
                                    detail=k12_parent.mobile,
                                )
                            ],
                        ),
                        transaction=transaction,
                    )

    def sync_dingtalk_student(
        self,
        dingtalk_corp_id: str,
        organization_id: str,
        context_dept_map: Dict[str, str],
        context_people_parent_map: Dict[str, str],
        transaction: Transaction,
    ):
        """
        同步学生、学生班级、学生家长关系
        :param dingtalk_corp_id:
        :param organization_id:
        :param context_dept_map:
        :param context_people_parent_map:
        :param transaction:
        :return:
        """

        k12_student_list = self.__dingtalk_k12_student_repository.fetch_dingtalk_k12_student_info(
            dingtalk_corp_id=dingtalk_corp_id
        )

        context_student_list = self.__context_people_user_map_repository.fetch_context_people_student_detail_by_corp_id(
            dingtalk_corp_id=dingtalk_corp_id
        )

        k12_student_id_list = [x.id for x in k12_student_list]

        context_res_user_id_list = [x.res_id for x in context_student_list]

        # 不在的禁用

        self.__remove_people(
            user_id_list=k12_student_id_list,
            context_people_list=context_student_list,
            transaction=transaction,
        )

        # 在 k12 ，不在 上下文，添加

        add_context_people_student_map = self.__add_k12_student(
            k12_student_list=k12_student_list,
            organization_id=organization_id,
            context_res_user_id_list=context_res_user_id_list,
            context_dept_map=context_dept_map,
            context_people_parent_map=context_people_parent_map,
            transaction=transaction,
        )

        # 在 k12 ，在 上下文，判断是否需要修改

        context_people_student_map = {x.res_id: x.people_id for x in context_student_list}

        context_people_student_map |= add_context_people_student_map

        self.__update_k12_student(
            k12_student_list=k12_student_list,
            organization_id=organization_id,
            context_student_list=context_student_list,
            context_dept_map=context_dept_map,
            context_people_parent_map=context_people_parent_map,
            transaction=transaction,
        )

        return context_people_student_map

    def __add_k12_student(
        self,
        k12_student_list: List[DingtalkK12StudentInfoViewModel],
        organization_id: str,
        context_res_user_id_list: List[str],
        context_dept_map: Dict[str, str],
        context_people_parent_map: Dict[str, str],
        transaction: Transaction,
    ) -> Dict[str, str]:
        """
        添加学生
        :param k12_student_list:
        :param organization_id:
        :param context_res_user_id_list:
        :param context_dept_map:
        :param context_people_parent_map:
        :param transaction:
        :return:
        """

        need_add_people_dict = {}

        for k12_student in k12_student_list:
            if k12_student.id not in context_res_user_id_list:
                new_people_id = generate_uuid_id()
                people_relationship_list = []
                for family_relationship in k12_student.family_relationship:
                    if family_relationship.parent_id and family_relationship.relationship_name:
                        people_relationship_list.append(
                            PeopleRelationshipViewModel(
                                subject_people_id=new_people_id,
                                object_people_id=context_people_parent_map.get(
                                    family_relationship.parent_id
                                ),
                                relationship=family_relationship.relationship_name,
                            )
                        )
                establishment_assign_list = []
                for dingtalk_k12_dept_id in k12_student.dingtalk_k12_dept_id_list:
                    establishment_assign_list.append(
                        EstablishmentAssignViewModel(
                            dimension_category=EnumDimensionCategory.EDU.name,
                            dimension_dept_tree_id=context_dept_map.get(dingtalk_k12_dept_id),
                            capacity_code=EnumCapacityCode.STUDENT.name,
                            capacity_name=EnumCapacityCode.STUDENT.value,
                            organization_id=organization_id,
                        )
                    )
                data = AddPeopleViewModel(
                    id=new_people_id,
                    name=k12_student.name,
                    remote_user_id=k12_student.remote_user_id,
                    people_relationship_list=people_relationship_list,
                    establishment_assign_list=establishment_assign_list,
                )
                need_add_people_dict[k12_student.id] = data

        context_people_map = {}
        for k12_student_id, people_em in need_add_people_dict.items():
            people_id = self.__people_service.add_people_info(
                people=people_em, transaction=transaction
            )
            self.add_student_avatar(people_id=people_id, transaction=transaction)
            self.__context_people_user_map_repository.insert_context_people_user_map(
                context_org_corp_map=ContextPeopleUserMapModel(
                    people_id=people_id,
                    res_category=EnumContextPeopleUserMapResCategory.DINGTALK_K12_STUDENT.name,
                    res_id=k12_student_id,
                ),
                transaction=transaction,
            )
            context_people_map[k12_student_id] = people_em.id

        return context_people_map

    def __update_k12_student(
        self,
        k12_student_list: List[DingtalkK12StudentInfoViewModel],
        organization_id: str,
        context_student_list: List[ContextPeopleStudentDetailViewModel],
        context_dept_map: Dict[str, str],
        context_people_parent_map: Dict[str, str],
        transaction: Transaction,
    ):
        """
        修改
        :param k12_student_list:
        :param organization_id:
        :param context_student_list:
        :param context_dept_map:
        :param context_people_parent_map:
        :param transaction:
        :return:
        """

        k12_student_dict = {x.id: x for x in k12_student_list}

        for context_student in context_student_list:
            k12_student = k12_student_dict.get(context_student.res_id)
            if k12_student:
                if k12_student.name != context_student.name:
                    self.__people_service.update_people(
                        people=PeopleModel(
                            id=context_student.people_id,
                            version=context_student.people_version,
                            name=k12_student.name,
                            is_available=True,
                        ),
                        transaction=transaction,
                    )
                establishment_assign_list = []
                for dingtalk_k12_dept_id in k12_student.dingtalk_k12_dept_id_list:
                    dimension_dept_tree_id = context_dept_map.get(dingtalk_k12_dept_id)
                    if not dimension_dept_tree_id:
                        # 说明这个班级已经被删除了，不需要继续
                        continue
                    establishment_assign_list.append(
                        EstablishmentAssignViewModel(
                            dimension_category=EnumDimensionCategory.EDU.name,
                            dimension_dept_tree_id=dimension_dept_tree_id,
                            capacity_code=EnumCapacityCode.STUDENT.name,
                            duty_name=EnumCapacityCode.STUDENT.value,
                            organization_id=organization_id,
                        )
                    )
                people_relationship_list = []
                for family_relationship in k12_student.family_relationship:
                    if family_relationship.parent_id and family_relationship.relationship_name:
                        people_relationship_list.append(
                            PeopleRelationshipViewModel(
                                subject_people_id=context_student.people_id,
                                object_people_id=context_people_parent_map.get(
                                    family_relationship.parent_id
                                ),
                                relationship=family_relationship.relationship_name,
                            )
                        )
                data = AddPeopleViewModel(
                    id=context_student.people_id,
                    name=k12_student.name,
                    remote_user_id=k12_student.remote_user_id,
                    people_relationship_list=people_relationship_list,
                    establishment_assign_list=establishment_assign_list,
                )
                self.__people_service.update_people_establishment_assign_and_relationship(
                    people=data, organization_id=organization_id, transaction=transaction
                )

    def __add_inner_people(
        self,
        dingtalk_user_list: List[DingtalkUserModel],
        organization_id: str,
        context_res_user_id_list: List[str],
        context_dept_map: Dict[str, str],
        context_k12_dept_map: Dict[str, str],
        transaction: Transaction,
    ) -> Dict[str, str]:
        """
        添加人员
        :param dingtalk_user_list:
        :param organization_id:
        :param context_res_user_id_list:
        :param transaction:
        :return:
        """

        need_add_people_dict = {}

        for dingtalk_user in dingtalk_user_list:
            if dingtalk_user.id not in context_res_user_id_list:
                establishment_assign_list = []
                for dingtalk_dept_user_duty in dingtalk_user.dingtalk_dept_user_duty_list:
                    establishment_assign_list.append(
                        EstablishmentAssignViewModel(
                            dimension_category=EnumDimensionCategory.ADMINISTRATION.name,
                            dimension_dept_tree_id=context_dept_map.get(
                                dingtalk_dept_user_duty.dingtalk_dept_id
                            ),
                            capacity_code=dingtalk_dept_user_duty.duty,
                            capacity_name=get_enum_value_by_name(
                                enum_class=EnumCapacityCode, enum_name=dingtalk_dept_user_duty.duty
                            ),
                            organization_id=organization_id,
                            seq=dingtalk_dept_user_duty.seq,
                        )
                    )
                for dingtalk_k12_dept_user_duty in dingtalk_user.dingtalk_k12_dept_user_duty_list:
                    establishment_assign_list.append(
                        EstablishmentAssignViewModel(
                            dimension_category=EnumDimensionCategory.EDU.name,
                            dimension_dept_tree_id=context_k12_dept_map.get(
                                dingtalk_k12_dept_user_duty.dingtalk_k12_dept_id
                            ),
                            capacity_code=dingtalk_k12_dept_user_duty.duty,
                            capacity_name=get_enum_value_by_name(
                                enum_class=EnumCapacityCode,
                                enum_name=dingtalk_k12_dept_user_duty.duty,
                            ),
                            organization_id=organization_id,
                        )
                    )
                data = AddPeopleViewModel(
                    id=generate_uuid_id(),
                    name=dingtalk_user.name,
                    mobile=dingtalk_user.mobile,
                    remote_user_id=dingtalk_user.remote_user_id,
                    establishment_assign_list=establishment_assign_list,
                )
                need_add_people_dict[dingtalk_user.id] = data

        context_people_map = {}
        for dingtalk_user_id, people_em in need_add_people_dict.items():
            self.__people_service.add_people_info(people=people_em, transaction=transaction)
            context_people_map[dingtalk_user_id] = people_em.id
            self.__context_people_user_map_repository.insert_context_people_user_map(
                context_org_corp_map=ContextPeopleUserMapModel(
                    people_id=people_em.id,
                    res_category=EnumContextPeopleUserMapResCategory.DINGTALK_USER.name,
                    res_id=dingtalk_user_id,
                ),
                transaction=transaction,
            )

        return context_people_map

    def __update_dingtalk_people(
        self,
        dingtalk_user_list: List[DingtalkUserModel],
        organization_id: str,
        context_people_list: List[ContextPeopleUserDetailViewModel],
        context_dept_map: Dict[str, str],
        context_k12_dept_map: Dict[str, str],
        dimension_category: str,
        transaction: Transaction,
    ):
        """
        修改 dingtalk people
        :param dingtalk_user_list:
        :param organization_id:
        :param context_people_list:
        :param context_dept_map:
        :param context_k12_dept_map:
        :param dimension_category:
        :param transaction:
        :return:
        """

        dingtalk_people_dict = {x.id: x for x in dingtalk_user_list}

        for people in context_people_list:
            dingtalk_people = dingtalk_people_dict.get(people.res_id)
            if dingtalk_people:
                if dingtalk_people.name != people.name:
                    self.__people_service.update_people(
                        people=PeopleModel(
                            id=people.people_id,
                            version=people.people_version,
                            name=dingtalk_people.name,
                            is_available=True,
                        ),
                        transaction=transaction,
                    )
                establishment_assign_list = []
                for dingtalk_dept_user_duty in dingtalk_people.dingtalk_dept_user_duty_list:
                    establishment_assign_list.append(
                        EstablishmentAssignViewModel(
                            dimension_category=dimension_category,
                            dimension_dept_tree_id=context_dept_map.get(
                                dingtalk_dept_user_duty.dingtalk_dept_id
                            ),
                            capacity_code=dingtalk_dept_user_duty.duty,
                            capacity_name=get_enum_value_by_name(
                                enum_class=EnumCapacityCode, enum_name=dingtalk_dept_user_duty.duty
                            ),
                            organization_id=organization_id,
                        )
                    )
                for dingtalk_k12_dept_user_duty in dingtalk_people.dingtalk_k12_dept_user_duty_list:
                    establishment_assign_list.append(
                        EstablishmentAssignViewModel(
                            dimension_category=EnumDimensionCategory.EDU.name,
                            dimension_dept_tree_id=context_k12_dept_map.get(
                                dingtalk_k12_dept_user_duty.dingtalk_k12_dept_id
                            ),
                            capacity_code=dingtalk_k12_dept_user_duty.duty,
                            capacity_name=get_enum_value_by_name(
                                enum_class=EnumCapacityCode,
                                enum_name=dingtalk_k12_dept_user_duty.duty,
                            ),
                            organization_id=organization_id,
                        )
                    )
                data = AddPeopleViewModel(
                    id=people.people_id,
                    name=dingtalk_people.name,
                    mobile=dingtalk_people.mobile,
                    remote_user_id=dingtalk_people.remote_user_id,
                    establishment_assign_list=establishment_assign_list,
                )
                self.__people_service.update_people_establishment_assign_and_relationship(
                    people=data, organization_id=organization_id, transaction=transaction
                )

    def add_student_avatar(self, people_id: str, transaction: Transaction):
        """
        添加学生头像
        :param people_id:
        :param transaction:
        :return:
        """
        file_path = build_abs_path_by_file(__file__, "../../context_sync/docs/avatar/")
        total_avatar_num = glob.glob(file_path + "*.png")
        relationship = EnumFileRelationship.AVATAR.name
        resource_category = EnumResource.PEOPLE.name
        avatar_seq = random.randint(1, len(total_avatar_num))
        file_name = str(avatar_seq) + ".png"
        with open(file_path + file_name, "rb") as f:
            self.__object_storage_service.upload_file_with_resource(
                file_name=file_name,
                file_blob=f.read(),
                resource=BasicResource(id=people_id, category=resource_category),
                relationship=relationship,
                transaction=transaction,
            )
