import { defineStore } from 'pinia';
import { store } from '/@/store';
import { CurrentPeriodInfo } from '/#/store';

export const usePeriodStore = defineStore({
  id: 'app-period',
  state: (): CurrentPeriodInfo => ({
    id: '',
    name: '',
    categoryCode: '',
  }),
  getters: {
    getPeriodId(): string {
      return this.id;
    },
    getPeriodName(): string {
      return this.name;
    },
  },
  actions: {
    setPeriod(periodInfo: CurrentPeriodInfo) {
      this.id = periodInfo.id;
      this.name = periodInfo.name;
      this.categoryCode = periodInfo.categoryCode;
    },
  },
});

// Need to be used outside the setup
export function usePeriodStoreWithOut() {
  return usePeriodStore(store);
}
