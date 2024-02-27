<template>
  <div>
    <PageWrapper :content-style="{ height: 'calc(100vh - 144px)' }">
      <template #headerContent>
        <div class="select-period"><SelectPeriod /></div>
      </template>
      <div class="content">
        <BasicTable
          :dataSource="evaluationCriteriaPlanTodoList"
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
            <!--            <template v-if="column.dataIndex === 'planName'">-->
            <!--              <div style="font-size: 16px; font-weight: 600">-->
            <!--                {{ record.planName }}-->
            <!--              </div>-->
            <!--            </template>-->
            <template v-if="column.dataIndex === 'executedStartAt'">
              <div class="plan-executed-at">
                <div class="mt-5">
                  开始：{{ dayjs.utc(record.executedStartAt).local().format('YYYY-MM-DD HH:mm') }}
                </div>
                <div class="mt-5">
                  结束：{{ dayjs.utc(record.executedFinishAt).local().format('YYYY-MM-DD HH:mm') }}
                </div>
              </div>
            </template>
            <!--            <template v-if="column.dataIndex === 'evaluationCriteriaName'">-->
            <!--              <div style="font-size: 16px; font-weight: 500">-->
            <!--                {{ record.evaluationCriteriaName }}-->
            <!--              </div>-->
            <!--            </template>-->
            <template v-if="column.dataIndex === 'planStatusName'">
              <Tag :color="record.planStatus ? colorData[record.planStatus] : ''">
                {{ record.planStatusName }}
              </Tag>
            </template>
            <template v-if="column.dataIndex === 'fillCount'">
              <Tag style="line-height: 24px" color="green">
                {{ record.fillCount }}
              </Tag>
            </template>
            <template v-if="column.dataIndex === 'notFillCount'">
              <Tag style="line-height: 24px" color="pink">
                {{ record.notFillCount }}
              </Tag>
            </template>
            <template v-if="column.dataIndex === 'operation'">
              <Button
                v-if="record.planStatus === 'IN_PROGRESS'"
                type="primary"
                color="edit"
                :iconSize="16"
                title="去评价"
                preIcon="solar:branching-paths-up-broken"
                @click="toEvaluationAssignmentList(record)"
              >
                去评价
              </Button>
              <Button
                v-else
                type="primary"
                color="info"
                :iconSize="16"
                title="去查看"
                preIcon="ant-design:eye-outlined"
                @click="toEvaluationAssignmentList(record)"
              >
                去查看
              </Button>
              <Button
                v-if="record.showReport"
                type="primary"
                color="indigo"
                :iconSize="16"
                title="评价报告"
                preIcon="carbon:report"
                class="ant-btn-left-margin"
                @click="toEvaluationReport(record)"
              >
                评价报告
              </Button>
            </template>
          </template>
        </BasicTable>
      </div>
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { BasicTable, useTable } from '/@/components/Table';
  import { getBasicColumns } from '/@/views/evaluationRecord/tableData';
  import { Input, Tag } from 'ant-design-vue';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { Button } from '/@/components/Button';
  import { apiGetEvaluationCriteriaPlanPageTodoList } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlan';
  import { PageWrapper } from '/@/components/Page';
  import dayjs from 'dayjs';
  import utc from 'dayjs/plugin/utc';
  import { usePeriodStore } from '/@/store/modules/period';
  import SelectPeriod from '/@/components/Period/SelectPeriod.vue';
  import { colorData } from '/@/utils/helper/common';

  export default defineComponent({
    components: {
      SelectPeriod,
      Tag,
      PageWrapper,
      BasicTable,
      InputSearch: Input.Search,
      Button,
    },
    setup() {
      dayjs.extend(utc);
      const store = usePeriodStore();

      const evaluationCriteriaPlanTodoList = ref([]);
      const columns = ref();
      const loading = ref(true);
      const total = ref(0);
      const tableHeight = ref(getTableHeight(document) - 50);
      columns.value = getBasicColumns();
      const [registerTable, { setPagination, setLoading }] = useTable({
        columns: columns.value,
        bordered: true,
      });
      const params = reactive({
        pageSize: 20,
        pageIndex: 0,
        searchText: '',
        draw: 1,
        evaluationObjectCategoryList: [],
        planStatusList: [],
      });

      const setPaginationInfo = () => {
        setPagination({
          current: params.pageIndex + 1,
          total: total.value,
          pageSize: params.pageSize,
        });
      };

      const getEvaluationCriteriaPlanPageTodoList = () => {
        apiGetEvaluationCriteriaPlanPageTodoList(params)
          .then((res) => {
            if (res.code === 200 && params.draw === res.data.draw) {
              total.value = res.data.filterCount;
              evaluationCriteriaPlanTodoList.value = res.data.data;
              params.draw++;
              setPaginationInfo();
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
            setLoading(false);
          });
      };
      getEvaluationCriteriaPlanPageTodoList();

      return {
        evaluationCriteriaPlanTodoList,
        loading,
        total,
        tableHeight,
        params,
        store,
        colorData,
        ...toRefs(params),
        setLoading,
        setPaginationInfo,
        getEvaluationCriteriaPlanPageTodoList,
        dayjs,
        registerTable,
      };
    },
    computed: {
      changePeriod() {
        return this.store.getPeriodId;
      },
    },
    watch: {
      changePeriod(newVal, oldVal) {
        if (newVal !== oldVal && oldVal) {
          this.init();
          this.getEvaluationCriteriaPlanPageTodoList();
        }
      },
    },
    methods: {
      onSearch(value) {
        this.init();
        this.searchText = value;
        this.getEvaluationCriteriaPlanPageTodoList();
      },
      onChange(pageInfo, filters) {
        this.init();
        this.pageSize = pageInfo.pageSize;
        this.pageIndex = pageInfo.current - 1;
        this.evaluationObjectCategoryList = filters.evaluationObjectCategoryName
          ? filters.evaluationObjectCategoryName
          : [];
        this.planStatusList = filters.planStatusName ? filters.planStatusName : [];
        this.getEvaluationCriteriaPlanPageTodoList();
      },
      init() {
        this.setLoading(true);
        this.pageSize = 20;
        this.pageIndex = 0;
        this.searchText = '';
        this.draw = 1;
        this.total = 0;
        this.setPaginationInfo();
      },
      toEvaluationAssignmentList(record) {
        this.$router.push(`/evaluation-assignment/todo-list/${record.evaluationCriteriaPlanId}`);
      },
      toEvaluationReport(record) {
        this.$router.push(
          `/evaluation-record/evaluation-report/overview/${record.evaluationCriteriaPlanId}`,
        );
      },
    },
  });
</script>

<style scoped lang="less">
  .content {
    width: 100%;
    height: 100%;
    background-color: #fff;
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
