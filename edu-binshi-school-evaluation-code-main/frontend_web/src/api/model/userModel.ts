/**
 * @description: 添加用户
 */
import { BasicPageQueryParamsModel } from '/@/api/model/baseModel';

export interface UserEditModel {
  id: string;
  name: string;
  password: string;
  isActivated: boolean;
}

/**
 * 获取用户列表
 */
export interface UserListModel extends BasicPageQueryParamsModel {
  currentUserRoleCode: string;
}
