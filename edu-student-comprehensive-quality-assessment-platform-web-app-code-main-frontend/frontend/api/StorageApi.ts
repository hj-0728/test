import defHttp from './BasicApi';
import { FileItem } from "@/model/Storage.model";

enum Api {
    UPLOAD_FILES = 'storage/upload-files',
}

export const apiUploadFiles = (params: FormData) => defHttp.post<FileItem[]>(Api.UPLOAD_FILES, null, params);
