import { DeleteScene, Scene, SceneEditModal, TerminalCategory } from '@/model/Scene.model';
import defHttp from './BasicApi';

enum Api {
  GET_SCENE_LIST = 'scene/list',
  SAVE_SCENE = 'scene/save',
  DELETE_SCENE = 'scene/delete',
  GET_SCENE_INFO = 'scene/info/',
  GET_TERMINAL_CATEGORY_LIST = 'scene/terminal-category-list',
}
export const apiGetSceneList = () => defHttp.get<Scene[]>(Api.GET_SCENE_LIST);
export const apiSaveScene = (params: SceneEditModal) => defHttp.post(Api.SAVE_SCENE, { ...params });
export const apiDeleteScene = (params: DeleteScene) =>
  defHttp.post(Api.DELETE_SCENE, { ...params });
export const apiGetSceneInfo = (sceneId: string) =>
  defHttp.get<Scene>(Api.GET_SCENE_INFO + sceneId);
export const apiGetTerminalCategoryList = () =>
  defHttp.get<TerminalCategory[]>(Api.GET_TERMINAL_CATEGORY_LIST);
