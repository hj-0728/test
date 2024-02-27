import { defHttp } from '/@/utils/http/axios';

enum Api {
  GET_SCORE_SYMBOL_LIST = '/score-symbol/list',
}

export const apiGetScoreSymbolList = (params) => {
  return defHttp.post<any>({
    url: Api.GET_SCORE_SYMBOL_LIST ,
    params: params
  });
};
