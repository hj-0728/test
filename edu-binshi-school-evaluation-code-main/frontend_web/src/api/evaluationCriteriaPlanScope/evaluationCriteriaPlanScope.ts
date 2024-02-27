import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';
const PREFIX = '/evaluation-criteria-plan-scope';
const Api = {
  SAVE_EVALUATION_CRITERIA_PLAN_SCOPE: `${PREFIX}/save`,
  GET_EVALUATION_CRITERIA_PLAN_SCOPE_BY_PLAN_ID: `${PREFIX}/get-plan-scope-by-plan-id`,
};

export const apiSaveEvaluationCriteriaPlanScope = (params) => {
  return defHttp.post<BasicResponseModel>({
    url: Api.SAVE_EVALUATION_CRITERIA_PLAN_SCOPE,
    params: params,
  });
};

export const apiGetPlanScopeByPlanId = (planId) => {
  return defHttp.get<BasicResponseModel>({
    url: `${Api.GET_EVALUATION_CRITERIA_PLAN_SCOPE_BY_PLAN_ID}/${planId}`,
  });
};
