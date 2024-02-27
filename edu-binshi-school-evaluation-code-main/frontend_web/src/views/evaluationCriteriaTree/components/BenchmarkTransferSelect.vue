<template>
  <Transfer
    v-model:target-keys="targetKeys"
    class="tree-transfer"
    :data-source="dataSource"
    :show-select-all="false"
    :one-way="true"
    :rowKey="(record) => record.value"
    @change="handleSelectChange"
  >
    <template #children="{ direction }">
      <Tree
        v-if="direction === 'left'"
        block-node
        check-strictly
        default-expand-all
        :fieldNames="{ title: 'name', key: 'value' }"
        :tree-data="treeData"

        @select="handleNodeSelect"
      >
        <template #title="node">
          <span v-if="node?.children?.length > 0">{{ node.name }}</span>
          <Radio v-else :checked="targetKeys.includes(node.value)" :value="node.value">{{
            node.name
          }}</Radio>
        </template>
      </Tree>
    </template>

    <template #render="item">
      <Row justify="space-between" style="align-items: center">
        <Col span="8">{{ item.name }} </Col>
        <Col span="8"
          ><InputNumber
            v-model:value="item.weight"
            min="1"
            :precision="0"
            @click.stop
            placeholder="请输入权重"
        /></Col>
      </Row>
    </template>
  </Transfer>
</template>

<script lang="ts">
  import { Row, Col, InputNumber, Transfer, Tree, Radio } from 'ant-design-vue';
  import type { TransferProps } from 'ant-design-vue';
  import { computed, ref } from 'vue';
  export default {
    name: 'BenchmarkTransferSelect',
    components: {
      Radio,
      Transfer,
      Tree,
      Row,
      Col,
      InputNumber,
    },
    props: {
      benchmarkTree: {
        type: Array,
        default: [],
      },
    },
    setup(props) {
      const tData: TransferProps['dataSource'] = [
        {
          value: 'A',
          name: '0-0',
          level: 1,
          children: [{ value: 'H', name: '0-0-0', level: 2, parentId: 'A' }],
        },
        {
          value: 'B',
          name: '0-1',
          level: 1,
          children: [
            { value: 'C', name: '0-1-0', level: 2, parentId: 'B' },
            { value: 'D', name: '0-1-1', level: 2, parentId: 'B' },
          ],
        },
        {
          value: 'E',
          name: '0-3',
          level: 1,
          children: [
            { value: 'F', name: '0-3-0', level: 2, parentId: 'E' },
            { value: 'G', name: '0-3-1', level: 2, parentId: 'E' },
          ],
        },
      ];
      const transferDataSource: TransferProps['dataSource'] = [];
      const targetKeys = ref<string[]>([]);

      const dataSource = ref(transferDataSource);

      const treeData = computed(() => {
        // return handleTreeData(props.benchmarkTree, targetKeys.value);
        return handleTreeData(tData, targetKeys.value);
      });
      const flatten = (list: TransferProps['dataSource'] = []) => {
        list.forEach((item) => {
          transferDataSource.push(item);
          flatten(item.children);
        });
      };
      flatten(JSON.parse(JSON.stringify(tData)));
      // flatten(JSON.parse(JSON.stringify(props.benchmarkTree)));
      const handleTreeData = (
        treeNodes: TransferProps['dataSource'],
        targetKeys: string[] = [],
      ) => {
        return treeNodes.map(({ children, ...props }) => ({
          ...props,
          disabled: targetKeys.includes(props.value as string),
          children: handleTreeData(children ?? [], targetKeys),
        }));
      };
      const selectedKeys = ref({});
      const selectedChildrenMap = ref({});
      return {
        transferDataSource,
        targetKeys,
        dataSource,
        treeData,
        selectedKeys,
        selectedChildrenMap,
      };
    },
    computed: {
      targetKeys() {
        return Object.values(this.selectedChildrenMap);
      },
    },
    methods: {
      handleNodeSelect(_, { selectedNodes }) {
        const selectedNode = selectedNodes[0];
        if (selectedNode && selectedNode.level === 2) {
          console.log(selectedNode);
          this.selectedChildrenMap[selectedNode.parentId] = selectedNode.value;
        }
      },
      handleSelectChange(targetKeys,direction,moveKeys) {
        for (const [parentKey, selectedChildKey] of Object.entries(this.selectedChildrenMap)) {
          if (moveKeys.includes(selectedChildKey)) {
            delete this.selectedChildrenMap[parentKey];
            return;
          }
        }
      },
    },
  };
</script>

<style scoped></style>
