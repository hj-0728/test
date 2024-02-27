export interface Scene {
  id?: string;
  version?: number;
  name: string;
  code: string;
  terminalCategoryList: string[];
  terminalCategoryNameList: string[];
  observationPointStatistics: ObservationPointStatistic[];
}

export interface SceneEditModal {
  id?: string;
  version?: number;
  name?: string;
  code?: string;
  terminalCategoryList?: string[];
  observationPointIdList?: string[];
}

export interface DeleteScene {
  sceneId: string;
}

export interface ObservationPointStatistic {
  category: string;
  category_name: string | null;
  num: number;
}

export interface TerminalCategory {
  label: string;
  value: string;
}
