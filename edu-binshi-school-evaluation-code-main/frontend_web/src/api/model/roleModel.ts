import { BasicResponseModel } from '/@/api/model/baseModel';

export interface RoleListResponseModel {
  searchText: string;
}

export interface changeIsActivatedResponseModel {
  id: string;
  version: number;
  isActivated: boolean;
}

export interface SaveRoleResponseModel {
  id: string;
  version: number;
  name: string;
  code: string;
  description: string;
  isActivated: boolean;
}

export interface DeleteRoleResponseModel {
  id: string;
}

export interface RoleListAddedToUserModel {
  id: string;
  version: number;
  name: string;
  code?: string;
  description?: string;
  is_activated: boolean;
}

export interface RoleListAddedToUserReturnModel extends BasicResponseModel {
  data: RoleListAddedToUserModel[];
}

export interface RoleWithManualModel {
  id: string;
  version: number;
  name: string;
  code?: string;
  description?: string;
  is_activated: boolean;
  manual_object_name?: string;
  manual_bucket_name?: string;
  manual_file_url?: string;
}

export interface RoleWithManualListReturnModel extends BasicResponseModel {
  data: RoleWithManualModel[];
  code: number;
}
