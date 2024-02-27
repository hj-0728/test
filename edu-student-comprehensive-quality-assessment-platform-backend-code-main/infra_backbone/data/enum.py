from enum import Enum


class EnumBackboneResource(str, Enum):
    DEPT = "部门"
    PEOPLE = "人员"
    ESTABLISHMENT_ASSIGN = "编制分配"
    DIMENSION_DEPT_TREE = "维度部门树"


class EnumFileRelationship(str, Enum):
    AVATAR = "头像"
    ICON = "图标"
    ANNEX = "附件"
