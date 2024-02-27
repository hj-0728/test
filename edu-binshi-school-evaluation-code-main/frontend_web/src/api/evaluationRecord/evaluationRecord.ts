import { defHttp } from '/@/utils/http/axios';
const PREFIX = '/evaluation-record';
const Api = {
  GET_EVALUATION_RECORD_TREE: `${PREFIX}/tree`,
};

export const apiGetEvaluationRecordTree = (params) => {
  return defHttp.post<any>({
    url: Api.GET_EVALUATION_RECORD_TREE,
    params: params,
  });
};
