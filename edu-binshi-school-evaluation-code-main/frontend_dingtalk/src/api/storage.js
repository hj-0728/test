// 对象存储API

import request from '../utils/request';

/*
上传文件
 */
export async function apiUploadFile(params) {
    return request({
        url: 'storage/upload-files',
        method: 'post',
        data:params
    });
}
