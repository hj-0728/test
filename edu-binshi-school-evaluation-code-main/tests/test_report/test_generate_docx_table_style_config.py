from docx import Document
from infra_utility.file_helper import build_abs_path_by_file

from edu_binshi.model.docx_table_style_config_model import DocxTableStyleConfigModel

FILE_NAME = build_abs_path_by_file(__file__, "../../edu_binshi/docs/report/template/common_style_template.docx")


def test_generate_docx_table_style_config(prepare_edu_evaluation_container, prepare_robot):
    uow = prepare_edu_evaluation_container.uow()
    docx_table_style_config_repository = prepare_edu_evaluation_container.docx_table_style_config_repository()
    with uow:
        transaction = uow.log_transaction(handler=prepare_robot, action='test_generate_docx_table_style_config')
        style_template_path = build_abs_path_by_file(__file__, FILE_NAME)
        doc = Document(style_template_path)
        table = doc.tables[0]
        for row_idx, row in enumerate(table.rows):
            if row_idx == 0:
                continue
            if not row.cells[2].text:
                continue
            print(f"{row_idx}: {row.cells[3].text}")
            exist = docx_table_style_config_repository.get_docx_table_style_config(
                name=row.cells[3].text,
                code=row.cells[2].text,
                belong_style_template_file_name='common_style_template.docx',
                row=row_idx,
                col=1,
            )
            if not exist:
                docx_table_style_config_repository.insert_docx_table_style_config(
                    docx_table_style_config=DocxTableStyleConfigModel(
                        name=row.cells[3].text,
                        code=row.cells[2].text,
                        belong_style_template_file_name='common_style_template.docx',
                        row=row_idx,
                        col=1,
                    ),
                    transaction=transaction,
                )
