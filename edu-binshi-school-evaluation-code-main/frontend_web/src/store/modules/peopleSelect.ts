import { defineStore } from 'pinia';
import { apiGetStudentInfoListByEstablishmentAssignIdList } from '/@/api/student/student';

interface People {
  peopleId: string;
  establishmentAssignId: string;
  schoolClass: string;
  studentName: string;
  grade: string;
}

interface Params {
  searchText: string;
  pageIndex: number;
  pageSize: number;
  draw: number;
}

interface PeopleSelectState {
  peopleList: Array<People>;
  peopleIdList: Array<string>;
  selectedRowKeys: Array<string>;
  filters: Array<string> | null;
  filtersForSelect: Array<string> | null;
  params: Params;
  paramsForSelect: Params;
}

export const useStudentSelectStore = defineStore({
  id: 'people-select-store',
  state: (): PeopleSelectState => ({
    peopleList: [],
    peopleIdList: [],
    selectedRowKeys: [],
    filters: [],
    filtersForSelect: [],
    params: {
      searchText: '',
      pageIndex: 0,
      pageSize: 10,
      draw: 1,
    },
    paramsForSelect: {
      searchText: '',
      pageIndex: 0,
      pageSize: 10,
      draw: 1,
    },
  }),
  getters: {},
  actions: {
    initPeopleSelectStore(peopleIdList: string[]) {
      this.saveParams('pageIndex', 0);
      this.saveParams('searchText', '');
      this.saveParams('draw', 1);
      this.saveParamsForSelect('pageIndex', 0);
      this.saveParamsForSelect('searchText', '');
      this.saveParamsForSelect('draw', 1);
      this.saveFilters([]);
      this.saveFiltersForSelect([]);
      this.$state.peopleIdList = [];
      this.$state.peopleList = [];
      this.$state.selectedRowKeys = [];
      apiGetStudentInfoListByEstablishmentAssignIdList(peopleIdList).then((res) => {
        if (res.code === 200) {
          this.$state.peopleIdList = [];
          this.$state.peopleList = [];
          this.$state.selectedRowKeys = [];
          for (const people of res.data) {
            this.saveSelectedPeople(people);
          }
        }
      });
    },
    saveParams(key, value) {
      this.$state.params[key] = value;
    },
    saveParamsForSelect(key, value) {
      this.$state.paramsForSelect[key] = value;
    },
    saveFilters(filters: Array<string> | null) {
      this.$state.filters = filters;
    },
    saveFiltersForSelect(filtersForSelect: Array<string> | null) {
      this.$state.filtersForSelect = filtersForSelect;
    },
    saveSelectedPeople(selectedPeople: People, selectType = 'checkbox') {
      const idx = this.$state.selectedRowKeys.indexOf(selectedPeople.establishmentAssignId);
      if (idx < 0) {
        if (selectType === 'radio') {
          this.$state.peopleList = [selectedPeople];
          this.$state.peopleIdList = [selectedPeople.peopleId];
          this.$state.selectedRowKeys = [selectedPeople.establishmentAssignId];
        } else {
          this.$state.peopleList.push(selectedPeople);
          this.$state.peopleIdList.push(selectedPeople.peopleId);
          this.$state.selectedRowKeys.push(selectedPeople.establishmentAssignId);
        }
      } else {
        this.$state.peopleList.splice(idx, 1);
        this.$state.peopleIdList.splice(idx, 1);
        this.$state.selectedRowKeys.splice(idx, 1);
      }
    },
  },
});
