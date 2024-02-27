import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';

const PREFIX = '/team-member';

const Api = {
  TEAM_MEMBER_LIST: `${PREFIX}/list`,
  TEAM_CAN_SELECT_PEOPLE_LIST: `${PREFIX}/can-select-people-list`,
  SAVE_TEAM_MEMBER: `${PREFIX}/save`,
  DELETE_TEAM_MEMBER: `${PREFIX}/delete`,
};

/**
 * 获取小组成员列表
 */

export const apiGetTeamMemberList = (params) =>
  defHttp.post<BasicResponseModel>({
    url: Api.TEAM_MEMBER_LIST,
    params: params,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * 获取小组可选人员列表
 */
export const apiGetTeamCanSelectPeopleList = (params) =>
  defHttp.post<BasicResponseModel>({
    url: Api.TEAM_CAN_SELECT_PEOPLE_LIST,
    params: params,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * 获取保存小组人员
 */
export const apiSaveTeamMember = (data) =>
  defHttp.post<any>(
    {
      url: Api.SAVE_TEAM_MEMBER,
      data,
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );

export const apiDeleteTeamMember = (teamMemberId) =>
  defHttp.post<any>(
    {
      url: Api.DELETE_TEAM_MEMBER + `/${teamMemberId}`,
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
