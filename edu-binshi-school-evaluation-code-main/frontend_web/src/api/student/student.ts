import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';
const PREFIX = '/student';
const Api = {
  GET_STUDENT_PAGE: `${PREFIX}/get-page`,
  GET_STUDENT_USER_PAGE: `${PREFIX}/get-student-user-page`,
  GET_STUDENT_INFO_LIST_BY_ESTABLISHMENT_ASSIGN_ID_LIST: `${PREFIX}/get-student-info-list-by-establishment-assign-id-list`,
  CREATE_STUDENT_USER: `${PREFIX}/create-student-user`,
  EXPORT_STUDENT_USER: `${PREFIX}/export-student-user`,
  BATCH_CREATE_STUDENT_USER: `${PREFIX}/batch-create-student-user`,
};

export const apiStudentPage = (params) => {
  return defHttp.post<any>({
    url: Api.GET_STUDENT_PAGE,
    params: params,
  });
};

export const apiGetStudentInfoListByEstablishmentAssignIdList = (peopleIdList: Array<string>) =>
  defHttp.post<any>(
    {
      url: Api.GET_STUDENT_INFO_LIST_BY_ESTABLISHMENT_ASSIGN_ID_LIST,
      params: {
        people_id_list: peopleIdList,
      },
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );

export const apiStudentUserPage = (params) => {
  return defHttp.post<any>({
    url: Api.GET_STUDENT_USER_PAGE,
    params: params,
  });
};

/**
 * 创建学生用户
 */
export const apiCreateStudentUser = (params) =>
  defHttp.post<BasicResponseModel>({
    url: Api.CREATE_STUDENT_USER,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * 批量创建学生用户
 */
export const apiBatchCreateStudentUser = (params) =>
  defHttp.post<BasicResponseModel>({
    url: Api.BATCH_CREATE_STUDENT_USER,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * 导出学生用户
 */
export const apiExportStudentUser = (params) =>
  defHttp.post<any>({
    url: Api.EXPORT_STUDENT_USER,
    params: params,
    headers: {
      ignoreCancelToken: true,
    },
  });
