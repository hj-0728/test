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
    <FormItemRest>
      <div style="margin: 6px 0; color: red; font-size: 14px">
        <InfoCircleOutlined />
        <span style="padding: 0 4px">不参与聚合的选项无需输入权重，删除权重即不参与计算</span>
      </div>
      <div
        v-for="benchmark in formItem.items"
        :key="benchmark"
        style="display: flex; align-items: center"
      >
        <InputNumber
          v-model:value="benchmark.weight"
          style="width: 400px; margin: 5px 0; height: 36px"
          min="1"
          :precision="0"
          :readonly="readonly"
          @change="changeWeight"
          placeholder="请输入权重"
        >
          <template #addonBefore>
            <Checkbox style="margin: 6px 0" :checked="benchmark.weight" :disabled="readonly">
              <span style="display: block; width: 150px">{{ benchmark.name }}</span>
            </Checkbox>
          </template>
        </InputNumber>
      </div>
    </FormItemRest>
  </FormItem>
</template>

<script lang="ts">
  import { Checkbox, Form, InputNumber } from 'ant-design-vue';
  import { reactive, toRefs } from 'vue';
  import { InfoCircleOutlined } from '@ant-design/icons-vue';

  export default {
    name: 'NumericRangeFormItem',
    components: {
      Checkbox,
      FormItem: Form.Item,
      InputNumber,
      FormItemRest: Form.ItemRest,
      InfoCircleOutlined,
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
      const { formItem } = toRefs(props);
      const params = reactive({});
      params[formItem.value.formName] = formItem.value.items;

      const validateFormItem = async (_rule) => {
        console.log('weight validateFormItem------');
        console.log(params[formItem.value.formName]);
        let weightCount = 0;
        params[formItem.value.formName].forEach((val) => {
          if (val.weight) {
            weightCount += 1;
          }
        });
        if (weightCount < 2) {
          return Promise.reject('请至少输入两个权重');
        }
        return Promise.resolve();
      };
      return {
        params,
        validateFormItem,
      };
    },
    methods: {
      setParams(benchmarkStrategyParams) {
        this.params[this.formItem.formName] = benchmarkStrategyParams[this.formItem.formName];
        let mapB = new Map(
          this.params[this.formItem.formName].map((item) => [item.sourceBenchmarkId, item]),
        );

        for (let itemA of this.formItem.items) {
          if (mapB.has(itemA.value)) {
            itemA.weight = mapB.get(itemA.value).weight;
          }
        }
      },
      changeWeight() {
        let weightNodeList = [];
        let seq = 1;
        this.formItem.items.forEach((benchmark) => {
          if (benchmark.weight) {
            weightNodeList.push({
              sourceBenchmarkId: benchmark.value,
              weight: benchmark.weight,
              seq: seq++,
            });
          }
        });
        this.params[this.formItem.formName] = weightNodeList;
      },
    },
  };
</script>

<style scoped lang="less">
  ::v-deep(.ant-input-number) {
    height: 36px !important;
  }
</style>
