import request from '../utils/request';

// 保存访问记录
export async function apiSaveAccessLog(data) {
    return request({
        url: 'access-log/save',
        method: 'post',
        data: data
    })
}
