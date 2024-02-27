import { defHttp } from '/@/utils/http/axios';
const PREFIX = '/input-score-log';
const Api = {
  UPDATE_INPUT_SCORE_LOG: `${PREFIX}/update`,
};

export const apiUpdateInputScoreLog = (params) => {
  return defHttp.post<any>({
    url: Api.UPDATE_INPUT_SCORE_LOG,
    params: params,
  });
};
