import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';
import { UserEditModel, UserListModel } from '/@/api/model/userModel';
import { ResponseUserEvaluationPermission } from '/@/api/user/userModel';

enum Api {
  TEACHER_LIST = '/user/teacher-list',
  ADD_USER = '/user/add',
  EDIT_USER = '/user/edit',
  RESET_PASSWORD = '/user/reset-password',
  GET_USER_PERMISSION_DETAIL = '/user-permission/detail',
  USER_INFO = '/user/info/',
  USER_EVALUATION_PERMISSION = '/user-permission/evaluation/',
}

/**
 * 获取用户列表
 */

export const apiGetUserTeacherList = (params: UserListModel) =>
  defHttp.post<BasicResponseModel>({
    url: Api.TEACHER_LIST,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * 添加用户
 */
export const apiAddUser = (params: UserEditModel) =>
  defHttp.post<any>({
    url: Api.ADD_USER,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * 编辑用户
 */
export const apiEditUser = (params: UserEditModel) =>
  defHttp.post<any>({
    url: Api.EDIT_USER,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * 重置用户密码
 */
export const apiResetUserPassword = (params) =>
  defHttp.post<BasicResponseModel>({
    url: Api.RESET_PASSWORD,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * 获取当前用户详细信息
 */
export const apiGetUserPermissionDetail = () =>
  defHttp.get<any>({
    url: Api.GET_USER_PERMISSION_DETAIL,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * 获取当前用户详细信息
 */
export const apiGetUserInfo = (userId) =>
  defHttp.get<any>({
    url: Api.USER_INFO + userId,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * 获取当前用户点评的数据权限
 */
export const apiGetUserEvaluationPermission = (studentId) =>
  defHttp.get<ResponseUserEvaluationPermission>({
    url: Api.USER_EVALUATION_PERMISSION + studentId,
    headers: {
      ignoreCancelToken: true,
    },
  });
