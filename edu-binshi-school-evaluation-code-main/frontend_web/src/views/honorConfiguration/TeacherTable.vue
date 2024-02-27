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
      <template #toolbar>
        <Button
          type="primary"
          color="success"
          :iconSize="18"
          preIcon="ant-design:plus-outlined"
          class="ant-btn-left-margin"
          @click="toAdd"
        >
          添加
        </Button>
      </template>
      <template #bodyCell="{ column, record }">
        <template v-if="column.dataIndex === 'imgUrl'">
          <img :src="record.imgUrl" style="max-height: 40px; margin-left: 30px" />
        </template>
        <template v-if="column.dataIndex === 'operation'">
          <Button
            type="primary"
            color="edit"
            :iconSize="16"
            preIcon="ant-design:setting-filled"
            @click="setSubject(record)"
          >
            编辑
          </Button>
          <Button
            type="primary"
            color="error"
            :iconSize="16"
            preIcon="material-symbols:delete-outline-rounded"
            class="ant-btn-left-margin"
            @click="deleteEvaluationCriteria(record)"
          >
            删除
          </Button>
        </template>
      </template>
    </BasicTable>
    <AddPeriod @register="registerSetSubjectModal" />
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { BasicTable, useTable } from '/@/components/Table';
  import { getBasicColumns } from '/@/views/honorConfiguration/teacherTableData';
  import { Input } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { useModal } from '/@/components/Modal';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { apiK12TeacherListPage } from '/@/api/k12TeacherSubject/k12TeacherSubject';
  import headerImg from '/@/assets/images/header.jpg';
  import specialA from '/@/assets/images/specialA.png';
  import specialB from '/@/assets/images/specialB.png';
  import specialC from '/@/assets/images/specialC.png';
  import studyA from '/@/assets/images/studyA.png';
  import studyB from '/@/assets/images/studyB.png';
  import studyC from '/@/assets/images/studyC.png';
  import AddPeriod from '/@/views/honorConfiguration/AddPeriod.vue';

  export default defineComponent({
    components: {
      BasicTable,
      InputSearch: Input.Search,
      Button,
      AddPeriod,
    },
    props: {
      dimensionDeptTreeId: {
        type: String,
        default: '',
      },
      periodId: {
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
      const getStudentPage = () => {
        loading.value = true;
        apiK12TeacherListPage(params)
          .then((res) => {
            if (res.code === 200) {
              if (props.dimensionDeptTreeId === '0bbb5d09-7c76-4b86-ba8b-e9d1649c6eb0') {
                res.data.data = [
                  {
                    imgUrl: specialA,
                    peopleName: '一级特殊奖',
                    deptName: '一年级',
                    capacityName: '30',
                  },
                  {
                    imgUrl: specialC,
                    peopleName: '二级特殊奖',
                    deptName: '一年级',
                    capacityName: '90',
                  },
                  {
                    imgUrl: specialB,
                    peopleName: '三级特殊奖',
                    deptName: '一年级',
                    capacityName: '270',
                  },
                ];
              } else {
                res.data.data = [
                  {
                    imgUrl: studyA,
                    peopleName: '一级学习奖',
                    deptName: '二年级',
                    capacityName: '10',
                  },
                  {
                    imgUrl: studyB,
                    peopleName: '二级学习奖',
                    deptName: '二年级',
                    capacityName: '30',
                  },
                  {
                    imgUrl: studyC,
                    peopleName: '三级学习奖',
                    deptName: '二年级',
                    capacityName: '90',
                  },
                ];
              }
              total.value = 5;
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
        headerImg,
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
      toAdd(data) {
        this.openSetSubjectModal(true, {
          peopleId: data.peopleId,
          peopleName: data.peopleName,
          dimensionDeptTreeId: data.dimensionDeptTreeId,
          deptName: data.deptName,
        });
      },
      deleteEvaluationCriteria(data) {
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: '确定要删除吗？',
          onOk: () => {
            console.log(data);
          },
          onCancel: () => {},
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
