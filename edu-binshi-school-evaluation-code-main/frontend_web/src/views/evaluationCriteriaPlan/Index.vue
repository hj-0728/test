<template>
  <div>
    <PageWrapper :content-style="{ height: 'calc(100vh - 144px)' }">
      <template #headerContent>
        <div class="select-period"><SelectPeriod /></div>
      </template>
      <div style="height: 100%; background: white">
        <BasicTable
          :dataSource="tableData"
          :canResize="true"
          :loading="loading"
          :scroll="{ x: 0 | false, y: tableHeight }"
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
              style="padding: 10px 0 10px 0; width: 30%"
            />
          </template>
          <template #toolbar>
            <Button
              type="primary"
              color="success"
              :iconSize="18"
              preIcon="ant-design:plus-outlined"
              class="ant-btn-left-margin"
              title="添加"
              @click="addEvaluationCriteriaPlan"
              >添加
            </Button>
          </template>
          <template #bodyCell="{ column, record }">
            <template v-if="column.dataIndex === 'executedAt'">
              <div class="plan-executed-at">
                <div class="mt-5">开始：{{ record.executedStartAt }}</div>
                <div class="mt-5">结束：{{ record.executedFinishAt }}</div>
              </div>
            </template>
            <template v-if="column.dataIndex === 'statusName'">
              <Tag :color="record.status ? colorData[record.status] : ''">
                {{ record.statusName }}
              </Tag>
            </template>
            <template v-if="column.dataIndex === 'operation'">
              <Button
                type="primary"
                color="info"
                :iconSize="16"
                title="查看"
                preIcon="ant-design:eye-outlined"
                @click="checkEvaluationCriteriaPlan(record)"
                v-if="!record.canEdit"
              >
                查看
              </Button>
              <Button
                type="primary"
                color="edit"
                :iconSize="16"
                title="编辑"
                preIcon="ant-design:edit-twotone"
                @click="editEvaluationCriteriaPlan(record)"
                v-if="record.canEdit"
              >
                编辑
              </Button>
              <Button
                type="danger"
                color="error"
                class="ant-btn-left-margin"
                :iconSize="16"
                title="作废"
                preIcon="fe:disabled"
                @click="abolishEvaluationCriteriaPlan(record)"
                v-if="record.status === 'PUBLISHED' || record.status === 'DRAFT'"
              >
                作废
              </Button>
              <Button
                type="primary"
                :iconSize="16"
                preIcon="ant-design:setting-filled"
                style="margin-left: 10px"
                @click="toPlanScope(record)"
              >
                适用范围
              </Button>
            </template>
          </template>
        </BasicTable>
      </div>
      <EditEvaluationCriteriaModal
        @register="registerEditEvaluationCriteriaModal"
        @save-success="saveSuccess"
      />
      <PlanScopeModal @register="register" @save-success="saveSuccess" />
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { getBasicColumns } from './evaluationPlanTableData';
  import { PageWrapper } from '/@/components/Page';
  import { BasicTable, useTable } from '/@/components/Table';
  import { Input, Tag } from 'ant-design-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { Button } from '/@/components/Button';
  import { useModal } from '/@/components/Modal';
  import EditEvaluationCriteriaModal from '/@/views/evaluationCriteriaPlan/EditEvaluationCriteriaPlanModal.vue';
  import PlanScopeModal from '/@/views/evaluationCriteriaPlan/components/PlanScopeModal.vue';
  import dayjs from 'dayjs';
  import utc from 'dayjs/plugin/utc';
  import {
    apiGetEvaluationPlanList,
    apiAbolishStatus,
  } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlan';
  import { evaluationCriteriaPlanStatusEnum } from '/@/enums/bizEnum';
  import { colorData } from '/@/utils/helper/common';
  import SelectPeriod from '/@/components/Period/SelectPeriod.vue';
  import { usePeriodStore } from '/@/store/modules/period';

  export default defineComponent({
    components: {
      SelectPeriod,
      Tag,
      Button,
      PageWrapper,
      BasicTable,
      InputSearch: Input.Search,
      EditEvaluationCriteriaModal,
      PlanScopeModal,
    },
    emits: ['register'],
    setup() {
      dayjs.extend(utc);
      const [registerEditEvaluationCriteriaModal, { openModal: openEditEvaluationCriteriaModal }] =
        useModal();
      const total = ref(0);
      const loading = ref(false);
      const tableData = ref([]);
      const [register, { openModal }] = useModal();
      const [registerGroupModal, { openModal: openGroupModal }] = useModal();
      const tableHeight = ref<Number>(getTableHeight(document) - 60);
      const [registerTable, { setPagination, setLoading }] = useTable({
        columns: getBasicColumns(),
        bordered: true,
      });
      const setPaginationInfo = () => {
        setPagination({
          total: total.value,
          pageSize: params.pageSize,
          current: params.pageIndex + 1,
        });
      };
      const params = reactive({
        searchText: '', //搜索框中的内容
        pageSize: 20, //页面显示条数
        pageIndex: 0, //当前显示的第几页
        draw: 1, //默认显示第一页
        statusList: [], //状态筛选列表
        isCurrentPeriod: true,
      });

      const toPlanScope = (record) => {
        openModal(true, {
          plan_id: record.id,
          disabled: !record.canEdit,
          required: record.status === evaluationCriteriaPlanStatusEnum.PUBLISHED, //发布状态时必须选择范围
        });
      };
      return {
        loading,
        total,
        params,
        register,
        tableData,
        tableHeight,
        colorData,
        registerTable,
        setLoading,
        setPaginationInfo,
        ...toRefs(params),
        openModal,
        registerEditEvaluationCriteriaModal,
        openEditEvaluationCriteriaModal,
        toPlanScope,
        registerGroupModal,
        openGroupModal,
      };
    },
    computed: {
      periodId() {
        return usePeriodStore().getPeriodId;
      },
    },
    watch: {
      periodId(newVal, oldVal) {
        if (newVal !== oldVal && oldVal) {
          this.onSearch();
        }
      },
    },
    mounted() {
      this.getEvaluationPlanList();
    },
    methods: {
      onSearch() {
        this.init();
        this.pageIndex = 0;
        this.getEvaluationPlanList();
      },
      init() {
        this.setLoading(true);
        this.draw = 1;
        this.total = 0;
      },
      onChange(pageInfo, filters) {
        this.pageSize = pageInfo.pageSize;
        this.pageIndex = pageInfo.current - 1;
        this.params.statusList = filters.statusName ? filters.statusName : [];
        this.getEvaluationPlanList();
      },
      getEvaluationPlanList() {
        this.loading = true;
        apiGetEvaluationPlanList(this.params)
          .then((res) => {
            if (res.code === 200) {
              this.total = res.data.filterCount;
              this.tableData = res.data.data;
              this.tableData.forEach((item) => {
                item.executedFinishAt = dayjs
                  .utc(item.executedFinishAt)
                  .local()
                  .format('YYYY-MM-DD HH:00');
                item.executedStartAt = dayjs
                  .utc(item.executedStartAt)
                  .local()
                  .format('YYYY-MM-DD HH:00');
                // 草稿状态或者发布状态还没结束的计划可以编辑
                item.canEdit =
                  item.status === evaluationCriteriaPlanStatusEnum.DRAFT ||
                  (item.executedFinishAt > dayjs().local().format('YYYY-MM-DD HH:mm') &&
                    item.status === evaluationCriteriaPlanStatusEnum.PUBLISHED);
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
            this.loading = false;
          });
      },
      saveSuccess() {
        this.getEvaluationPlanList();
      },
      editEvaluationCriteriaPlan(data) {
        this.openEditEvaluationCriteriaModal(true, {
          modalCategory: 'EDIT',
          evaluationCriteriaPlan: data,
          required: data.status === evaluationCriteriaPlanStatusEnum.PUBLISHED, //发布状态时必须选择范围
        });
      },
      addEvaluationCriteriaPlan() {
        this.openEditEvaluationCriteriaModal(true, {
          modalCategory: 'ADD',
        });
      },
      checkEvaluationCriteriaPlan(data) {
        this.openEditEvaluationCriteriaModal(true, {
          modalCategory: 'CHECK',
          evaluationCriteriaPlan: data,
        });
      },
      abolishEvaluationCriteriaPlan(plan) {
        let title = '点击确定会将该条计划作废，是否确认作废？';
        let result = {
          id: plan.id,
          version: plan.version,
          evaluationCriteriaId: plan.evaluationCriteriaId,
          focusPeriodId: plan.focusPeriodId,
          name: plan.name,
          executedStartAt: plan.executedStartAt,
          executedFinishAt: plan.executedFinishAt,
          status: 'ABOLISHED',
          statusName: '已作废',
        };
        useMessage().createConfirm({
          iconType: 'info',
          title: () => title,
          centered: true,
          onOk: () => {
            this.setLoading(true);
            apiAbolishStatus(result)
              .then((res) => {
                if (res.code === 200) {
                  useMessage().createSuccessNotification({
                    message: '成功',
                    description: '操作成功',
                  });
                  this.getEvaluationPlanList();
                } else {
                  useMessage().createErrorNotification({
                    message: '操作失败',
                    description: res.error.message,
                  });
                  this.setLoading(false);
                }
              })
              .catch(() => {
                useMessage().createErrorNotification({
                  message: '保存失败',
                  description: '网络错误',
                });
                this.setLoading(false);
              });
          },
        });
      },
    },
  });
</script>

<style lang="less" scoped>
  ::v-deep(.zebra-highlight) {
    background: #fafafa;
  }

  .void-button-style {
    margin-left: 5px;
  }

  .delete-button-style {
    margin-left: 5px;
  }

  .plan-executed-at {
    word-break: normal;
    width: auto;
    display: block;
    white-space: pre-wrap;
    word-wrap: break-word;
    overflow: hidden;
  }

  .mt-5 {
    margin-top: 5px;
  }

  .select-period {
    width: 100%;
    display: flex;
    flex: 1;
    justify-content: flex-start;
  }

  ::v-deep(.ant-page-header-content) {
    padding-top: 0 !important;
  }
</style>
