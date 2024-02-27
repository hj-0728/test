<template>
  <PageWrapper title="Tree">
    <div style="background: white; padding: 10px">
      <InputSearch v-model:value="params.searchValue" placeholder="搜索" enter-button />
      <BasicTree ref="basicTree" :treeData="treeData" :clickRowToExpand="true" />
    </div>
  </PageWrapper>
</template>
<script lang="ts">
  import { defineComponent, nextTick, reactive, ref, unref } from 'vue';
  import { BasicTree } from '/@/components/Tree/index';
  import { PageWrapper } from '/@/components/Page';
  import { apiGetTemplateTree } from '/@/api/template/template.ts';
  import { InputSearch } from 'ant-design-vue';

  export default defineComponent({
    components: { BasicTree, PageWrapper, InputSearch },

    setup() {
      const params = reactive({
        searchValue: '',
      });
      const treeData = ref([]);
      const basicTree = ref();

      const getTemplateTree = () => {
        apiGetTemplateTree(params)
          .then((res) => {
            if (res.code === 200) {
              treeData.value = res.data;
              nextTick(() => {
                console.log(unref(basicTree));
                unref(basicTree)?.expandAll(true);
              });
            }
          })
          .finally(() => {});
      };
      getTemplateTree();
      return { params, treeData, basicTree };
    },
  });
</script>
<style scoped></style>
