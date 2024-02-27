import { BasicPageQueryResponseModel } from '/@/api/model/baseModel';

export interface routeQueryParamsModel extends BasicPageQueryResponseModel {
  category: any;
  accessStrategy: any;
}

/**
 * 编辑列表
 */
export interface RouteEditModel {
  id: string;
  path: string;
  accessStrategy: string;
  accessStrategyNameName: string;
}
