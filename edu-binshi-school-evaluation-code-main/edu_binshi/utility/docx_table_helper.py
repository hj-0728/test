from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.table import Table


class CachedTable(Table):
    """
    用于加速python-docx写入数据到表格的速度
    https://github.com/python-openxml/python-docx/issues/174#issuecomment-667784193
    """

    def __init__(self, tbl, parent):
        super(Table, self).__init__(parent)
        self._element = self._tbl = tbl
        self._cached_cells = None

    @property
    def _cells(self):
        if self._cached_cells is None:
            self._cached_cells = super(CachedTable, self)._cells
        return self._cached_cells

    @staticmethod
    def transform(table):
        cached_table = CachedTable(table._tbl, table._parent)
        return cached_table


def set_table_border(table: Table, **kwargs):
    """
    设置表格边框
    用法:
    set_table_border(
        table,
        top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},
        bottom={"sz": 12, "color": "#00FF00", "val": "single"},
        start={"sz": 24, "val": "dashed", "shadow": "true"},
        end={"sz": 12, "val": "dashed"},
        insideH={"sz": 12, "val": "dashed"},
        insideV={"sz": 12, "val": "dashed"}
    )
    """
    tbl_pr = table._tbl.tblPr
    tblBorders = tbl_pr.first_child_found_in("w:tblBorders")
    if tblBorders is None:
        tblBorders = OxmlElement("w:tblBorders")
        tbl_pr.append(tblBorders)
    for edge in ("start", "top", "end", "bottom", "insideH", "insideV"):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = "w:{}".format(edge)
            element = tblBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tblBorders.append(element)
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn("w:{}".format(key)), str(edge_data[key]))
