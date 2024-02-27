import { defHttp } from '/@/utils/http/axios';
import { SaveTemplateResponseModel } from './model/templateListModel';
import { BasicPageQueryParamsModel, BasicResponseModel } from '../model/baseModel';

enum Api {
  TEMPLATE_INFO = '/template/info/',
  SAVE_TEMPLATE = '/template/save',
  LIST = '/template/list',
  TREE = '/template/tree',
  GET_ASPECT_REPORT_DATA = '/test/get-aspect-report',
}

/**
 * @description: Save sample list value
 * test
 */

export const apiGetAspectReportData = () =>
  defHttp.get<BasicResponseModel>({
    url: Api.GET_ASPECT_REPORT_DATA,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * @description: Save sample list value
 * test
 */

export const apiSaveTemplate = (params: SaveTemplateResponseModel) =>
  defHttp.post<any>({
    url: Api.SAVE_TEMPLATE,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * @description: get template  value
 */

export const apiGetTemplateInfo = (templateId: string) =>
  defHttp.get<any>({
    url: Api.TEMPLATE_INFO + templateId,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * @description: get sample list
 */

export const apiGetTemplateList = (params: BasicPageQueryParamsModel) =>
  defHttp.post<any>({
    url: Api.LIST,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });

/**
 * @description: get sample tree
 */

export const apiGetTemplateTree = (params) =>
  defHttp.post<any>({
    url: Api.TREE,
    params,
    headers: {
      ignoreCancelToken: true,
    },
  });
/**
 * @description : get sample listdata
 * */
