import request from '../utils/request';

/*
职责切换
 */
export async function apiSwitchCapacity(capacityCode) {
    return request({
        url: `capacity/switch-capacity/${capacityCode}`,
        method: 'get'
    });
}
