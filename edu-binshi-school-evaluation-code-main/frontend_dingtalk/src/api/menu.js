import request from '../utils/request';

// 获取菜单列表
export async function apiGetMenuList() {
    return request({
        url: `/menu/list`,
        method: 'get',
    })
}
