import { BasicResponseModel } from '/@/api/model/baseModel';

/**
 * @description: menu tree interface return value
 */

export interface MenuTree {
  id: string;
  name: string;
  children: MenuTree[];
}

export interface MenuTreeModel extends BasicResponseModel {
  data: MenuTree;
}
