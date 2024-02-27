<template>
  <div class="evaluation-criteria-tree">
    <PageWrapper
      :content-style="{
        height: 'calc(100vh - 80px)',
        margin: '16px 8px 0 8px',
        overflow: 'hidden',
      }"
    >
      <div class="content">
        <Tree
          @on-select-evaluation-criteria-tree-node="onSelectEvaluationCriteriaTreeNode"
          @get-evaluation-criteria="getEvaluationCriteria"
        />
      </div>
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import Tree from '/@/views/evaluationCriteriaTree/Tree.vue';
  import { PageWrapper } from '/@/components/Page';
  import { Row, Col } from 'ant-design-vue';

  import Detail from '/@/views/evaluationCriteriaTree/Detail.vue';
  // import TestTree from "/@/views/evaluationCriteriaTree/TestTree.vue";
  export default defineComponent({
    components: {
      Tree,
      Detail,
      PageWrapper,
      Row,
      Col,
      // TestTree,
    },
    setup() {
      const selectedEvaluationCriteriaTreeNodeId = ref();
      const evaluationCriteriaTreeDetailRef = ref();
      return {
        selectedEvaluationCriteriaTreeNodeId,
        evaluationCriteriaTreeDetailRef,
      };
    },
    methods: {
      getEvaluationCriteria(data) {
        // this.evaluationCriteriaTreeDetailRef.evaluationCriteria = data;
      },
      onSelectEvaluationCriteriaTreeNode(data) {
        // console.log(data);
        // this.selectedEvaluationCriteriaTreeNodeId = data.node.id;
      },
    },
  });
</script>

<style scoped lang="less">
  .evaluation-criteria-tree {
    .content {
      height: 100%;
      background-color: #fff;
    }
  }
</style>
