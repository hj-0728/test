<template>
  <div>
    <BasicTable
      :dataSource="tableData"
      :canResize="true"
      :loading="loading"
      :scroll="{ x: 0 | false, y: tableHeight }"
      :showIndexColumn="false"
      @register="registerTable"
      @change="onChange"
      :row-selection="{
        type: 'checkbox',
        selectedRowKeys: pStore.$state.selectedRowKeys,
        onSelect: onSelect,
        onSelectAll: onSelectAll,
      }"
      rowKey="establishmentAssignId"
      :pagination="{ total: total, pageSize: pageSize, current: pageIndex + 1 }"
    >
      <template #tableTitle>
        <InputSearch
          v-model:value="searchText"
          placeholder="搜索"
          enter-button
          @search="onSearch"
          style="padding: 5px 0; width: 30%"
        />
      </template>
      <template #bodyCell="{ column, record }">
        <template v-if="column.dataIndex === 'dept'">
          <span>{{ record.grade + '/' + record.schoolClass }}</span>
        </template>
      </template>
      <template #toolbar>
        <Button
          :type="selectShow ? 'default' : 'primary'"
          :color="selectShow ? undefined : 'blue'"
          :iconSize="16"
          preIcon="ant-design:eye-outlined"
          class="ant-btn-left-margin"
          @click="showOriginTable"
        >
          原数据
        </Button>
        <Button
          :type="selectShow ? 'primary' : 'default'"
          :color="selectShow ? 'blue' : undefined"
          preIcon="ic:baseline-check"
          :iconSize="16"
          style="margin-right: 10px"
          @click="showSelectedDataList"
        >
          已选择({{ pStore.$state.selectedRowKeys.length }})
        </Button>
        <Button
          type="primary"
          preIcon="ic:baseline-check"
          @click="confirmSelectedPeople"
          :iconSize="16"
        >
          {{ confirmButtonText }}
        </Button>
      </template>
    </BasicTable>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { BasicTable, useTable } from '/@/components/Table';
  import { getBasicColumns } from '/@/views/evaluationCriteriaPlan/components/peopleTableData';
  import { Input } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { UserInfo } from '/#/store';
  import { apiStudentPage } from '/@/api/student/student';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { getAuthCache } from '/@/utils/auth';
  import { USER_INFO_KEY } from '/@/enums/cacheEnum';
  import { useStudentSelectStore } from '/src/store/modules/peopleSelect';

  export default defineComponent({
    components: {
      BasicTable,
      InputSearch: Input.Search,
      Button,
    },
    props: {
      dimensionDeptTreeId: {
        type: String,
        default: '',
      },
    },
    setup(props) {
      const currentUserInfo: UserInfo = getAuthCache(USER_INFO_KEY);
      const currentRoleCode = currentUserInfo.currentRole?.code;

      const total = ref(0);
      const tableHeight = ref(getTableHeight(document) * 0.5);
      const loading = ref(false);
      const tableData = ref([]);
      const selectShow = ref(false);
      const pStore = useStudentSelectStore();
      const params = reactive({
        searchText: '',
        pageSize: selectShow.value
          ? pStore.$state.paramsForSelect.pageSize
          : pStore.$state.params.pageSize,
        pageIndex: selectShow.value
          ? pStore.$state.paramsForSelect.pageIndex
          : pStore.$state.params.pageIndex,
        draw: selectShow.value ? pStore.$state.paramsForSelect.draw : pStore.$state.params.draw,
        dimensionDeptTreeId: props.dimensionDeptTreeId,
      });
      const columns = ref();
      columns.value = getBasicColumns();
      const [registerTable] = useTable({
        columns: columns.value,
        bordered: true,
      });
      const getStudentPage = () => {
        loading.value = true;
        apiStudentPage(params)
          .then((res) => {
            if (res.code === 200) {
              total.value = res.data.filterCount;
              tableData.value = res.data.data;
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch(() => {
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络错误',
            });
          })
          .finally(() => {
            loading.value = false;
          });
      };
      getStudentPage();

      const confirmButtonText = ref('确认');

      const onSelect = (record, _selected = {}, _selectedRows = [], _nativeEvent = {}) => {
        pStore.saveSelectedPeople(record, 'checkbox');
        if (selectShow.value) {
          total.value = pStore.$state.peopleIdList.length;
        }
      };

      const onSelectAll = (_selected, _selectedRows, changeRows) => {
        for (const row of changeRows) {
          pStore.saveSelectedPeople(row);
        }
        if (selectShow.value) {
          total.value = pStore.$state.peopleIdList.length;
        }
      };
      return {
        loading,
        registerTable,
        ...toRefs(params),
        params,
        tableData,
        tableHeight,
        total,
        currentRoleCode,
        getStudentPage,
        selectShow,
        confirmButtonText,
        onSelect,
        onSelectAll,
        pStore,
      };
    },
    methods: {
      addSuccess() {
        this.pageSize = 20;
        this.pageIndex = 0;
        this.searchText = '';
        this.draw = 1;
        this.getStudentPage();
      },
      onSearch() {
        this.pageIndex = 0;
        this.getStudentPage();
      },
      onChange(pageInfo, _filters) {
        this.pageSize = pageInfo.pageSize;
        this.pageIndex = pageInfo.current - 1;
        if (this.selectShow) {
          this.searchForSelectShow();
        } else {
          this.getStudentPage();
        }
      },
      init() {
        this.pageSize = 20;
        this.pageIndex = 0;
        this.searchText = '';
        this.draw = 1;
      },
      showOriginTable() {
        this.selectShow = false;
        this.params.pageIndex = this.pStore.$state.params.pageIndex;
        this.params.searchText = this.pStore.$state.params.searchText;
        this.params.draw = this.pStore.$state.params.draw;
        this.getStudentPage();
      },
      showSelectedDataList() {
        this.selectShow = true;
        this.params.searchText = this.pStore.$state.paramsForSelect.searchText;
        this.total = this.pStore.$state.peopleList.length;
        this.tableData = this.pStore.$state.peopleList;
        this.searchForSelectShow();
      },
      searchForSelectShow() {
        this.filterAndSearchForSelect(
          { gender: this.pStore.$state.filtersForSelect },
          this.params.searchText,
        );
      },
      filterAndSearchForSelect(_filters, searchText) {
        let data: Array<object> = [];
        if (searchText.trim() !== '') {
          for (const rowData of this.pStore.$state.peopleList) {
            if (rowData['name'].indexOf(searchText.trim()) > -1) {
              data.push(rowData);
            }
          }
        } else {
          data = this.pStore.$state.peopleList;
        }
        this.tableData = data;
        this.total = data.length;
      },
      confirmSelectedPeople() {
        const selectedRowKeys = this.pStore.$state.selectedRowKeys;
        const peopleList = this.pStore.$state.peopleList;
        const total = this.total;
        this.$emit('confirmSelect', { selectedRowKeys, peopleList, total });
      },
    },
  });
</script>

<style scoped lang="less">
  ::v-deep(.vben-basic-table-header__toolbar) {
    margin-right: 0;
  }
</style>
