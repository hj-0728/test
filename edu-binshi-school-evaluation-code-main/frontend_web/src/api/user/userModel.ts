import { BasicResponseModel } from '/@/api/model/baseModel';

export interface UserEvaluationPermission {
  showDutyTeacher: boolean;
  isOnDutyTeacher: boolean;
  roleCode: string;
  canSwitch: boolean;
}

export interface ResponseUserEvaluationPermission extends BasicResponseModel {
  data: UserEvaluationPermission;
}
