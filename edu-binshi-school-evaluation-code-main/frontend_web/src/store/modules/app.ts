import type {
  ProjectConfig,
  HeaderSetting,
  MenuSetting,
  TransitionSetting,
  MultiTabsSetting,
} from '/#/config';
import type { BeforeMiniState } from '/#/store';

import { defineStore } from 'pinia';
import { store } from '/@/store';

import { ThemeEnum } from '/@/enums/appEnum';
import { APP_DARK_MODE_KEY_, PROJ_CFG_KEY } from '/@/enums/cacheEnum';
import { Persistent } from '/@/utils/cache/persistent';
import { darkMode } from '/@/settings/designSetting';
import { resetRouter } from '/@/router';
import { deepMerge } from '/@/utils';
import { useRouter } from 'vue-router';

interface AppState {
  darkMode?: ThemeEnum;
  // Page loading status
  pageLoading: boolean;
  // project config
  projectConfig: ProjectConfig | null;
  // When the window shrinks, remember some states, and restore these states when the window is restored
  beforeMiniInfo: BeforeMiniState;
  updatePasswordStatus: string;
  logoutStatus: string;
  updateUnreadStatusFlag: boolean;
}
let timeId: TimeoutHandle;
export const useAppStore = defineStore({
  id: 'app',
  state: (): AppState => ({
    darkMode: undefined,
    pageLoading: false,
    projectConfig: Persistent.getLocal(PROJ_CFG_KEY),
    beforeMiniInfo: {},
    updatePasswordStatus: '',
    logoutStatus: '',
    updateUnreadStatusFlag: false,
  }),
  getters: {
    getLogoutStatus(): string {
      return this.logoutStatus;
    },
    getUpdatePasswordStatus(): string {
      return this.updatePasswordStatus;
    },
    getPageLoading(): boolean {
      return this.pageLoading;
    },
    getDarkMode(): 'light' | 'dark' | string {
      return this.darkMode || localStorage.getItem(APP_DARK_MODE_KEY_) || darkMode;
    },

    getBeforeMiniInfo(): BeforeMiniState {
      return this.beforeMiniInfo;
    },

    getProjectConfig(): ProjectConfig {
      return this.projectConfig || ({} as ProjectConfig);
    },

    getHeaderSetting(): HeaderSetting {
      return this.getProjectConfig.headerSetting;
    },
    getMenuSetting(): MenuSetting {
      return this.getProjectConfig.menuSetting;
    },
    getTransitionSetting(): TransitionSetting {
      return this.getProjectConfig.transitionSetting;
    },
    getMultiTabsSetting(): MultiTabsSetting {
      return this.getProjectConfig.multiTabsSetting;
    },
    getUpdateUnreadStatusFlag() {
      return this.updateUnreadStatusFlag;
    },
    getActiveMenu(): string {
      const { currentRoute } = useRouter();
      if (currentRoute.value.meta.currentActiveMenu) {
        return currentRoute.value.meta.currentActiveMenu;
      } else {
        return currentRoute.value.fullPath;
      }
    },
  },
  actions: {
    setLogoutStatus(logoutStatus: string) {
      this.logoutStatus = logoutStatus;
    },
    setUpdatePasswordStatus(updatePasswordStatus: string) {
      this.updatePasswordStatus = updatePasswordStatus;
    },
    setPageLoading(loading: boolean): void {
      this.pageLoading = loading;
    },

    setDarkMode(mode: ThemeEnum): void {
      this.darkMode = mode;
      localStorage.setItem(APP_DARK_MODE_KEY_, mode);
    },

    setBeforeMiniInfo(state: BeforeMiniState): void {
      this.beforeMiniInfo = state;
    },

    setProjectConfig(config: DeepPartial<ProjectConfig>): void {
      this.projectConfig = deepMerge(this.projectConfig || {}, config);
      Persistent.setLocal(PROJ_CFG_KEY, this.projectConfig);
    },

    setUpdateUnreadStatusFlag(updateUnreadStatusFlag: boolean) {
      this.updateUnreadStatusFlag = updateUnreadStatusFlag;
    },

    async resetAllState() {
      resetRouter();
      Persistent.clearAll();
    },
    async setPageLoadingAction(loading: boolean): Promise<void> {
      if (loading) {
        clearTimeout(timeId);
        // Prevent flicker
        timeId = setTimeout(() => {
          this.setPageLoading(loading);
        }, 50);
      } else {
        this.setPageLoading(loading);
        clearTimeout(timeId);
      }
    },
  },
});

// Need to be used outside the setup
export function useAppStoreWithOut() {
  return useAppStore(store);
}
