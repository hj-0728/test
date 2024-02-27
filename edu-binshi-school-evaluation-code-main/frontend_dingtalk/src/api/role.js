import request from '../utils/request';

/*
职责切换
 */
export async function apiSwitchRole(roleId) {
    return request({
        url: `role/switch-role/${roleId}`,
        method: 'get'
    });
}
