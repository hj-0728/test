from typing import List, Optional

from infra_basic.basic_repository import BasicRepository
from infra_basic.transaction import Transaction

from edu_binshi.entity.docx_table_style_config import DocxTableStyleConfigEntity
from edu_binshi.model.docx_table_style_config_model import DocxTableStyleConfigModel


class DocxTableStyleConfigRepository(BasicRepository):
    """
    word表格样式配置 repository
    """

    def insert_docx_table_style_config(
        self,
        docx_table_style_config: DocxTableStyleConfigModel,
        transaction: Transaction,
    ):
        """
        添加word表格样式配置
        """
        return self._insert_versioned_entity_by_model(
            entity_cls=DocxTableStyleConfigEntity,
            entity_model=docx_table_style_config,
            transaction=transaction
        )

    def update_docx_table_style_config(
        self,
        docx_table_style_config: DocxTableStyleConfigModel,
        transaction: Transaction,
        limited_col_list: Optional[List[str]] = None,
    ):
        """
        更新word表格样式配置
        """
        return self._update_versioned_entity_by_model(
            entity_cls=DocxTableStyleConfigEntity,
            update_model=docx_table_style_config,
            transaction=transaction,
            limited_col_list=limited_col_list
        )

    def delete_docx_table_style_config(
        self,
        docx_table_style_config_id: str,
        transaction: Transaction,
    ):
        """
        删除word表格样式配置
        """
        return self._delete_versioned_entity_by_id(
            entity_cls=DocxTableStyleConfigEntity,
            entity_id=docx_table_style_config_id,
            transaction=transaction,
        )

    def get_docx_table_style_config(
        self,
        name: str,
        code: str,
        belong_style_template_file_name: str,
        row: int,
        col: int,
    ) -> Optional[DocxTableStyleConfigModel]:
        """
        删除word表格样式配置
        """

        sql = """
        SELECT * FROM st_docx_table_style_config
        WHERE name = :name
        AND code = :code
        AND belong_style_template_file_name = :belong_style_template_file_name
        AND row = :row
        AND col = :col
        """

        return self._fetch_first_to_model(
            model_cls=DocxTableStyleConfigModel,
            sql=sql,
            params={
                "name": name,
                "code": code,
                "belong_style_template_file_name": belong_style_template_file_name,
                "row": row,
                "col": col,
            },
        )

    def get_docx_table_style_config_dict(
        self,
    ):
        """
        删除word表格样式配置
        """

        sql = """
        SELECT json_object_agg(
        sc.code, json_build_object('name', sc.name, 'templateFileName',
        sc.belong_style_template_file_name, 'belong_style_template_file_name',
        sc.belong_style_template_file_name, 'row', sc.row, 'col', sc.col)
        ) AS docx_table_style_config
        FROM st_docx_table_style_config sc
        """

        data = self._execute_sql(
            sql=sql,
            params={},
        )
        return data[0].get("docx_table_style_config")
