<template>
  <div class="content">
    <Row :gutter="[16, 0]" style="height: 100%">
      <Col :span="6" style="height: 100%">
        <div style="background-color: #fff; height: calc(100% + 16px)">
          <ScopeTree
            ref="refScopeTree"
            v-if="evaluationCriteriaPlanId"
            :plan-id="evaluationCriteriaPlanId"
            @on-select-tree="onSelectTree"
          />
          <Empty class="empty-info" v-else :image="simpleImage" />
        </div>
      </Col>
      <Col :span="18">
        <div style="height: 100%; width: 100%; background-color: #fff">
          <EvaluationAssignmentTable
            ref="refEvaluationAssignmentTable"
            v-if="evaluationCriteriaPlanId"
            :plan-id="evaluationCriteriaPlanId"
          />
          <Empty class="empty-info" v-else :image="simpleImage" />
        </div>
      </Col>
    </Row>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref, provide, inject } from 'vue';
  import ScopeTree from '/@/components/EvaluationReport/ScopeTree.vue';
  import EvaluationAssignmentTable from '/@/components/EvaluationReport/EvaluationAssignmentTable.vue';
  import { Col, Empty, Row } from 'ant-design-vue';

  export default defineComponent({
    components: {
      Empty,
      Col,
      Row,
      ScopeTree,
      EvaluationAssignmentTable,
    },
    setup() {
      const dimensionDeptTreeId = ref(null);
      const organizationId = ref(null);
      const deptName = ref();
      provide('dimensionDeptTreeId', dimensionDeptTreeId);
      provide('organizationId', organizationId);
      provide('deptName', deptName);
      const refScopeTree = ref();
      const refEvaluationAssignmentTable = ref();
      const evaluationCriteriaPlanId = inject('evaluationCriteriaPlanId');
      return {
        dimensionDeptTreeId,
        organizationId,
        deptName,
        refScopeTree,
        evaluationCriteriaPlanId,
        refEvaluationAssignmentTable,
        simpleImage: Empty.PRESENTED_IMAGE_SIMPLE,
      };
    },
    methods: {
      onSelectTree(node) {
        this.deptName = node.name;
        if (node.deptId) {
          this.dimensionDeptTreeId = node.id;
          this.organizationId = null;
        } else {
          this.dimensionDeptTreeId = null;
          this.organizationId = node.id;
        }
      },
      selectPlanId() {
        if (!this.evaluationCriteriaPlanId) {
          return;
        }
        if (this.refScopeTree) {
          this.refScopeTree.searchValue = '';
          this.refScopeTree.selectedKeys = [];
          this.refScopeTree.getEvaluationReportDeptTree(this.evaluationCriteriaPlanId);
        }

        if (this.refEvaluationAssignmentTable) {
          this.refEvaluationAssignmentTable.searchText = '';
          this.refEvaluationAssignmentTable.dimensionDeptTreeId = null;
          this.refEvaluationAssignmentTable.changePlan(this.evaluationCriteriaPlanId);
        }
      },
      selectPlan(plan) {
        if (!plan) {
          return;
        }
        this.refEvaluationAssignmentTable.reportCategory = plan.reportCategory;
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

    .empty-info {
      margin: 0 !important;
      padding: 32px 0;
    }
  }
</style>
