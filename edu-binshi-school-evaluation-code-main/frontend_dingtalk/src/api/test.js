import request from '../utils/request';


export async function apiGetTestInfo() {
    const info = new Date().getTime();
    return request({
        url: `test/get-test-info/` + info,
        method: 'get'
    });
}



export async function apiGetTestInfoWithAuth() {
    const info = new Date().getTime();
    return request({
        url: `test/get-test-info-with-auth/` + info,
        method: 'get'
    });
}