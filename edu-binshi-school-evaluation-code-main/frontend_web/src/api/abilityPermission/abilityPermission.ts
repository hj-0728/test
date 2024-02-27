import {
  abilityPermissionTreeModel,
  GrantedResponseModel,
  SaveGrantedResponseModel,
} from '/@/api/abilityPermission/model/abilityPermissionModel';
import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';

enum Api {
  SAVE_ABILITY_PERMISSION_ASSIGN = '/ability-permission/assign',
  GET_ABILITY_PERMISSION_ASSIGN_TREE = '/ability-permission/assign-tree',
  GET_ABILITY_PERMISSION_TREE = '/ability-permission/tree',
  DELETE_ABILITY_PERMISSION = '/ability-permission/delete/',
  UPDATE_SORT_ABILITY_PERMISSION = '/ability-permission/update-sort',
  CREATE_ABILITY_PERMISSION = '/ability-permission/create',
  EDIT_ABILITY_PERMISSION = '/ability-permission/edit',
}

/**
 * @description:获取功能授权树
 */
export const apiGetAbilityPermissionAssignTree = (params: GrantedResponseModel) => {
  return defHttp.post<any>({
    url: Api.GET_ABILITY_PERMISSION_ASSIGN_TREE,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });
};

/**
 * @description:保存功能权限授权
 */
export const apiSaveAbilityPermissionAssign = (params: SaveGrantedResponseModel) => {
  return defHttp.post<any>({
    url: Api.SAVE_ABILITY_PERMISSION_ASSIGN,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });
};

/**
 * @description: 获取功能权限树
 */
export function apiGetAbilityPermissionTree() {
  return defHttp.get<abilityPermissionTreeModel>(
    {
      url: Api.GET_ABILITY_PERMISSION_TREE,
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
}

/**
 * @description: 删除功能权限
 */
export function apiDeleteAbilityPermission(permissionId) {
  return defHttp.post<BasicResponseModel>(
    {
      url: Api.DELETE_ABILITY_PERMISSION + permissionId,
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
}

/**
 * @description: 更新权限树的排序
 */
export function apiUpdateAbilityPermissionSort(params) {
  return defHttp.post<BasicResponseModel>(
    {
      url: Api.GET_ABILITY_PERMISSION_TREE,
      params: params,
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
}
/**
 * @description: 创建功能权限
 */
export function apiCreateAbilityPermission(params) {
  return defHttp.post<BasicResponseModel>(
    {
      url: Api.CREATE_ABILITY_PERMISSION,
      params: params,
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
}

/**
 * @description: 编辑功能权限
 */
export function apiEditAbilityPermission(params) {
  return defHttp.post<BasicResponseModel>(
    {
      url: Api.EDIT_ABILITY_PERMISSION,
      params: params,
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
}
