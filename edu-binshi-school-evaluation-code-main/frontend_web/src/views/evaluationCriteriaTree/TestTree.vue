<template>
  111111
  <Tree
    v-model:expandedKeys="expandedKeys"
    v-model:selectedKeys="selectedKeys"
    show-line
    :tree-data="treeData"
  >
    <template #switcherIcon="{ switcherCls }"><down-outlined :class="switcherCls" /></template>
  </Tree>
</template>
<script lang="ts">
import { DownOutlined } from '@ant-design/icons-vue';
import { defineComponent, ref } from 'vue';
import {Tree, TreeProps } from 'ant-design-vue';
export default defineComponent({
  components: {
    DownOutlined,
    Tree,
  },
  setup() {
    const expandedKeys = ref<string[]>(['0-0-0']);
    const selectedKeys = ref<string[]>([]);
    const treeData: TreeProps['treeData'] = [
      {
        title: 'parent 1',
        key: '0-0',
        children: [
          {
            title: 'parent 1-0',
            key: '0-0-0',
            children: [
              {
                title: 'leaf',
                key: '0-0-0-0',
              },
              {
                title: 'leaf',
                key: '0-0-0-1',
              },
              {
                title: 'leaf',
                key: '0-0-0-2',
              },
            ],
          },
          {
            title: 'parent 1-1',
            key: '0-0-1',
            children: [
              {
                title: 'leaf',
                key: '0-0-1-0',
              },
            ],
          },
          {
            title: 'parent 1-2',
            key: '0-0-2',
            children: [
              {
                title: 'leaf',
                key: '0-0-2-0',
              },
              {
                title: 'leaf',
                key: '0-0-2-1',
              },
            ],
          },
        ],
      },
    ];
    return {
      expandedKeys,
      selectedKeys,
      treeData,
    };
  },
});
</script>
