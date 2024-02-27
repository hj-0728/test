from typing import List, Optional

from infra_basic.errors import BusinessError
from infra_basic.pagination_carrier import PaginationCarrier
from infra_basic.transaction import Transaction
from infra_utility.datetime_helper import local_now
from infra_utility.enum_helper import get_enum_value_by_name

from infra_backbone.model.contact_info_model import ContactInfoModel, EnumContactInfoCategory
from infra_backbone.model.edit.add_people_em import AddPeopleViewModel
from infra_backbone.model.edit.people_em import PeopleEm
from infra_backbone.model.identity_number_model import (
    EnumIdentityNumberCategory,
    EnumIdentityNumberOwnerCategory,
    IdentityNumberModel,
)
from infra_backbone.model.params.people_params import PeoplePageQueryParams, PeopleQueryParams
from infra_backbone.model.people_model import EnumPeopleGender, PeopleModel
from infra_backbone.model.people_relationship_model import PeopleRelationshipModel
from infra_backbone.model.resource_contact_info_model import (
    EnumContactInfoResourceCategory,
    ResourceContactInfoModel,
)
from infra_backbone.model.view.people_page_vm import PeoplePageVm
from infra_backbone.repository.identity_number_repository import IdentityNumberRepository
from infra_backbone.repository.people_relationship_repository import PeopleRelationshipRepository
from infra_backbone.repository.people_repository import PeopleRepository
from infra_backbone.repository.resource_contact_info_repository import ResourceContactInfoRepository
from infra_backbone.service.contact_info_service import ContactInfoService
from infra_backbone.service.establishment_assign_service import EstablishmentAssignService


