import request from "../utils/request";

/*
获取用户信息
 */
export async function apiGetDingtalkUserInfo() {
    return request({
        url: `dingtalk-user/info`,
        method: 'get',
    });
}
