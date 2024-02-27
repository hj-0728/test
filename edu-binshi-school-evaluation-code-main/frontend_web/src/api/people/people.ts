import { defHttp } from '/@/utils/http/axios';

enum Api {
  GET_PEOPLE_BIND_USER_PAGE = '/people/bind-user-page',
}

export const apiGetPeopleBindUserPage = (params) => {
  return defHttp.post<any>({
    url: Api.GET_PEOPLE_BIND_USER_PAGE,
    params: params,
  });
};
