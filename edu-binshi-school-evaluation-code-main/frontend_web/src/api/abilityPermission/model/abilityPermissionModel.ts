import { BasicResponseModel } from '/@/api/model/baseModel';

/**
 * @description: menu tree interface return value
 */

export interface abilityPermissionTree {
  id: string;
  name: string;
  code: string;
  version: number;
  nodeType: string;
  parentId: string;
  treeId: string;
  treeVersion: number;
  seq: number;
  children: abilityPermissionTree[];
}

export interface abilityPermissionTreeModel extends BasicResponseModel {
  data: abilityPermissionTree;
}

export interface GrantedResponseModel {
  assignResourceCategory: string;
  assignResourceId: string;
}

export interface SaveGrantedResponseModel extends GrantedResponseModel {
  abilityPermissionIdList: string[];
}
