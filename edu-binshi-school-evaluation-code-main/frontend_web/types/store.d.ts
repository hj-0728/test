import { ErrorTypeEnum } from '/@/enums/exceptionEnum';
import { MenuModeEnum, MenuTypeEnum } from '/@/enums/menuEnum';
import { RoleInfo } from '/@/api/sys/model/userModel';
import { RoleEnum } from '/@/enums/roleEnum';

// Lock screen information
export interface LockInfo {
  // Password required
  pwd?: string | undefined;
  // Is it locked?
  isLock?: boolean;
}

// Error-log information
export interface ErrorLogInfo {
  // Type of error
  type: ErrorTypeEnum;
  // Error file
  file: string;
  // Error name
  name?: string;
  // Error message
  message: string;
  // Error stack
  stack?: string;
  // Error detail
  detail: string;
  // Error url
  url: string;
  // Error time
  time?: string;
}

export interface CurrentRoleInfo {
  id: string;
  name: string;
  code: RoleEnum;
  userRoleId: string;
}

export interface UserInfo {
  id: string;
  name: string;
  userId: string;
  username: string;
  realName: string;
  avatar?: string;
  desc?: string;
  homePath?: string;
  roleList: RoleInfo[];
  currentRole: CurrentRoleInfo;
  currentOrganization?: CurrentOrganization;
  passwordReset?: string;
}

export interface BeforeMiniState {
  menuCollapsed?: boolean;
  menuSplit?: boolean;
  menuMode?: MenuModeEnum;
  menuType?: MenuTypeEnum;
}

export interface CurrentPeriodInfo {
  id: string;
  name: string;
  categoryCode: string;
}
