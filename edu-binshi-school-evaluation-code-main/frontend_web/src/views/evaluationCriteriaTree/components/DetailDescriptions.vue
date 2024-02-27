<template>
  <Descriptions bordered>
    <DescriptionsItem label="描述">{{ evaluationCriteriaTree.comments }}</DescriptionsItem>
  </Descriptions>
</template>

<script>
  import { Descriptions } from 'ant-design-vue';

  export default {
    name: 'DetailDescriptions',
    components: {
      Descriptions,
      DescriptionsItem: Descriptions.Item,
    },
    props: {
      evaluationCriteriaTree:{
        type: Object,
      },
    },
    setup() {},
  };
</script>

<style scoped></style>
