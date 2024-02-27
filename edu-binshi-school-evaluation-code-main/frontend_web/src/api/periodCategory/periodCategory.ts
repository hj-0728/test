import { defHttp } from '/@/utils/http/axios';
const PREFIX = '/period-category';
const Api = {
  GET_PERIOD_CATEGORY_LIST: `${PREFIX}/get-list`,
};

export const apiGetPeriodCategoryList = () => {
  return defHttp.get<any>({
    url: Api.GET_PERIOD_CATEGORY_LIST,
  });
};
