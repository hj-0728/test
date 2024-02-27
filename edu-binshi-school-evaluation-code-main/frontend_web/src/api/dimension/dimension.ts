import { defHttp } from '/@/utils/http/axios';

enum Api {
  GET_DIMENSION_LIST = '/dimension/get-list/',
}

export const apiGetDimensionList = () => {
  return defHttp.get<any>({
    url: Api.GET_DIMENSION_LIST,
  });
};
