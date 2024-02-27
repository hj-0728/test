import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';
import { MenuTreeModel } from '/@/api/menu/model/menuModel';

const PREFIX = '/menu';

enum Api {
  GET_DB_MENU_TREE = '/get-db-tree',
  GET_MENU_TREE = '/tree',
  ADD_MENU = '/add',
  EDIT_MENU = '/edit',
  DELETE_MENU = '/delete',
  UPDATE_MENU_SORT = '/update-sort',
  GET_CURRENT_ROLE_MENU_PATH_LIST = '/current-role/path-list/web',
}

/**
 * @description: 获取用户菜单
 */

export const apiGetDBMenuTree = () => {
  return defHttp.get<any>({ url: PREFIX + Api.GET_DB_MENU_TREE });
};

/**
 * @description: menu api get menu tree
 */
export function apiGetMenuTree(category: string) {
  return defHttp.get<MenuTreeModel>({
    url: PREFIX + `${Api.GET_MENU_TREE}/${category}`,
  });
}

/**
 * @description: menu api add menu
 */
export function apiAddMenu(params) {
  return defHttp.post<BasicResponseModel>({
    url: PREFIX + Api.ADD_MENU,
    params: params,
  });
}

/**
 * @description: menu api edit menu
 */
export function apiEditMenu(params) {
  return defHttp.post<BasicResponseModel>({
    url: PREFIX + Api.EDIT_MENU,
    params: params,
  });
}

/**
 * @description: menu api delete menu
 */
export function apiDeleteMenu(menuId) {
  return defHttp.post<BasicResponseModel>({
    url: PREFIX + `${Api.DELETE_MENU}/${menuId}`,
  });
}

/**
 * @description: menu api delete menu
 */
export function apiUpdateMenuSort(params) {
  return defHttp.post<BasicResponseModel>({
    url: PREFIX + Api.UPDATE_MENU_SORT,
    params: params,
  });
}

/**
 * @description: 获取当前角色的菜单路径列表
 */
export function apiGetMenuPathList() {
  return defHttp.get<BasicResponseModel>({
    url: PREFIX + Api.GET_CURRENT_ROLE_MENU_PATH_LIST,
  });
}
