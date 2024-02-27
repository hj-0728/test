<template>
  <div class="h-full p-4 menu-detail-container">
    <div style="padding-top: 30px">
      <Description
        v-if="onClickMenu && onClickMenu.id !== '#'"
        title="菜单信息"
        :column="1"
        :data="onClickMenu"
        :schema="schema"
      />
      <h3 v-else>
        <Icon icon="icon-park-outline:tips-one" />
        <span style="margin-left: 10px">点击菜单可查看详细信息</span>
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
      const onClickMenu = ref(null);
      const schema: DescItem[] = [
        {
          field: 'name',
          label: '名称',
        },
        {
          field: 'path',
          label: '路径',
        },
        {
          field: 'icon',
          label: 'icon',
        },
        {
          field: 'permissionName',
          label: '功能权限',
        },
      ];
      return {
        onClickMenu,
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
