import { defHttp } from '/@/utils/http/axios';
import {
  LoginParams,
  UserInfoResponseModel,
  ChangePasswordParams,
  ImproveUserPasswordParams,
} from './model/userModel';

import { ErrorMessageMode } from '/#/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';

enum Api {
  LOGIN = '/user/login',
  LOGOUT = '/user/logout',
  GET_USER_INFO = '/user/get-user-info',
  GET_PERM_CODE = '/get-perm-code',
  GET_LOGIN_VALIDATE_IMAGE = '/user/get-login-validate-image',
  GET_ORGANIZATION_USER_OPTION = '/user/get-organization-user-option',
  CHANGE_PASSWORD = '/user/change-user-password',
  CHANGE_USER_ACTIVATED = '/user/chang-user-activated',
  IMPROVE_USER_PASSWORD = '/user/improve-user-password',
}

/**
 * @description: user login api
 */
export function apiLogin(params: LoginParams, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<any>(
    {
      url: Api.LOGIN,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
}

/**
 * @description: 获取用户信息
 */
export function apiGetUserInfo() {
  return defHttp.get<UserInfoResponseModel>(
    { url: Api.GET_USER_INFO },
    { errorMessageMode: 'none' },
  );
}

/**
 * @description: 退出登录
 */
export function doLogout() {
  return defHttp.post<any>({
    url: Api.LOGOUT,
    headers: {
      ignoreCancelToken: true,
    },
  });
}

export function getPermCode() {
  return defHttp.get<string[]>({ url: Api.GET_PERM_CODE });
}

export function apiGetLoginValidateImage() {
  return defHttp.get<any>({ url: Api.GET_LOGIN_VALIDATE_IMAGE });
}

/**
 * @description:获取组织用户选择框的选项
 */
export const apiGetOrganizationUserOption = (organizationId) => {
  return defHttp.get({
    url: Api.GET_ORGANIZATION_USER_OPTION + '/' + organizationId,
  });
};

/**
 * @description: changePassword
 */
export function aipChangePassword(params: ChangePasswordParams, mode: ErrorMessageMode = 'modal') {
  return defHttp.post<any>(
    {
      url: Api.CHANGE_PASSWORD,
      params,
    },
    {
      errorMessageMode: mode,
    },
  );
}

/**
 * 改变启用状态
 */
export function apiChangeActivated(params) {
  return defHttp.post<BasicResponseModel>({
    url: Api.CHANGE_USER_ACTIVATED,
    params: params,
  });
}
/**
 * @description: 完善密码
 */
export function aipImproveUserPassword(params: ImproveUserPasswordParams) {
  return defHttp.post<any>({
    url: Api.IMPROVE_USER_PASSWORD,
    params,
  });
}
