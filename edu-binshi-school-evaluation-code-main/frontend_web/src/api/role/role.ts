import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';
import {
  changeIsActivatedResponseModel,
  RoleListResponseModel,
  SaveRoleResponseModel,
} from '../model/roleModel';
import { ErrorMessageMode } from '/#/axios';

const PREFIX = '/role';

enum Api {
  UPDATE_USER_CURRENT_ROLE = '/update-user-current-role',
  ROLE_LIST = '/list',
  ROLE_PAGE_LIST = '/page-list',
  SAVE_ROLE = '/role/save',
  CHANGE_IS_ACTIVATED = '/role/change-is-activated',
  ROLE_INFO = '/role/info/',
  GET_USER_ROLE_LIST = '/get-user-role-list',
  GET_ROLE_FILTER_LIST = '/role/get-role-filter-list',
  GET_TEACHER_ROLE_LIST = '/role/get-teacher-role-list',
}

/**
 * @description: update current role
 */
export function apiUpdateUserCurrentRole(data) {
  return defHttp.post<BasicResponseModel>({
    url: PREFIX + Api.UPDATE_USER_CURRENT_ROLE,
    params: data,
  });
}

/**
 * @description:获取角色列表信息
 */
export const apiGetRoleList = () => {
  return defHttp.get<any>({
    url: PREFIX + Api.ROLE_LIST,
  });
};

/**
 * @description:获取角色列表信息
 */
export const apiGetRolePageList = (params: RoleListResponseModel) => {
  return defHttp.post<any>({
    url: PREFIX + Api.ROLE_PAGE_LIST,
    params,
  });
};

/**
 * @description:获取角色列表信息
 */
export const roleListApi = (params, mode: ErrorMessageMode = 'modal') => {
  return defHttp.post<any>(
    {
      url: PREFIX + Api.ROLE_LIST,
      params,
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      errorMessageMode: mode,
      isTransformResponse: false,
    },
  );
};

/**
 * @description:改变激活状态
 */
export const changeIsActivatedApi = (params: changeIsActivatedResponseModel) => {
  return defHttp.post<any>({
    url: Api.CHANGE_IS_ACTIVATED,
    params,
  });
};

/**
 * @description:获取指定组织的所有角色列表信息saveRoleModel
 */
export const roleInfoApi = (roleId: string) => {
  return defHttp.get<any>(
    {
      url: Api.ROLE_INFO + roleId,
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
};

/**
 * @description:新增或保存角色
 */
export const SaveRoleApi = (params: SaveRoleResponseModel) => {
  return defHttp.post<any>(
    {
      url: Api.SAVE_ROLE,
      params,
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
};

/**
 * @description:获取用户的角色
 */
export const apiGetUserRoleList = (userId) => {
  return defHttp.get<any>(
    {
      url: PREFIX + Api.GET_USER_ROLE_LIST + '/' + userId,
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
};

export const apiGetRoleFilterList = () => {
  return defHttp.get<any>(
    {
      url: Api.GET_ROLE_FILTER_LIST,
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
};

export const apiGetTeacherRoleList = () => {
  return defHttp.get<any>(
    {
      url: Api.GET_TEACHER_ROLE_LIST,
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
};
