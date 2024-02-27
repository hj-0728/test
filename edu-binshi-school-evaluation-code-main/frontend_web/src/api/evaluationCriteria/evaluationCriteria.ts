import { defHttp } from '/@/utils/http/axios';
const PREFIX = '/evaluation-criteria';
const Api = {
  GET_EVALUATION_CRITERIA_PAGE: `${PREFIX}/get-page`,
  SAVE_EVALUATION_CRITERIA: `${PREFIX}/save`,
  GET_EVALUATION_CRITERIA_DETAIL: `${PREFIX}/detail`,
  UPDATE_EVALUATION_CRITERIA_STATUS: `${PREFIX}/update-status`,
  DELETE_EVALUATION_CRITERIA: `${PREFIX}/delete`,
  GET_ENUM_EVALUATION_OBJECT_CATEGORY: `${PREFIX}/get-enum-evaluation-object-category`,
  GET_ENUM_EVALUATION_CRITERIA_STATUS: `${PREFIX}/get-enum-evaluation-criteria-status`,
  GET_EVALUATION_CRITERIA_PLAN_BY_EVALUATION_CRITERIA_ID: `${PREFIX}/get-evaluation-criteria-plan-by-evaluation-criteria-id`,
  GET_EVALUATION_CRITERIA_LIST: `${PREFIX}/get-list`,
};

export const apiGetEvaluationCriteriaPage = (params) => {
  return defHttp.post<any>({
    url: Api.GET_EVALUATION_CRITERIA_PAGE,
    params: params,
  });
};

export const apiSaveEvaluationCriteria = (params) => {
  return defHttp.post<any>({
    url: Api.SAVE_EVALUATION_CRITERIA,
    params: params,
  });
};

export const apiGetEvaluationCriteriaDetail = (evaluationCriteriaId) => {
  return defHttp.get<any>({
    url: `${Api.GET_EVALUATION_CRITERIA_DETAIL}/${evaluationCriteriaId}`,
  });
};

export const apiUpdateEvaluationCriteriaStatus = (params) => {
  return defHttp.post<any>({
    url: `${Api.UPDATE_EVALUATION_CRITERIA_STATUS}`,
    params: params,
  });
};

export const apiDeleteEvaluationCriteria = (params) => {
  return defHttp.post<any>({
    url: `${Api.DELETE_EVALUATION_CRITERIA}`,
    params: params,
  });
};

export const apiGetEnumEvaluationObjectCategory = () => {
  return defHttp.get<any>({
    url: `${Api.GET_ENUM_EVALUATION_OBJECT_CATEGORY}`,
  });
};

export const apiGetEnumEvaluationCriteriaStatus = () => {
  return defHttp.get<any>({
    url: `${Api.GET_ENUM_EVALUATION_CRITERIA_STATUS}`,
  });
};

export const apiGetEvaluationCriteriaPlanByEvaluationCriteriaId = (param) => {
  return defHttp.get<any>({
    url: `${Api.GET_EVALUATION_CRITERIA_PLAN_BY_EVALUATION_CRITERIA_ID}`,
    params: {
      evaluation_criteria_id: param,
    },
  });
};

export const apiGetEvaluationCriteriaList = (params) => {
  return defHttp.post<any>({
    url: Api.GET_EVALUATION_CRITERIA_LIST,
    params: params,
  });
};
