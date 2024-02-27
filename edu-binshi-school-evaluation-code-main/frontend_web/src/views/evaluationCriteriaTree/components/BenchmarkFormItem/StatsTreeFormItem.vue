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
    <div class="indicator-tree">
      <Tree
        class="transfer-tree"
        check-strictly
        checkable
        default-expand-all
        :field-names="{ key: 'value', title: 'name' }"
        :checked-keys="[...targetKeys]"
        :tree-data="treeData"
        :disabled="readonly"
        @select="handleNodeSelect"
        @check="handleNodeSelect"
      />
    </div>
  </FormItem>
</template>

<script lang="ts">
  import { Form, TransferProps, Tree } from 'ant-design-vue';
  import { computed, reactive, ref } from 'vue';

  export default {
    name: 'StatsTreeFormItem',
    components: {
      Tree,
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

        if (params[props.formItem.formName].length < 2) {
          return Promise.reject('请选择至少两个' + props.formItem.title);
        }
        return Promise.resolve();
      };

      return {
        params,
        validateFormItem,
        dataSource,
        treeData,
        selectedKeys,
        selectedChildrenMap,
        targetKeys,
      };
    },
    methods: {
      setParams(benchmarkStrategyParams) {
        this.targetKeys = [];
        this.selectedChildrenMap = {};
        this.params[this.formItem.formName] = benchmarkStrategyParams[this.formItem.formName];
        this.params[this.formItem.formName].forEach((sourceBenchmarkId) => {
          this.targetKeys.push(sourceBenchmarkId);
        });
      },
      handleNodeSelect(selectedKeys, e) {
        console.log('handleNodeSelect');
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
        console.log(this.targetKeys);
        this.params[this.formItem.formName] = this.targetKeys;
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

  .indicator-tree {
    border: 1px solid #d9d9d9;
    padding: 10px;
    border-radius: 8px;
    margin-top: 8px;
  }
</style>
