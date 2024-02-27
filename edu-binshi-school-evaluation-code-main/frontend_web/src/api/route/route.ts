import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';
import { RouteEditModel, routeQueryParamsModel } from '/@/api/route/routeModel';

enum Api {
  GET_PATH_LIST = '/route/list',
  EDIT_PATH_LIST = '/route/edit',
  ACCESS_STRATEGY = '/route/access-strategy',
  GET_ROUTE_ABILITY_PERMISSION_ASSIGN_TREE = '/route/assign-tree',
}

/**
 * 获取路径列表
 */
export function apiGetPathList(params: routeQueryParamsModel) {
  return defHttp.post<BasicResponseModel>({
    url: Api.GET_PATH_LIST,
    params: params,
    headers: {
      ignoreCancelToken: true,
    },
  });
}

/**
 * 编辑路径列表
 */
export function apiEditPath(params: RouteEditModel) {
  return defHttp.post<any>({
    url: Api.EDIT_PATH_LIST,
    params: params,
    headers: {
      ignoreCancelToken: true,
    },
  });
}

/**
 * 获取路径身份验证
 */
export function apiGetRouteAccessStrategy() {
  return defHttp.get<any>({
    url: Api.ACCESS_STRATEGY,
    headers: {
      ignoreCancelToken: true,
    },
  });
}

/**
 * 获取路由功能权限树
 */
export function apiGetRouteAbilityPermissionAssignTree(param) {
  return defHttp.get<any>({
    url: Api.GET_ROUTE_ABILITY_PERMISSION_ASSIGN_TREE + '/' + param,
    headers: {
      ignoreCancelToken: true,
    },
  });
}
