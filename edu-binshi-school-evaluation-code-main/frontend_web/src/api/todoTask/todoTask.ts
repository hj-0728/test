import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';
const PREFIX = '/todo-task';
const Api = {
  PAGE: `${PREFIX}/page`,
  COMPLETE: `${PREFIX}/complete`,
};

/**
 * 获取待办事项列表
 */
export const apiGetTodoTaskPage = (params) => {
  return defHttp.post<BasicResponseModel>({
    url: `${Api.PAGE}`,
    params: params,
  });
};

/**
 * 完成待办事项
 */
export const apiCompleteTodoTask = (data) => {
  return defHttp.post<BasicResponseModel>({
    url: `${Api.COMPLETE}`,
    params: data,
  });
};
