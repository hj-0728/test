import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';
const PREFIX = '/evaluation-criteria-plan';
const Api = {
  SAVE_EVALUATION_CRITERIA_PLAN: `${PREFIX}/save`,
  GET_EVALUATION_CRITERIA_PLAN_DETAIL: `${PREFIX}/get-detail`,
  GET_EVALUATION_CRITERIA_PLAN_LIST: `${PREFIX}/list`,
  ABOLISH: `${PREFIX}/abolish`,
  DELETE_EVALUATION_CRITERIA_PLAN: `${PREFIX}/delete`,
  GET_EVALUATION_CRITERIA_PLAN_TODO_LIST: `${PREFIX}/todo-list`,
  SAVE_EVALUATION_CRITERIA_PLAN_AND_SCOPE: `${PREFIX}/save-plan-and-scope`,
  GET_EVALUATION_CRITERIA_PLAN_INFO: `${PREFIX}/get-info-by-id`,
};

export const apiSaveEvaluationCriteriaPlan = (params) => {
  return defHttp.post<any>({
    url: Api.SAVE_EVALUATION_CRITERIA_PLAN,
    params: params,
  });
};

export const apiGetEvaluationCriteriaPlanDetail = (evaluationCriteriaPlanId) => {
  return defHttp.get<any>({
    url: `${Api.GET_EVALUATION_CRITERIA_PLAN_DETAIL}/${evaluationCriteriaPlanId}`,
  });
};

/**
 * 获取评价计划列表
 */
export const apiGetEvaluationPlanList = (params) =>
  defHttp.post<BasicResponseModel>({
    url: `${Api.GET_EVALUATION_CRITERIA_PLAN_LIST}`,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });

export const apiAbolishStatus = (params) =>
  defHttp.post<BasicResponseModel>({
    url: `${Api.ABOLISH}`,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });

export const apiDeleteEvaluationCriteriaPlan = (params) => {
  return defHttp.post<any>({
    url: `${Api.DELETE_EVALUATION_CRITERIA_PLAN}`,
    params: params,
  });
};

export const apiGetEvaluationCriteriaPlanPageTodoList = (params) => {
  return defHttp.post<BasicResponseModel>({
    url: `${Api.GET_EVALUATION_CRITERIA_PLAN_TODO_LIST}`,
    params: params,
  });
};

export const apiSaveEvaluationCriteriaPlanAndScope = (params) => {
  return defHttp.post<BasicResponseModel>({
    url: `${Api.SAVE_EVALUATION_CRITERIA_PLAN_AND_SCOPE}`,
    params: params,
  });
};

/**
 * 获取评价计划本身信息
 */
export const apiGetEvaluationCriteriaPlanInfo = (evaluationCriteriaPlanId) => {
  return defHttp.get<any>({
    url: `${Api.GET_EVALUATION_CRITERIA_PLAN_INFO}/${evaluationCriteriaPlanId}`,
  });
};
