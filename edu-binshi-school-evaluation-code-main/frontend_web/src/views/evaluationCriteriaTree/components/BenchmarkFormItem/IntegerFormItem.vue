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
    <span v-if="readonly">{{ params[formItem.formName] }}</span>
    <InputNumber
      v-else
      :readonly="readonly"
      v-model:value="params[formItem.formName]"
      style="width: 100px"
      :min="formItem.min ? formItem.min : 0"
      :precision="0"
    />
  </FormItem>
</template>

<script>
  import { Form, InputNumber } from 'ant-design-vue';
  import { reactive } from 'vue';

  export default {
    name: 'IntegerFormItem',
    components: {
      FormItem: Form.Item,
      InputNumber,
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
        if (!params[props.formItem.formName]) {
          return Promise.reject('请输入' + props.formItem.title);
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
      setParams(benchmarkStrategyParams) {
        this.params[this.formItem.formName] = benchmarkStrategyParams[this.formItem.formName];
      },
    },
  };
</script>

<style scoped>
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.5s;
  }

  .fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
    opacity: 0;
  }
</style>
