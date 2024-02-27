<template>
  <div>
    <BasicTable
      :dataSource="tableData"
      :canResize="true"
      :loading="loading"
      :scroll="{ y: tableHeight }"
      :showIndexColumn="false"
      @register="registerTable"
      @change="onChange"
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
        <template v-if="column.dataIndex === 'operation'">
          <Button
            type="primary"
            color="edit"
            :iconSize="16"
            preIcon="ant-design:setting-filled"
            @click="setSubject(record)"
          >
            设置科目
          </Button>
        </template>
      </template>
    </BasicTable>
    <SetSubjectModel @register="registerSetSubjectModal" @refresh-table="getStudentPage" />
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { BasicTable, useTable } from '/@/components/Table';
  import { getBasicColumns } from '/@/views/teacherManage/deptTeacher/teacherTableData';
  import { Input } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { useModal } from '/@/components/Modal';
  import { useMessage } from '/@/hooks/web/useMessage';
  import {
    apiGetCapacityAndSubjectFilters,
    apiK12TeacherListPage,
  } from '/@/api/k12TeacherSubject/k12TeacherSubject';
  import SetSubjectModel from '/@/views/teacherManage/deptTeacher/SetSubjectModel.vue';

  export default defineComponent({
    components: {
      SetSubjectModel,
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
      const [registerSetSubjectModal, { openModal: openSetSubjectModal }] = useModal();
      const total = ref(0);
      const tableHeight = ref(getTableHeight(document));
      const loading = ref(false);
      const tableData = ref([]);
      const params = reactive({
        pageSize: 20,
        pageIndex: 0,
        searchText: '',
        draw: 1,
        dimensionDeptTreeId: props.dimensionDeptTreeId,
        subjectNameList: [],
        capacityNameList: [],
      });
      const columns = ref();
      columns.value = getBasicColumns();
      const [registerTable] = useTable({
        columns: columns.value,
        bordered: true,
      });
      const getCapacityAndSubjectFilters = () => {
        loading.value = true;
        apiGetCapacityAndSubjectFilters()
          .then((res) => {
            if (res.code === 200) {
              console.log(res.data, 'res.data');
              columns.value.forEach(function (item) {
                if (item.dataIndex == 'capacityName') {
                  item.filters = res.data.capacityFilters;
                }
                if (item.dataIndex == 'subjectName') {
                  item.filters = res.data.subjectFilters;
                }
              });
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
      getCapacityAndSubjectFilters();
      const getStudentPage = () => {
        loading.value = true;
        apiK12TeacherListPage(params)
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
      return {
        loading,
        registerTable,
        ...toRefs(params),
        params,
        tableData,
        tableHeight,
        total,
        getStudentPage,
        registerSetSubjectModal,
        openSetSubjectModal,
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
      onChange(pageInfo, filters) {
        this.pageSize = pageInfo.pageSize;
        this.pageIndex = pageInfo.current - 1;
        this.params.subjectNameList = filters.subjectName ? filters.subjectName : [];
        this.params.capacityNameList = filters.capacityName ? filters.capacityName : [];
        this.getStudentPage();
      },
      init() {
        this.pageSize = 20;
        this.pageIndex = 0;
        this.searchText = '';
        this.draw = 1;
      },
      setSubject(data) {
        this.openSetSubjectModal(true, {
          peopleId: data.peopleId,
          peopleName: data.peopleName,
          dimensionDeptTreeId: data.dimensionDeptTreeId,
          deptName: data.deptName,
        });
      },
    },
  });
</script>

<style scoped lang="less">
  ::v-deep(.vben-basic-table-header__toolbar) {
    margin-right: 0;
  }
</style>
