import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';

enum Api {
  TEAM_CATEGORY_LIST = '/team-category/list',
  CHANGE_TEAM_CATEGORY_ACTIVATED = '/team-category/change-team-category-activated',
  GET_TEAM_CATEGORY_DETAIL = '/team-category/get-team-category-detail',
  SAVE_TEAM_CATEGORY = '/team-category/save-team-category',
}

/**
 * 获取小组类型列表
 */

export const apiGetTeamCategoryList = (params) =>
  defHttp.post<BasicResponseModel>({
    url: Api.TEAM_CATEGORY_LIST,
    params: params,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * 改变启用状态
 */
export function apiChangeActivated(params) {
  return defHttp.post<BasicResponseModel>({
    url: Api.CHANGE_TEAM_CATEGORY_ACTIVATED,
    params: params,
  });
}

/**
 * 获取小组类型细节
 */
export const apiGetTeamCategoryDetail = (teamCategoryId) => {
  return defHttp.get<any>({
    url: `${Api.GET_TEAM_CATEGORY_DETAIL}/${teamCategoryId}`,
  });
};

/**
 * 保存小组类型
 */
export const apiSaveTeamCategory = (params) => {
  return defHttp.post<any>({
    url: Api.SAVE_TEAM_CATEGORY,
    params: params,
  });
};
