import { defHttp } from '/@/utils/http/axios';
import { BasicResponseModel } from '/@/api/model/baseModel';

enum Api {
  UPLOAD_FILE = '/storage/upload-files',
  GET_FILE_DOWNLOAD_URL = '/storage/get-file-download-url/',
}

/**
 * @description: 文件上传
 */
export const apiUpload = (params) => {
  return defHttp.post<BasicResponseModel>(
    {
      url: Api.UPLOAD_FILE,
      params: params,
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
};

/**
 * @description: 获取文件url
 */
export const apiGetFileUrl = (fileId) => {
  return defHttp.get<any>(
    {
      url: Api.GET_FILE_DOWNLOAD_URL + fileId,
      headers: {
        ignoreCancelToken: true,
      },
    },
    {
      isReturnNativeResponse: false,
      isTransformResponse: false,
    },
  );
};
