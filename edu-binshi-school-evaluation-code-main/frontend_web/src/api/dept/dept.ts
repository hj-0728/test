import { defHttp } from '/@/utils/http/axios';

enum Api {
  GET_DIMENSION_DEPT_TREE = '/dept/dimension-dept-tree/',
  GET_DIMENSION_DEPT_TREE_BY_CODE = '/dept/dimension-dept-tree-by-code',
  ADD_DEPT = '/dept/add',
  ADD_DEPT_PEOPLE = '/dept/add-dept-people',
  EDIT_DEPT = '/dept/edit',
  GET_DEPT_INFO = '/dept/get-info/',
  GET_DEPT_TREE = '/dept/get-tree',
}

export const apiGetDimensionDeptTree = (dimensionId) => {
  return defHttp.get<any>({
    url: Api.GET_DIMENSION_DEPT_TREE + dimensionId,
  });
};

export const apiGetDimensionDeptTreeByDimensionCode = (params) => {
  return defHttp.post<any>({
    url: Api.GET_DIMENSION_DEPT_TREE_BY_CODE,
    params: params,
  });
};

export const apiAddDept = (params) => {
  return defHttp.post<any>({
    url: Api.ADD_DEPT,
    params: params,
  });
};

export const apiAddDeptPeople = (params) => {
  return defHttp.post<any>({
    url: Api.ADD_DEPT_PEOPLE,
    params: params,
  });
};

export const apiEditDept = (params) => {
  return defHttp.post<any>({
    url: Api.EDIT_DEPT,
    params: params,
  });
};

export const apiGetDeptInfo = (dimensionDeptTreeId) => {
  return defHttp.get<any>({
    url: Api.GET_DEPT_INFO + dimensionDeptTreeId,
  });
};

export const apiGetDeptTree = (params) => {
  return defHttp.post<any>({
    url: Api.GET_DEPT_TREE,
    params: params,
  });
};
