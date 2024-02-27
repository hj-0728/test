import { defineStore } from 'pinia';
import { store } from '/@/store';

interface ChangeRoleState {
  needClearTabs: boolean;
  refreshSideBarKey: number;
}

export const useChangeRoleStore = defineStore({
  id: 'useChangeStore',
  state: (): ChangeRoleState => ({
    needClearTabs: false,
    refreshSideBarKey: 1,
  }),
  getters: {},
  actions: {
    setNeedClearTabs(needClearTabs: boolean): any {
      this.$state.needClearTabs = needClearTabs;
    },
    setRefreshSideBarKey(refreshSideBarKey: number): any {
      this.$state.refreshSideBarKey = refreshSideBarKey;
    },
  },
});

export function useFillInStoreWithOut() {
  return useChangeRoleStore(store);
}
