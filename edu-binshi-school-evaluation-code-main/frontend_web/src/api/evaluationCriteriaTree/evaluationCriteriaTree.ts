import { defHttp } from '/@/utils/http/axios';
const PREFIX = '/evaluation-criteria-tree';
const Api = {
  GET_EVALUATION_CRITERIA_TREE: `${PREFIX}/get-tree`,
  GET_EVALUATION_CRITERIA_TREE_DETAIL: `${PREFIX}/detail`,
  SAVE_EVALUATION_CRITERIA_TREE: `${PREFIX}/save`,
  DELETE_EVALUATION_CRITERIA_TREE: `${PREFIX}/delete`,
  UPDATE_EVALUATION_CRITERIA_TREE_SEQ: `${PREFIX}/update-seq`,
  EVALUATION_CRITERIA_TREE_BOUND_TAG_ITEM_LIST: `${PREFIX}/bound-tag-item-list`,
  EVALUATION_CRITERIA_TREE_NOT_BOUND_TAG_ITEM_LIST: `${PREFIX}/not-bound-tag-item-list`,
  EVALUATION_CRITERIA_TREE_BOUND_TAG_DETAIL: `${PREFIX}/bound-tag-detail`,
  EVALUATION_CRITERIA_TREE_BIND_TAG: `${PREFIX}/bind-tag`,
  EVALUATION_CRITERIA_TREE_UNBOUND_TAG: `${PREFIX}/unbound-tag`,
};

export const apiGetEvaluationCriteriaTree = (evaluationCriteriaId) => {
  return defHttp.get<any>({
    url: `${Api.GET_EVALUATION_CRITERIA_TREE}/${evaluationCriteriaId}`,
  });
};

export const apiGetEvaluationCriteriaTreeDetail = (evaluationCriteriaTreeId) => {
  return defHttp.get<any>({
    url: `${Api.GET_EVALUATION_CRITERIA_TREE_DETAIL}/${evaluationCriteriaTreeId}`,
  });
};

export const apiSaveEvaluationCriteriaTree = (params) => {
  return defHttp.post<any>({
    url: `${Api.SAVE_EVALUATION_CRITERIA_TREE}`,
    params: params,
  });
};

export const apiDeleteEvaluationCriteriaTree = (params) => {
  return defHttp.post<any>({
    url: Api.DELETE_EVALUATION_CRITERIA_TREE,
    params: params,
  });
};

export const apiUpdateEvaluationCriteriaTreeSeq = (params) => {
  return defHttp.post<any>({
    url: Api.UPDATE_EVALUATION_CRITERIA_TREE_SEQ,
    params: params,
  });
};

export const apiGetEvaluationCriteriaBoundTagItemList = (params) => {
  return defHttp.post<any>({
    url: Api.EVALUATION_CRITERIA_TREE_BOUND_TAG_ITEM_LIST,
    params: params,
  });
};

export const apiGetEvaluationCriteriaTreeBoundTagDetail = (evaluationCriteriaId) => {
  return defHttp.get<any>({
    url: `${Api.EVALUATION_CRITERIA_TREE_BOUND_TAG_DETAIL}/${evaluationCriteriaId}`,
  });
};

export const apiGetEvaluationCriteriaNotBoundTagItemList = (params) => {
  return defHttp.post<any>({
    url: Api.EVALUATION_CRITERIA_TREE_NOT_BOUND_TAG_ITEM_LIST,
    params: params,
  });
};

export const apiEvaluationCriteriaTreeBindTag = (params) => {
  return defHttp.post<any>({
    url: Api.EVALUATION_CRITERIA_TREE_BIND_TAG,
    params: params,
  });
};

export const apiEvaluationCriteriaTreeUnboundTag = (params) => {
  return defHttp.post<any>({
    url: Api.EVALUATION_CRITERIA_TREE_UNBOUND_TAG,
    params: params,
  });
};
