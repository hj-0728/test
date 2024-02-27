<template>
  <div class="evaluation-report">
    <PageWrapper :content-style="{ height: 'calc(100vh - 168px)' }">
      <template #headerContent>
        <div class="md:flex">
          <div style="width: 100%; padding-bottom: 12px; display: flex; flex: 1">
            <select-period />
            <select-plan
              ref="selectPlan"
              @select-plan-id="selectPlanId"
              @select-plan-callback="selectPlanCallback"
            />
          </div>
        </div>
      </template>
      <div class="content">
        <EvaluationReport ref="refEvaluationReport" />
      </div>
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref, provide } from 'vue';
  import { PageWrapper } from '/@/components/Page';
  import SelectPlan from '/@/components/EvaluationCriteriaPlan/SelectPlan.vue';
  import EvaluationReport from '/@/components/EvaluationReport/Index.vue';
  import { useRoute } from 'vue-router';
  import { apiGetEvaluationCriteriaPlanInfo } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlan';
  import { useMessage } from '/@/hooks/web/useMessage';
  import SelectPeriod from '/@/components/Period/SelectPeriod.vue';

  export default defineComponent({
    components: {
      SelectPeriod,
      PageWrapper,
      SelectPlan,
      EvaluationReport,
    },
    setup() {
      const refEvaluationReport = ref();
      const route = useRoute();
      const evaluationCriteriaPlanId = ref(route.params.id);
      provide('evaluationCriteriaPlanId', evaluationCriteriaPlanId);
      return {
        route,
        refEvaluationReport,
        evaluationCriteriaPlanId,
      };
    },
    mounted() {
      if (this.route.params.id) {
        apiGetEvaluationCriteriaPlanInfo(this.route.params.id)
          .then((res) => {
            if (res.code === 200) {
              this.refEvaluationReport.selectPlan(res.data);
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
          });
      }
    },
    methods: {
      selectPlanId(planId) {
        this.evaluationCriteriaPlanId = planId;
        this.refEvaluationReport.selectPlanId();
      },
      selectPlanCallback(plan) {
        this.$nextTick(() => {
          this.refEvaluationReport?.selectPlan(plan);
        });
      },
    },
  });
</script>

<style scoped lang="less">
  .evaluation-report {
    .content {
      height: 100%;
      //margin-top: 10px;
    }
  }
</style>
