<template>
  <div>
    <PageWrapper>
      <template #headerContent>
        <div class="md:flex">
          <div style="width: 100%; padding-bottom: 12px; display: flex; flex: 1">
            <select-period />
            <select-plan ref="selectPlan" @select-plan-id="selectPlanId" />
          </div>
        </div>
      </template>
      <div class="content">
        <Row :gutter="[16, 0]" style="height: 100%">
          <Col :span="8" style="height: 100%">
            <div style="background-color: #fff; height: 100%">
              <plan-indicator-tree
                ref="refPlanIndicatorTree"
                v-if="evaluationCriteriaPlanId"
                :plan-id="evaluationCriteriaPlanId"
                @on-select-indicator="onSelectIndicator"
              />
              <Empty
                class="empty-info"
                v-if="!loadingTree && !evaluationCriteriaPlanId"
                :image="simpleImage"
              />
            </div>
          </Col>
          <Col :span="16" style="height: 100%">
            <div class="plan-echarts">
              <Loading :loading="loadingEcharts" :absolute="true" />
              <div
                v-if="evaluationCriteriaPlanId && indicatorId && benchmarkList.length > 0"
                style="height: 100%"
              >
                <div>
                  <span class="benchmark-label">评价分类：</span>
                  <RadioGroup v-model:value="benchmark" @change="changeBenchmark">
                    <Radio v-for="item in benchmarkList" :value="item" :key="item.id">
                      <span style="font-weight: bold; font-size: 17px">{{ item.name }}</span>
                    </Radio>
                  </RadioGroup>
                </div>
                <div style="margin-top: 25px; height: calc(100% - 125px)">
                  <Tabs type="card" @change="changeTabs" v-model:activeKey="activeKey">
                    <template v-for="item in planScopeTabs" :key="item.code">
                      <TabPane>
                        <template #tab>
                          <div style="min-width: 160px; text-align: center">
                            <span>{{ item.name }}</span>
                          </div>
                        </template>
                      </TabPane>
                    </template>
                  </Tabs>
                  <div style="height: 100%; overflow-y: auto">
                    <div v-if="activeKey === 'DEPT'" style="margin: 5px 0 20px 0">
                      <span style="font-weight: bold">选择年级：</span>
                      <Select
                        ref="selectGrade"
                        style="width: 40%"
                        v-model:value="gradeDimensionDeptTreeId"
                        :options="gradeDeptList"
                        @change="gradeDeptChange"
                        :fieldNames="{ label: 'name', value: 'dimensionDeptTreeId' }"
                        :maxTagCount="1"
                        :maxTagTextLength="5"
                        placeholder="选择年级"
                        :filter-option="false"
                      />
                    </div>
                    <plan-echarts
                      v-if="evaluationCriteriaPlanId && benchmarkId && activeKey !== 'RANKING'"
                      :plan-id="evaluationCriteriaPlanId"
                      :benchmark="benchmark"
                      :echarts-type="activeKey"
                      :grade-dimension-dept-tree-id="gradeDimensionDeptTreeId"
                      @complete-echarts="completeEcharts"
                      ref="refPlanEcharts"
                    />
                    <div v-if="activeKey === 'RANKING'">
                      <plan-ranking
                        ref="refPlanRanking"
                        @complete-echarts="completeEcharts"
                        v-if="evaluationCriteriaPlanId && benchmark"
                        :plan-id="evaluationCriteriaPlanId"
                        :benchmark="benchmark"
                      />
                    </div>
                  </div>
                </div>
              </div>
              <Empty
                class="empty-info"
                v-if="!loadingEcharts && benchmarkList.length === 0"
                :image="simpleImage"
              />
            </div>
          </Col>
        </Row>
      </div>
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { PageWrapper } from '/@/components/Page';
  import { Row, Col, Select, Radio, Tabs, Empty } from 'ant-design-vue';
  import PlanIndicatorTree from '/src/views/statistics/components/PlanIndicatorTree.vue';
  import PlanEcharts from '/@/views/statistics/components/PlanEcharts.vue';
  import {
    apiGetPlanDeptGradeScope,
    apiGetPlanIndicatorBenchmark,
  } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlanStatistics';
  import { useMessage } from '/@/hooks/web/useMessage';
  import SelectPlan from '/@/components/EvaluationCriteriaPlan/SelectPlan.vue';
  import SelectPeriod from '/@/components/Period/SelectPeriod.vue';
  import PlanRanking from '/@/views/statistics/components/PlanRanking.vue';
  import { Loading } from '/@/components/Loading';

  export default defineComponent({
    components: {
      Loading,
      Select,
      PageWrapper,
      Row,
      Col,
      PlanIndicatorTree,
      PlanEcharts,
      RadioGroup: Radio.Group,
      Radio,
      Tabs,
      TabPane: Tabs.TabPane,
      SelectPlan,
      SelectPeriod,
      PlanRanking,
      Empty,
    },
    setup() {
      const loadingTree = ref(true);
      const loadingEcharts = ref(true);
      const evaluationCriteriaPlanId = ref<String | null>(null);
      const indicatorId = ref<String | null>(null);
      const benchmarkList = ref<object[]>([]);
      const benchmarkId = ref<String | null>(null);
      const benchmark = ref<object | null>(null);
      const gradeDimensionDeptTreeId = ref<String | null>(null);
      const gradeDeptList = ref<object[]>([]);
      const activeKey = ref('');
      const planScopeTabs = ref<object[]>([]);
      return {
        evaluationCriteriaPlanId,
        indicatorId,
        benchmarkList,
        benchmarkId,
        planScopeTabs,
        gradeDimensionDeptTreeId,
        gradeDeptList,
        activeKey,
        benchmark,
        simpleImage: Empty.PRESENTED_IMAGE_SIMPLE,
        loadingTree,
        loadingEcharts,
      };
    },
    mounted() {},
    methods: {
      init() {
        this.evaluationCriteriaPlanId = null;
        this.indicatorId = null;
        this.benchmarkList = [];
        this.benchmarkId = null;
        this.benchmark = null;
        this.gradeDimensionDeptTreeId = null;
        this.gradeDeptList = [];
        this.activeKey = '';
        this.planScopeTabs = [];
        this.loadingTree = true;
        this.loadingEcharts = true;
      },
      selectPlanId(data) {
        this.init();
        console.log(data);
        console.log('selectPlanId=========');
        if (!data) {
          this.evaluationCriteriaPlanId = data;
          this.loadingTree = false;
          this.loadingEcharts = false;
        }
        if (this.evaluationCriteriaPlanId !== data) {
          this.evaluationCriteriaPlanId = data;
          this.$refs.refPlanIndicatorTree?.getIndicatorTree(data);
          this.getPlanGradeScope();
        }
      },
      getPlanIndicatorBenchmark() {
        this.loadingEcharts = true;
        apiGetPlanIndicatorBenchmark(this.evaluationCriteriaPlanId, this.indicatorId)
          .then((res) => {
            if (res.code === 200) {
              console.log(res);
              this.benchmarkList = res.data;
              if (this.benchmarkList.length > 0) {
                this.benchmarkId = this.benchmarkList[0].id;
                this.benchmark = this.benchmarkList[0];
                console.log(this.$refs.refPlanEcharts);
                this.changeStatistics();
              } else {
                this.loadingEcharts = false;
              }
              console.log(this.benchmarkId);
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch((error) => {
            console.log(error);
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络错误1',
            });
          })
          .finally(() => {});
      },
      getPlanGradeScope() {
        apiGetPlanDeptGradeScope(this.evaluationCriteriaPlanId)
          .then((res) => {
            console.log(res);
            if (res.code === 200) {
              if (res.data.length > 0) {
                this.planScopeTabs = [
                  { name: '班级对比', code: 'DEPT' },
                  { name: '排行', code: 'RANKING' },
                ];
                this.gradeDeptList = res.data;
                this.gradeDimensionDeptTreeId = this.gradeDeptList[0].dimensionDeptTreeId;
                this.activeKey = 'DEPT';
              } else {
                this.planScopeTabs = [
                  { name: '学生统计', code: 'STUDENT' },
                  { name: '排行', code: 'RANKING' },
                ];
                this.activeKey = 'STUDENT';
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
          .finally(() => {});
      },
      onSelectIndicator(data) {
        console.log(data);
        this.indicatorId = data.indicatorId;
        this.loadingTree = false;
        if (!this.indicatorId) {
          this.loadingEcharts = false;
        } else {
          this.loadingEcharts = true;
          this.getPlanIndicatorBenchmark();
        }
        console.log('onSelectIndicator');
      },
      changeBenchmark(data) {
        console.log(data);
        console.log(this.benchmark);
        this.benchmarkId = this.benchmark.id;
        console.log(this.benchmarkId);
        console.log('changeBenchmark');
        this.changeStatistics();
      },
      changeTabs(tabsCode) {
        console.log(tabsCode);
        console.log('changeTabs');
        if (tabsCode === 'DEPT') {
          console.log('班级对比');
        } else if (tabsCode === 'STUDENT') {
          console.log('学生对比');
        } else if (tabsCode === 'RANKING') {
          console.log('排行');
        }
      },
      gradeDeptChange() {
        console.log('gradeDeptChange');
        console.log('更新echarts');
        this.$refs.refPlanEcharts?.updateChart(
          this.evaluationCriteriaPlanId,
          this.benchmark,
          this.gradeDimensionDeptTreeId,
        );
      },
      changeStatistics() {
        this.$refs.refPlanEcharts?.updateChart(
          this.evaluationCriteriaPlanId,
          this.benchmark,
          this.gradeDimensionDeptTreeId,
        );
        this.$refs.refPlanRanking?.init(this.evaluationCriteriaPlanId, this.benchmark.id);
      },
      completeEcharts() {
        this.loadingEcharts = false;
      },
    },
  });
</script>

<style lang="less" scoped>
  .content {
    //background-color: #fff;
    height: calc(100vh - 168px);
    //margin-top: 10px;
  }

  .plan-echarts {
    height: 100%;
    width: 100%;
    background-color: #fff;
    padding: 10px 20px;
  }

  .benchmark-label {
    padding: 0 20px 10px 0;
    font-weight: bold;
    font-size: 18px;
  }

  .empty-info {
    margin: 0 !important;
    padding: 32px 0;
  }
</style>
