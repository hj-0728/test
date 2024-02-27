/**
 * @description: Login interface parameters
 */
import { BasicResponseModel } from '/@/api/model/baseModel';
import { UserInfo } from '/#/store';

export interface LoginParams {
  name: string;
  password: string;
  validateCode?: string;
  validateImageSrc?: string;
}

export interface RoleInfo {
  id: string;
  name: string;
  code: string;
}

/**
 * @description: Login interface return value
 */
export interface LoginResultModel {
  userId: string | number;
  token: string;
  role: RoleInfo;
}

export interface UserInfoResponseModel extends BasicResponseModel {
  data: UserInfo;
}

/**
 * @description: change password parameters
 */
export interface ChangePasswordParams {
  password: string;
  newPassword: string;
  verifyNewPassword: string;
}

/**
 * @description: 完善密码
 */
export interface ImproveUserPasswordParams {
  newPassword: string;
  verifyNewPassword: string;
}
