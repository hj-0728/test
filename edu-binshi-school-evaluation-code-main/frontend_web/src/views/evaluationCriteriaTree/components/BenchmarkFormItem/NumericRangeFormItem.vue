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
    <InputNumber
      v-model:value="params[Object.keys(formItem.formName)[0]]"
      style="width: 100px"
      min="0"
      :precision="0"
      :readonly="readonly"
    />
    <span style="margin: 0 10px">至</span>
    <FormItemRest>
      <InputNumber
        v-model:value="params[Object.keys(formItem.formName)[1]]"
        style="width: 100px"
        min="0"
        :precision="0"
        :readonly="readonly"
      />
    </FormItemRest>
  </FormItem>
</template>

<script>
  import { Form, InputNumber } from 'ant-design-vue';
  import { reactive } from 'vue';

  export default {
    name: 'NumericRangeFormItem',
    components: {
      FormItem: Form.Item,
      InputNumber,
      FormItemRest: Form.ItemRest,
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
      const params = reactive({});

      const validateFormItem = async (_rule) => {
        if (
          params[Object.keys(props.formItem.formName)[0]] === undefined ||
          params[Object.keys(props.formItem.formName)[1]] === undefined
        ) {
          return Promise.reject('请输入区间值');
        } else if (
          params[Object.keys(props.formItem.formName)[0]] >=
          params[Object.keys(props.formItem.formName)[1]]
        ) {
          return Promise.reject('最大值必须大于最小值');
        }
        return Promise.resolve();
      };
      return {
        params,
        validateFormItem,
      };
    },
    methods: {
      getParams() {
        //   循环求所有子节点的params
        return {
          ...this.params,
          ...this.$refs.childrenComponentRef?.getParams(),
        };
      },
      setParams(parentParams) {
        Object.keys(this.formItem.formName).forEach((item) => {
          this.params[item] = parentParams[item];
        });
      },
    },
  };
</script>

<style scoped></style>
