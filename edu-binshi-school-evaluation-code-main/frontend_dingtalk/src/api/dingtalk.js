// 微信


import request from "../utils/request";

/*
获取微信签名
 */
export async function apiGetSignature(data) {
    return request({
        url: `dingtalk/get-signature`,
        method: 'post',
        data: data
    });
}