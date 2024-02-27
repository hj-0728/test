import { defHttp } from '/@/utils/http/axios';
const PREFIX = '/user-role';

enum Api {
  SAVE_USER_ROLE = '/save',
}

/**
 * @description:保存用户角色
 */
export const apiSaveUserRole = (params: any) => {
  return defHttp.post<any>(
    {
      url: PREFIX + Api.SAVE_USER_ROLE,
      params,
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
};
