<template>
  <FormItem
    :name="formItem.formName"
    :label="formItem.title"
    :rules="{
      required: required,
      trigger: ['blur'],
      validator: validateFormItem,
    }"
  >
    <Transfer
      v-model:target-keys="targetKeys"
      class="tree-transfer"
      :data-source="dataSource"
      :show-select-all="false"
      :one-way="true"
      :disabled="readonly"
      @change="handleNodeSelect"
      :rowKey="(record) => record.value"
      :selectAllLabels="selectAllLabels"
    >
      <template #children="{ direction }">
        <Tree
          class="transfer-tree"
          v-if="direction === 'left'"
          check-strictly
          checkable
          default-expand-all
          :field-names="{ key: 'value', title: 'name' }"
          :checked-keys="[...targetKeys]"
          :tree-data="treeData"
          :disabled="readonly"
          @select="handleNodeSelect"
          @check="handleNodeSelect"
        >
          <!--          <template #title="node">-->
          <!--            <span v-if="node?.children?.length > 0">{{ node.name }}</span>-->
          <!--            <CheckBox v-else :checked="targetKeys?.includes(node.value)" :value="node.value">{{-->
          <!--              node.name-->
          <!--            }}</CheckBox>-->
          <!--          </template>-->
        </Tree>
      </template>

      <template #render="item">
        <Row justify="space-between" style="align-items: center">
          <Col span="10">{{ item.name }} </Col>
          <Col span="10"
            ><InputNumber
              @change="changeWeight"
              v-model:value="item.weight"
              min="1"
              style="width: 100%"
              :precision="0"
              @click.stop
              :readonly="readonly"
              placeholder="请输入权重"
          /></Col>
        </Row>
      </template>
    </Transfer>
  </FormItem>
</template>

<script lang="ts">
  import { Col, Form, InputNumber, Row, Transfer, TransferProps, Tree } from 'ant-design-vue';
  import { computed, reactive, ref } from 'vue';
  import { SelectAllLabel } from 'ant-design-vue/es/transfer';

  export default {
    name: 'TreeSelectFormItem',
    components: {
      Transfer,
      Tree,
      Row,
      Col,
      InputNumber,
      FormItem: Form.Item,
    },
    props: {
      formItem: {
        type: Object,
      },
      required: {
        type: Boolean,
        default: true,
      },
      readonly: {
        type: Boolean,
        default: false,
      },
    },
    setup(props) {
      const dataSource = ref([]);
      const targetKeys = ref<string[]>([]);

      const params = reactive({
        [props.formItem.formName]: [],
      });
      const treeData = computed(() => {
        // return handleTreeData(props.benchmarkTree, targetKeys.value);
        return handleTreeData(props.formItem.items, targetKeys.value);
      });
      const flatten = (list: TransferProps['dataSource'] = []) => {
        list.forEach((item) => {
          dataSource.value.push(item);
          flatten(item.children);
        });
      };
      flatten(JSON.parse(JSON.stringify(props.formItem.items)));
      // flatten(JSON.parse(JSON.stringify(props.benchmarkTree)));
      const handleTreeData = (
        treeNodes: TransferProps['dataSource'],
        targetKeys: string[] = [],
      ) => {
        return treeNodes.map(({ children, ...props }) => ({
          ...props,
          // disabled: targetKeys.includes(props.value as string),
          children: handleTreeData(children ?? [], targetKeys),
        }));
      };
      const selectedKeys = ref({});
      const selectedChildrenMap = ref({});
      const validateFormItem = async (_rule) => {
        console.log(selectedChildrenMap.value);
        if (params[props.formItem.formName].some((obj) => !obj.weight)) {
          return Promise.reject('请输入权重');
        }
        if (params[props.formItem.formName].length < 2) {
          return Promise.reject('请选择至少两个' + props.formItem.title);
        }
        return Promise.resolve();
      };

      const indicatorCount = computed(() => {
        // return handleTreeData(props.benchmarkTree, targetKeys.value);
        return getIndicatorCount(props.formItem.items);
      });

      const getIndicatorCount = (tree) => {
        let c = 0;
        tree.forEach((value) => {
          if (!value.checkable) {
            c++;
          }
          if (value.children && value.children.length > 0) {
            c += getIndicatorCount(value.children);
          }
        });
        return c;
      };

      const selectAllLabels: SelectAllLabel[] = [
        ({ totalCount }) => `${totalCount - indicatorCount.value} 项`,
      ];

      return {
        params,
        validateFormItem,
        dataSource,
        treeData,
        selectedKeys,
        selectedChildrenMap,
        targetKeys,
        selectAllLabels,
      };
    },
    computed: {
      // targetKeys() {
      //   return Object.values(this.selectedChildrenMap);
      // },
    },
    methods: {
      setParams(benchmarkStrategyParams) {
        this.targetKeys = [];
        this.selectedChildrenMap = {};
        this.params[this.formItem.formName] = benchmarkStrategyParams[this.formItem.formName];
        this.params[this.formItem.formName].forEach((paramItem) => {
          this.targetKeys.push(paramItem.sourceBenchmarkId);
          const dataSourceItem = this.dataSource.find(
            (item) => item.value === paramItem.sourceBenchmarkId,
          );
          if (dataSourceItem) {
            dataSourceItem.weight = paramItem.weight;
          }
        });
      },
      handleNodeSelect(selectedKeys, e) {
        console.log(selectedKeys, e);
        if (e !== 'left' && e.node.checkable) {
          const selectedKey = e.node.value;
          let index = this.targetKeys.indexOf(selectedKey);
          if (index !== -1) {
            this.targetKeys.splice(index, 1);
          } else {
            this.targetKeys.push(selectedKey);
          }
        }
        this.changeWeight();
      },
      changeWeight() {
        let seq = 1;
        this.params[this.formItem.formName] = this.dataSource.reduce((acc, item) => {
          if (this.targetKeys.includes(item.value)) {
            acc.push({
              sourceBenchmarkId: item.value,
              weight: item.weight,
              seq: seq++,
            });
          }
          return acc;
        }, []);
      },
    },
  };
</script>

<style scoped lang="less">
  .transfer-tree {
    ::v-deep(.ant-tree .ant-tree-treenode) {
      width: 100%;
    }

    ::v-deep(.ant-tree .ant-tree-node-content-wrapper) {
      width: 100%;
    }
  }
</style>
