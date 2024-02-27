import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';
const PREFIX = '/evaluation-assignment';
const Api = {
  GET_EVALUATION_ASSIGNMENT_TODO_LIST: `${PREFIX}/todo-list`,
  GET_EVALUATION_ASSIGNMENT_ABOUT_ME_LIST: `${PREFIX}/about-me-list`,
};

export const apiGetEvaluationAssignmentTodoList = (params) => {
  return defHttp.post<BasicResponseModel>({
    url: Api.GET_EVALUATION_ASSIGNMENT_TODO_LIST,
    params: params,
  });
};

export const apiGetEvaluationAssignmentAboutMeList = (params) => {
  return defHttp.post<BasicResponseModel>({
    url: Api.GET_EVALUATION_ASSIGNMENT_ABOUT_ME_LIST,
    params: params,
  });
};
