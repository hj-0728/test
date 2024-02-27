import { defHttp } from '/@/utils/http/axios';

enum Api {
  GET_TAG_LIST = '/tag/resource-evaluation-criteria-tree/list',
}

export const apiGetTagList = () => {
  return defHttp.get<any>({
    url: Api.GET_TAG_LIST,
  });
};
