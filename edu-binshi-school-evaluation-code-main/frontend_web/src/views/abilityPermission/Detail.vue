<template>
  <div className="h-full p-4 menu-detail-container">
    <div style="padding-top: 30px">
      <Description
        v-if="onClickPermission && onClickPermission.id !== '#'"
        title="功能权限"
        :column="1"
        :data="onClickPermission"
        :schema="schema"
      />
      <h3 v-else>
        <Icon icon="icon-park-outline:tips-one" />
        <span style="margin-left: 10px">点击功能权限可查看详细信息</span>
      </h3>
    </div>
  </div>
</template>
<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { Description, DescItem } from '/@/components/Description/index';
  import { Icon } from '/@/components/Icon';

  export default defineComponent({
    components: { Description, Icon },
    setup() {
      const onClickPermission = ref(null);
      const schema: DescItem[] = [
        {
          field: 'name',
          label: '名称',
        },
        {
          field: 'code',
          label: '编码',
        },
        {
          field: 'nodeDesc',
          label: '类型',
        },
      ];
      return {
        onClickPermission,
        schema,
      };
    },
    methods: {},
  });
</script>

<style>
  .menu-detail-container {
    margin: 0 1rem;
    background: #ffffff;
    padding: 0 1rem;
    position: relative;
  }
</style>
