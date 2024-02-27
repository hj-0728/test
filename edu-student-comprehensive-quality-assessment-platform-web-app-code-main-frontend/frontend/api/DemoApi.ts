import defHttp from './BasicApi';
import { DemoTableParams, SaveDemoData } from '../model/Demo.model';

enum Api {
  GET_DEMO_TABLE = 'demo/table',
  SAVE_DEMO = 'demo/save',
}

export const apiGetDemoTable = (params: DemoTableParams) => defHttp.post(Api.GET_DEMO_TABLE, params);

export const apiSaveDemoData = (data: SaveDemoData) => defHttp.post(Api.SAVE_DEMO, data);