class PeopleService:
    def __init__(
        self,
        people_repository: PeopleRepository,
        identity_number_repository: IdentityNumberRepository,
        resource_contact_info_repository: ResourceContactInfoRepository,
        people_relationship_repository: PeopleRelationshipRepository,
        establishment_assign_service: EstablishmentAssignService,
        contact_info_service: ContactInfoService,
    ):
        self.__people_repository = people_repository
        self.__identity_number_repository = identity_number_repository
        self.__resource_contact_info_repository = resource_contact_info_repository
        self.__people_relationship_repository = people_relationship_repository
        self.__establishment_assign_service = establishment_assign_service
        self.__contact_info_service = contact_info_service

    def insert_people(
        self,
        people: PeopleModel,
        transaction: Transaction,
    ):
        """
        插入人员
        :param people:
        :param transaction:
        :return:
        """
        return self.__people_repository.insert_people(
            data=people,
            transaction=transaction,
        )

    def delete_people_by_id(
        self,
        people_id: str,
        transaction: Transaction,
    ):
        """
        删除人员
        :param people_id:
        :param transaction:
        :return:
        """
        return self.__people_repository.delete_people_by_id(
            people_id=people_id,
            transaction=transaction,
        )

    def update_people(
        self,
        people: PeopleModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新人员
        :param people:
        :param transaction:
        :param limited_col_list:
        :return:
        """
        return self.__people_repository.update_people(
            people_id=people.id,
            version=people.version,
            people=people,
            transaction=transaction,
            limited_col_list=limited_col_list,
        )

    def get_people_page(
        self,
        params: PeoplePageQueryParams,
    ) -> PaginationCarrier[PeoplePageVm]:
        """
        获取人员列表 分页
        :param params:
        :return:
        """
        people_list_page = self.__people_repository.get_people_page(
            params=params,
        )
        for people in people_list_page.data:
            if people.gender:
                people.gender_display = get_enum_value_by_name(
                    enum_class=EnumPeopleGender, enum_name=people.gender
                )
        return people_list_page

    def get_people_info_by_id(
        self,
        people_id: str,
    ):
        """
        根据id获取人员信息
        :param people_id:
        :return:
        """
        data = self.__people_repository.get_people_info_by_id(
            people_id=people_id,
        )
        if data:
            data.gender_display = get_enum_value_by_name(
                enum_class=EnumPeopleGender, enum_name=data.gender
            )
            for number in data.number_info:
                number.category_display = get_enum_value_by_name(
                    enum_class=EnumIdentityNumberCategory, enum_name=number.category
                )
        return data

    def add_people_and_identity_number(self, people_info: PeopleEm, transaction: Transaction):
        """
        添加人员及证件号码
        """
        people_id = self.__people_repository.insert_people(
            data=PeopleModel(name=people_info.name, gender=people_info.gender),
            transaction=transaction,
        )
        if people_info.identity_number:
            self.__identity_number_repository.insert_identity_number(
                data=IdentityNumberModel(
                    owner_id=people_id,
                    owner_category=EnumIdentityNumberOwnerCategory.PEOPLE.name,
                    category=people_info.identity_category,
                    number=people_info.identity_number,
                ),
                transaction=transaction,
            )
        return people_id

    def get_people_info_by_identity_number(self, identity_category: str, identity_number: str):
        """
        根据证件照获取人员信息
        """
        people_info = self.__people_repository.get_people_info_by_identity_number(
            identity_category=identity_category, identity_number=identity_number
        )
        if people_info:
            resource_contact_info = (
                self.__resource_contact_info_repository.fetch_resource_contact_info(
                    resource_id=people_info.id,
                    resource_category=EnumContactInfoResourceCategory.PEOPLE.name,
                )
            )
            if resource_contact_info:
                people_info.phone_list = [
                    contact_info.detail
                    for contact_info in resource_contact_info.contact_info_list
                    if contact_info.category == EnumContactInfoCategory.PHONE.name
                ]
        return people_info

    def get_people_list(self, query_params: PeopleQueryParams) -> PaginationCarrier[PeopleModel]:
        """
        获取用户列表
        """
        people_list = self.__people_repository.get_people_list(query_params=query_params)
        for people in people_list.data:
            if people.gender:
                people.gender_display = get_enum_value_by_name(
                    enum_class=EnumPeopleGender, enum_name=people.gender
                )
        return people_list

    def add_people(self, people: PeopleModel, transaction: Transaction):
        """
        添加人员
        """
        exist_people = self.__people_repository.get_people_by_name(
            name=people.name,
        )
        if exist_people:
            raise BusinessError(f"人员【{people.name}】已存在，请勿重复添加")
        people_id = self.__people_repository.insert_people(
            data=people,
            transaction=transaction,
        )
        return people_id

    def get_exist_people_by_remote_user_id(self, remote_user_id: str):
        """
        根据远程用户id获取已存在的人员信息
        """
        return self.__people_repository.get_people_by_remote_user_id(remote_user_id=remote_user_id)

    def add_people_info(self, people: AddPeopleViewModel, transaction: Transaction) -> str:
        """
        添加 people 信息
        :param people:
        :param transaction:
        :return:
        """
        if people.remote_user_id:
            exist_people_list = self.get_exist_people_by_remote_user_id(
                remote_user_id=people.remote_user_id,
            )
            if exist_people_list:
                people.id = exist_people_list[0].id
            else:
                people.id = self.__people_repository.insert_people(
                    data=people.cast_to(PeopleModel),
                    transaction=transaction,
                )
        if people.mobile:
            self.__contact_info_service.save_resource_contact_info(
                data=ResourceContactInfoModel(
                    resource_id=people.id,
                    resource_category=EnumContactInfoResourceCategory.PEOPLE.name,
                    contact_info_list=[
                        ContactInfoModel(
                            category=EnumContactInfoCategory.PHONE.name,
                            detail=people.mobile,
                        ),
                    ],
                ),
                transaction=transaction,
            )
        if people.people_relationship_list:
            for people_relationship in people.people_relationship_list:
                self.__people_relationship_repository.insert_people_relationship(
                    data=people_relationship.cast_to(
                        PeopleRelationshipModel, subject_people_id=people.id
                    ),
                    transaction=transaction,
                )

        if people.establishment_assign_list:
            self.__establishment_assign_service.add_establishment_assign(
                establishment_assign_list=people.establishment_assign_list,
                people_id=people.id,
                transaction=transaction,
            )
        return people.id

    def update_people_establishment_assign_and_relationship(
        self, people: AddPeopleViewModel, organization_id: str, transaction: Transaction
    ):
        """
        更新人员信息
        """
        if people.mobile:
            self.__contact_info_service.save_resource_contact_info(
                data=ResourceContactInfoModel(
                    resource_id=people.id,
                    resource_category=EnumContactInfoResourceCategory.PEOPLE.name,
                    contact_info_list=[
                        ContactInfoModel(
                            category=EnumContactInfoCategory.PHONE.name,
                            detail=people.mobile,
                        ),
                    ],
                ),
                transaction=transaction,
            )
        if people.people_relationship_list:
            self.handle_people_relationship(people=people, transaction=transaction)

        if people.establishment_assign_list:
            self.__establishment_assign_service.update_people_establishment_assign(
                establishment_assign_list=people.establishment_assign_list,
                organization_id=organization_id,
                people_id=people.id,
                transaction=transaction,
            )

    def handle_people_relationship(self, people: AddPeopleViewModel, transaction: Transaction):
        handle_time = local_now()
        exist_relationship_list = (
            self.__people_relationship_repository.get_people_relationship_list(people_id=people.id)
        )
        people_relationship_dict = {
            f"{relationship.subject_people_id}&&{relationship.object_people_id}": relationship
            for relationship in people.people_relationship_list
        }
        exist_relationship_dict = {
            f"{relationship.subject_people_id}&&{relationship.object_people_id}": relationship
            for relationship in exist_relationship_list
        }
        for k, v in people_relationship_dict.items():
            existed_rel = exist_relationship_dict.get(k)
            if existed_rel and existed_rel.relationship != v.relationship:
                new_relationship = PeopleRelationshipModel(
                    subject_people_id=existed_rel.subject_people_id,
                    object_people_id=existed_rel.object_people_id,
                    relationship=v.relationship,
                    started_on=handle_time,
                )
                self.__people_relationship_repository.insert_people_relationship(
                    data=new_relationship, transaction=transaction
                )
                existed_rel.ended_on = handle_time
                self.__people_relationship_repository.update_people_relationship(
                    data=existed_rel,
                    transaction=transaction,
                    limited_col_list=["ended_on"],
                )
            if not existed_rel:
                # 如果不在数据库中，应该新增
                new_relationship = PeopleRelationshipModel(
                    subject_people_id=v.subject_people_id,
                    object_people_id=v.object_people_id,
                    relationship=v.relationship,
                    started_on=handle_time,
                )
                self.__people_relationship_repository.insert_people_relationship(
                    data=new_relationship, transaction=transaction
                )
        for k, v in exist_relationship_dict.items():
            # 如果在数据库，不在当前人员的关系中，应该删除
            if not people_relationship_dict.get(k):
                v.ended_on = handle_time
                self.__people_relationship_repository.update_people_relationship(
                    data=v,
                    transaction=transaction,
                    limited_col_list=["ended_on"],
                )

    def get_people_by_user_id_and_role_code(self, user_id: str, role_code: str) -> PeopleModel:
        """
        根据用户id跟当前role_code获取people信息
        :param user_id:
        :param role_code:
        :return:
        """
        people_info = self.__people_repository.get_people_by_user_id_and_role_code(
            user_id=user_id, role_code=role_code
        )
        if not people_info:
            raise BusinessError("未找到人员信息")
        return people_info
