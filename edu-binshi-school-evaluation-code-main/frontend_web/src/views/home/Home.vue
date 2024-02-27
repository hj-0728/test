<template>
  <div>
    <PageWrapper>
      <template #headerContent>
        <div class="select-period"><select-period /></div>
      </template>
      <div class="content">
        <Row :gutter="[16, 0]" style="height: 100%">
          <Col :span="13" style="height: 100%">
            <div class="list-title">
              <Row>
                <Col :span="12">评价计划进展</Col>
                <Col :span="12">
                  <div class="count-right">
                    <span style="color: #389e0d; padding-right: 30px">
                      进行中：{{ planInProgressCount }}
                    </span>
                    <span style="color: #096dd9">待开始：{{ planToBeStartedCount }}</span>
                  </div>
                </Col>
              </Row>
            </div>
            <div class="plan-list">
              <plan-progress-list
                :is-in-progress="true"
                ref="planInProgressList"
                @set-plan-count="setPlanCount"
              />
            </div>
            <div class="plan-list-wait">
              <plan-progress-list
                :is-in-progress="false"
                ref="planNotInProgressList"
                @set-plan-count="setPlanCount"
              />
            </div>
          </Col>
          <Col :span="11" style="height: 100%">
            <div class="list-title">
              <Row>
                <Col :span="12">
                  待办事项
                  <span style="color: red; font-size: 14px">
                    （点击<Icon style="margin: 0 4px" icon="todo|svg" :size="14" />完成待办事项）
                  </span>
                </Col>
                <Col :span="12">
                  <div class="count-right">
                    <span style="color: red">{{ todoCount }}</span>
                    /
                    <span style="color: #389e0d">{{ todoCompletedCount }}</span>
                  </div>
                </Col>
              </Row>
            </div>
            <div class="todo-list">
              <todo-task-list
                ref="refTodoTaskUndone"
                :is-completed="false"
                @set-todo-count="setTodoCount"
                @todo-task-completed="initHome"
              />
            </div>
            <div class="todo-c-list">
              <todo-task-list
                ref="refTodoTaskCompleted"
                :is-completed="true"
                @set-todo-count="setTodoCount"
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
  import { Row, Col } from 'ant-design-vue';
  import PlanProgressList from '/@/views/home/components/PlanProgressList.vue';
  import TodoTaskList from '/@/views/home/components/TodoTaskList.vue';
  import headerImg from '/@/assets/images/header.jpg';
  import { useUserStore } from '/@/store/modules/user';
  import { Icon } from '/@/components/Icon';
  import SelectPeriod from '/@/components/Period/SelectPeriod.vue';
  import { usePeriodStore } from '/@/store/modules/period';

  export default defineComponent({
    components: {
      Icon,
      PageWrapper,
      Row,
      Col,
      PlanProgressList,
      TodoTaskList,
      SelectPeriod,
    },
    setup() {
      const loading = ref(false);
      const planLoading = ref(false);
      const todoLoading = ref(false);

      const planCount = ref(0);
      const todoCount = ref(0);
      const todoCompletedCount = ref(0);
      const planInProgressCount = ref(0);
      const planToBeStartedCount = ref(0);

      const userStore = useUserStore();
      const { name } = userStore.getUserInfo;
      // console.log(userInfo);
      return {
        loading,
        planLoading,
        todoLoading,
        headerImg,
        name,
        planCount,
        todoCount,
        todoCompletedCount,
        planInProgressCount,
        planToBeStartedCount,
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
          this.initHome();
        }
      },
    },
    mounted() {
      this.loading = false;
    },
    methods: {
      setPlanCount(data) {
        if (data.isInProgress) {
          this.planInProgressCount = data.count;
        } else {
          this.planToBeStartedCount = data.count;
        }
      },
      setTodoCount(data) {
        if (data.isCompleted) {
          this.todoCompletedCount = data.count;
        } else {
          this.todoCount = data.count;
        }
      },
      initHome() {
        this.$refs.planInProgressList.init();
        this.$refs.planNotInProgressList.init();
        this.$refs.refTodoTaskUndone.init();
        this.$refs.refTodoTaskCompleted.init();
      },
    },
  });
</script>

<style lang="less" scoped>
  .content {
    //background-color: #fff;
    height: calc(100vh - 144px);
    //margin-top: 10px;
  }

  .plan-list {
    height: calc(58% - 46px);
    width: 100%;
    background-color: #fff;
    padding: 10px;
    overflow-y: auto;
  }

  .plan-list-wait {
    height: 42%;
    width: 100%;
    background-color: #fff;
    padding: 10px;
    overflow-y: auto;
    margin-top: 10px;
  }

  .todo-list {
    height: calc(58% - 46px);
    width: 100%;
    background-color: #fff;
    padding: 10px;
    overflow-y: auto;
  }

  .todo-c-list {
    height: 42%;
    width: 100%;
    background-color: #fff;
    padding: 10px;
    overflow-y: auto;
    margin-top: 10px;
  }

  .list-title {
    width: 100%;
    background-color: #fff;
    padding: 10px 24px;
    color: #000000d9;
    font-weight: 500;
    font-size: 16px;
    border-bottom: 1px solid #f0f0f0;
  }

  .count-right {
    text-align: right;
    font-weight: bold;
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
