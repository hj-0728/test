import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';

enum Api {
  TEAM_LIST = '/team/list',
  DELETE_TEAM = '/team/delete/',
  GET_TEAM_DETAIL = '/team/detail/',
  GET_TEAM_GOAL = '/team-goal/get-team-goal-tree',
  SAVE_TEAM = '/team/save',
}
/**
 * 获取小组列表
 */

export const apiGetTeamList = (params) =>
  defHttp.post<BasicResponseModel>({
    url: Api.TEAM_LIST,
    params: params,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * 删除小组
 */
export const apiDeleteTeam = (teamId) =>
  defHttp.post<BasicResponseModel>({
    url: Api.DELETE_TEAM + teamId,
  });

/**
 * 保存小组信息
 */
export const apiSaveTeam = (params) => {
  return defHttp.post<any>({
    url: Api.SAVE_TEAM,
    params: params,
  });
};

/**
 * 获取小组目标树
 */
export const apiGetTeamGoalTree = (params) => {
  return defHttp.post<any>({
    url: Api.GET_TEAM_GOAL,
    params: params,
  });
};

/**
 * 获取小组信息详情
 */
export const apiGetTeamDetail = (teamId) => {
  return defHttp.get<any>({
    url: `${Api.GET_TEAM_DETAIL}/${teamId}`,
  });
};
