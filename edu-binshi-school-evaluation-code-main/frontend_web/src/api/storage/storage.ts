import { defHttp } from '/@/utils/http/axios';

enum Api {
  UPLOAD_FILE = '/storage/upload',
  GET_FILE_DOWNLOAD_URL = '/storage/get-file-url/',
}

/**
 * @description:上传文件
 */
export const apiUploadFile = (params: any) => {
  return defHttp.post<any>({
    url: Api.UPLOAD_FILE,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });
};

/**
 * @description:获取文件下载url
 */
export const apiGetFileDownloadUrl = (fileId) => {
  return defHttp.get({
    url: Api.GET_FILE_DOWNLOAD_URL + fileId,
  });
};
