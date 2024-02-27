<template>
  <div>
    <PageWrapper :content-style="{ height: 'calc(100vh - 80px)' }">
      <template #headerContent>
        <div class="select-period"><select-period /></div>
      </template>
      <div class="evaluation-criteria-content">
        <EvaluationCriteriaTable />
      </div>
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import { PageWrapper } from '/@/components/Page';
  import EvaluationCriteriaTable from '/@/views/evaluationCriteria/EvaluationCriteriaTable.vue';
  import SelectPeriod from '/@/components/Period/SelectPeriod.vue';

  export default defineComponent({
    components: {
      SelectPeriod,
      PageWrapper,
      EvaluationCriteriaTable,
    },
    setup() {
      return {};
    },
  });
</script>

<style scoped lang="less">
  .evaluation-criteria-content {
    width: 100%;
    height: 100%;
    background-color: #fff;
  }
  .select-period {
    width: 100%;
    display: flex;
    flex: 1;
    justify-content: flex-start;
  }
</style>
