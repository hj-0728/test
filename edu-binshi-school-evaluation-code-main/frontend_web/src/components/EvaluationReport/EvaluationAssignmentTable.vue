<template>
  <div>
    <ViewPdfModal
      ref="refViewPdfModal"
      @register="registerViewPdfModal"
      @download-assignment-report="downloadEvaluationAssignmentReport"
    />
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
          v-if="tableData && tableData.length > 0"
          type="primary"
          color="purple"
          :iconSize="18"
          preIcon="ph:download-simple"
          class="ant-btn-left-margin"
          title="导出报告"
          @click="exportDeptReport()"
          >导出报告
        </Button>
      </template>
      <template #bodyCell="{ column, record }">
        <template v-if="column.dataIndex === 'operation'">
          <Button
            type="primary"
            :iconSize="16"
            preIcon="ic:baseline-remove-red-eye"
            class="view-report-button-style"
            v-if="record['reportFileId']"
            @click="viewPdf(record)"
          >
            查看
          </Button>
          <Button
            type="primary"
            color="edit"
            :iconSize="16"
            preIcon="ph:download-simple"
            @click="downloadEvaluationAssignmentReport(record)"
          >
            下载
          </Button>
        </template>
      </template>
    </BasicTable>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs, watch, inject } from 'vue';
  import { BasicTable, useTable } from '/@/components/Table';
  import { getBasicColumns } from '/@/components/EvaluationReport/EvaluationAssignmentTableData';
  import { Input } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { useModal } from '/@/components/Modal';
  import { useMessage } from '/@/hooks/web/useMessage';
  import {
    apiGetDimensionDeptTreeReport,
    apiGetEvaluationAssignmentReportReport,
    apiGetEvaluationReportAssignmentPageList,
  } from '/@/api/evaluationReport/evaluationReport';
  import ViewPdfModal from '/@/components/pdf/viewPdfModal.vue';

  export default defineComponent({
    components: {
      BasicTable,
      InputSearch: Input.Search,
      Button,
      ViewPdfModal,
    },
    props: {
      planId: {
        type: String,
        default: null,
      },
    },
    setup(props) {
      const [registerViewPdfModal, { openModal: openViewPdfModal }] = useModal();
      const [register, { openModal }] = useModal();
      const total = ref(0);
      const tableHeight = ref(getTableHeight(document) - 70);
      const loading = ref(false);
      const tableData = ref([]);
      const dimensionDeptTreeId = ref(inject('dimensionDeptTreeId'));
      const organizationId = ref(inject('organizationId'));
      const params = reactive({
        pageSize: 20,
        pageIndex: 0,
        searchText: '',
        draw: 1,
        evaluationCriteriaPlanId: props.planId,
        dimensionDeptTreeId: dimensionDeptTreeId,
      });
      const reportCategory = ref();
      const columns = ref();
      columns.value = getBasicColumns();
      const [registerTable, { setPagination, setLoading }] = useTable({
        columns: columns.value,
        bordered: true,
      });

      watch(
        () => dimensionDeptTreeId.value,
        (newValue, oldValue) => {
          if (oldValue !== newValue) {
            loading.value = true;
            params.pageIndex = 0;
            tableData.value = [];
            total.value = 0;
            getAssignmentPageList();
          }
        },
        { deep: true },
      );

      const getAssignmentPageList = (planId = props.planId) => {
        loading.value = true;
        params.evaluationCriteriaPlanId = planId;
        apiGetEvaluationReportAssignmentPageList(params)
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
      getAssignmentPageList();

      return {
        loading,
        registerTable,
        ...toRefs(params),
        params,
        tableData,
        dimensionDeptTreeId,
        organizationId,
        tableHeight,
        total,
        getAssignmentPageList,
        register,
        openModal,
        setPagination,
        setLoading,
        reportCategory,
        registerViewPdfModal,
        openViewPdfModal,
      };
    },
    methods: {
      onSearch() {
        this.pageIndex = 0;
        this.getAssignmentPageList();
      },
      onChange(pageInfo, _filters) {
        this.pageSize = pageInfo.pageSize;
        this.pageIndex = pageInfo.current - 1;
        this.getAssignmentPageList();
      },
      init() {
        this.pageSize = 20;
        this.pageIndex = 0;
        this.searchText = '';
        this.draw = 1;
        this.total = 0;
        this.tableData = [];
      },
      exportDeptReport() {
        const params = {
          reportCategory: this.reportCategory,
          targetCategory: this.dimensionDeptTreeId ? 'DIMENSION_DEPT_TREE' : 'ORGANIZATION',
          targetId: this.dimensionDeptTreeId ? this.dimensionDeptTreeId : this.organizationId,
          evaluationCriteriaPlanId: this.$props.planId,
        };
        if (!params.targetId) {
          useMessage().createErrorNotification({
            message: '错误',
            description: '未获取导出部门',
          });
          return;
        }
        this.getDimensionDeptTreeReport(params);
      },
      downloadEvaluationAssignmentReport(record) {
        console.log('downloadEvaluationAssignmentReport');
        console.log(record);
        const params = {
          reportCategory: this.reportCategory,
          targetCategory: 'EVALUATION_ASSIGNMENT',
          targetId: record.evaluationAssignmentId,
          evaluationCriteriaPlanId: this.$props.planId,
        };
        this.getEvaluationAssignmentReport(params);
      },
      viewPdf(record) {
        this.openViewPdfModal(true, {
          fileId: record.reportFileId,
          peopleName: record.peopleName,
          evaluationAssignmentId: record.evaluationAssignmentId,
        });
      },
      checkFileUrlList(fileUrl) {
        if (!fileUrl) {
          return false;
        }
        const url = fileUrl.url;
        const a = document.createElement('a');
        a.href = url;
        a.click();
        return true;
      },
      getEvaluationAssignmentReport(params) {
        this.loading = true;
        apiGetEvaluationAssignmentReportReport(params)
          .then((res) => {
            if (res.code === 200) {
              if (res.data) {
                this.getAssignmentPageList(this.planId);
              }
              const pass = this.checkFileUrlList(res.data);
              if (!pass) {
                useMessage().createErrorNotification({
                  message: '错误',
                  description: '未找到报告',
                });
                return;
              }
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
            this.loading = false;
            this.$refs.refViewPdfModal?.closeLoading();
          });
      },
      getDimensionDeptTreeReport(params) {
        this.loading = true;
        apiGetDimensionDeptTreeReport(params)
          .then((res) => {
            if (res.code === 200) {
              const pass = this.checkFileUrlList(res.data);
              if (!pass) {
                useMessage().createSuccessNotification({
                  message: '您的报告正在生成中，请稍后在消息中查看。',
                });
              }
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
            this.loading = false;
          });
      },
      changePlan(planId) {
        this.loading = true;
        this.init();
        this.getAssignmentPageList(planId);
      },
    },
  });
</script>

<style scoped lang="less">
  ::v-deep(.vben-basic-table-header__toolbar) {
    margin-right: 0;
  }

  .view-report-button-style {
    background: #4bc0c0;
    border-color: #4bc0c0;
    margin: 0 5px;
  }

  .view-report-button-style:hover {
    background: #4bc08f;
    border-color: #4bc08f;
  }
</style>
