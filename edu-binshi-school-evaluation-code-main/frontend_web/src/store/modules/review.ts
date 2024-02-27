import { defineStore } from 'pinia';
import { store } from '/@/store';

export const useReviewStore = defineStore({
  id: 'app-review',
  state: (): {
    specializedFieldId: null;
    deductedStandardId: null;
    indexDefAspectId: null;
  } => ({
    specializedFieldId: null,
    deductedStandardId: null,
    indexDefAspectId: null,
  }),
  getters: {
    getSpecializedFieldId(): string | null {
      return this.specializedFieldId;
    },
    getDeductedStandardId(): string | null {
      return this.deductedStandardId;
    },
  },
  actions: {
    setSpecializedFieldId(id: string | null) {
      // @ts-ignore
      this.specializedFieldId = id;
    },
    setDeductedStandardId(id: string | null) {
      // @ts-ignore
      this.deductedStandardId = id;
    },
    setIndexDefAspectId(id: string | null) {
      // @ts-ignore
      this.indexDefAspectId = id;
    },
    reset() {
      this.specializedFieldId = null;
      this.deductedStandardId = null;
      this.indexDefAspectId = null;
    },
  },
});

// Need to be used outside the setup
export function useReviewStoreWithOut() {
  return useReviewStore(store);
}
