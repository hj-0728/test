import os
from typing import List, Dict

from infra_utility.file_helper import build_abs_path_by_file

from biz_comprehensive.data.enum import EnumDictMetaCode
from infra_backbone.model.dict_data_model import EnumValueType
from infra_backbone.model.edit.dict_em import DictDataEm
from infra_backbone.service.dict_service import DictService
from infra_backbone.service.storage_service import StorageService


def test_init_img(prepare_app_container, prepare_robot):
    uow = prepare_app_container.uow()
    dict_service: DictService = prepare_app_container.backbone_container.dict_service()
    storage_service: StorageService = (
        prepare_app_container.backbone_container.storage_service()
    )
    need_upload_meta_list = [
        # EnumDictMetaCode.SYSTEM_COMMEND_OBSERVATION_POINT_ICON.name,
        # EnumDictMetaCode.SYSTEM_TO_BE_IMPROVED_OBSERVATION_POINT_ICON.name,
        EnumDictMetaCode.STUDENT_DEFAULT_AVATAR.name,
        EnumDictMetaCode.DEPT_DEFAULT_AVATAR.name,
    ]
    for meta in need_upload_meta_list:
        dict_meta = dict_service.get_dict_meta_by_meta_code(dict_meta_code=meta)
        file_list = _load_folder_files(dict_meta_code=meta)
        with uow:
            transaction = uow.log_transaction(
                handler=prepare_robot,
                action="test_init_img",
                action_params={"dict_meta_id": dict_meta.id}
            )
            dict_data_list = []
            for file in file_list:
                file_info = storage_service.upload_file_with_resource(
                    file_name=file["file_name"],
                    file_blob=file["file_blob"],
                    transaction=transaction,
                    is_public=True,
                )
                dict_data_list.append(
                    DictDataEm(
                        name=file["file_name"],
                        code=file["file_name"],
                        value_type=EnumValueType.STRING.name,
                        value=file_info.id,
                    )
                )

            dict_service.update_dict_data(
                dict_meta_id=dict_meta.id,
                is_tree=False,
                dict_data_list=dict_data_list,
                transaction=transaction,
            )


def _load_folder_files(dict_meta_code: str) -> List[Dict]:
    """
    加载文件夹下的所有文件
    """
    dict_meta_file_map = {
        EnumDictMetaCode.SYSTEM_COMMEND_OBSERVATION_POINT_ICON.name: "commend",
        EnumDictMetaCode.SYSTEM_TO_BE_IMPROVED_OBSERVATION_POINT_ICON.name: "to_be_improved",
        EnumDictMetaCode.STUDENT_DEFAULT_AVATAR.name: "student_avatar",
        EnumDictMetaCode.DEPT_DEFAULT_AVATAR.name: "dept_avatar",
    }
    folder_path = build_abs_path_by_file(__file__, f"init_img/{dict_meta_file_map[dict_meta_code]}")

    file_list = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # 打开图片并转换为字节数组
        with open(file_path, "rb") as img_file:
            img_bytes = img_file.read()
        file_list.append({"file_name": filename, "file_blob": img_bytes})
    return file_list
