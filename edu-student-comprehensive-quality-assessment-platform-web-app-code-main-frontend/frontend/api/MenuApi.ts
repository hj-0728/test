import { Menu, MenuTree, UpdateMenuSort } from '@/model/Menu.model';
import defHttp from './BasicApi';

enum Api {
    SAVE_MENU = 'menu/save',
    GET_MENU_INFO = 'menu/get-info/',
    GET_MENU_TREE = 'menu/get-tree',
    DELETE_MENU = 'menu/delete/',
    UPDATE_SORT = 'menu/update-sort',
}

export const apiSaveMenu = (params: Menu) => defHttp.post(Api.SAVE_MENU, params);
export const apiGetMenuInfo = (menuId: string) => defHttp.get<Menu>(Api.GET_MENU_INFO + menuId);
export const apiGetMenuTree = (searchText: string) => defHttp.post<MenuTree[]>(Api.GET_MENU_TREE, { searchText, menuCategory: 'WEB' });
export const apiDeleteMenu = (menuId: string) => defHttp.post(Api.DELETE_MENU + menuId);
export const apiUpdateSort = (params: UpdateMenuSort[]) => defHttp.post(Api.UPDATE_SORT, params);
