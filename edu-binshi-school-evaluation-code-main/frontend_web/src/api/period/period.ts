import { defHttp } from '/@/utils/http/axios';
const PREFIX = '/period';
const Api = {
  GET_PERIOD_TREE: `${PREFIX}/get-tree`,
  CURRENT_PERIOD: `${PREFIX}/current-period`,
  PERIOD_LIST: `${PREFIX}/get-list`,
  CHANGE_CURRENT_PERIOD: `${PREFIX}/change-current-period`,
};

export const apiGetPeriodTree = (params) => {
  return defHttp.post<any>({
    url: Api.GET_PERIOD_TREE,
    params: params,
  });
};

export const apiGetCurrentPeriod = () => {
  return defHttp.get<any>({
    url: Api.CURRENT_PERIOD,
  });
};

export const apiGetPeriodListByCategory = (period_category) => {
  return defHttp.get<any>({
    url: Api.PERIOD_LIST + '/' + period_category,
  });
};

export const apiChangeCurrentPeriod = (params) => {
  return defHttp.post<any>({
    url: Api.CHANGE_CURRENT_PERIOD,
    params: params,
  });
};
