import { BasicResponseModel } from '/@/api/model/baseModel';

export interface FileExtInfoModel extends BasicResponseModel {
  storageInfoId: string;
  originalName: string;
  summary: string | null;
  bucketName: string;
  objectName: string;
  checksum: string;
  size: number;
  url: string | null;
}
