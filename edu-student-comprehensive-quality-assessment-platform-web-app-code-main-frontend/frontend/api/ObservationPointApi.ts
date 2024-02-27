import { MessageCarrier } from '@/model/Basic.model';
import {
    DeleteObservationPoint, ObservationPoint,
    ObservationPointList,
    ObservationPointSystemIcon,
    SaveObservationPoint,
} from '@/model/ObservationPoint.model';
import defHttp from './BasicApi';

enum Api {
    GET_OBSERVATION_POINT_LIST = 'observation-point/list',
    SAVE_OBSERVATION_POINT = 'observation-point/save',
    DELETE_OBSERVATION_POINT = 'observation-point/delete',
    GET_OBSERVATION_POINT_SYSTEM_ICON = 'observation-point/get-system-icon/',
    GET_OBSERVATION_POINT_INFO = 'observation-point/get-observation-point/',
}

export const apiGetObservationPointList = () => defHttp.get<ObservationPointList>(Api.GET_OBSERVATION_POINT_LIST);
export const apiSaveObservationPoint = (params: SaveObservationPoint) => defHttp.post<MessageCarrier<null>>(Api.SAVE_OBSERVATION_POINT, params);
export const apiDeleteObservationPoint = (params: DeleteObservationPoint) => defHttp.post<MessageCarrier<null>>(Api.DELETE_OBSERVATION_POINT, params);
export const apiGetObservationPointSystemIcon = (category: string) => defHttp.get<ObservationPointSystemIcon[]>(Api.GET_OBSERVATION_POINT_SYSTEM_ICON + category);
export const apiGetObservationPointInfo = (observationPointId: string) => defHttp.get<ObservationPoint>(Api.GET_OBSERVATION_POINT_INFO + observationPointId);
