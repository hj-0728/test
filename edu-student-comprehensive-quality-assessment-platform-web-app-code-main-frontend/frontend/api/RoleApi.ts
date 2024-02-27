import { PageFilterParams, PageFilterResult } from '@/model/Basic.model';
import { ChangeIsActivated, Role } from '@/model/Role.model';
import defHttp from './BasicApi';

enum Api {
    GET_ROLE_PAGE_LIST = 'role/page-list',
    SAVE_ROLE = 'role/save',
    CHANGE_IS_ACTIVATED = 'role/change-is-activated',
    GET_ROLE_INFO = 'role/info/',
}
export const apiGetRolePageList = (params: PageFilterParams) => defHttp.post<PageFilterResult<Role>>(Api.GET_ROLE_PAGE_LIST, { ...params });
export const apiSaveRole = (params: Role) => defHttp.post(Api.SAVE_ROLE, { ...params });
export const apiChangeIsActivated = (params: ChangeIsActivated) => defHttp.post(Api.CHANGE_IS_ACTIVATED, { ...params });
export const apiGetRoleInfo = (roleId: string) => defHttp.get<Role>(Api.GET_ROLE_INFO + roleId);
