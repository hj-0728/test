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
    <CheckboxGroup
      :disabled="readonly"
      v-model:value="params[formItem.formName]"
      style="width: 100%"
    >
      <Row>
        <Col :span="24" v-for="option in formItem.items" :key="option">
          <Checkbox style="margin: 6px 0" :value="option.value">{{ option.name }}</Checkbox>
        </Col>
      </Row>
    </CheckboxGroup>
  </FormItem>
</template>

<script lang="ts">
  import { Checkbox, Col, Form, Row } from 'ant-design-vue';
  import { reactive, toRefs } from 'vue';

  export default {
    name: 'NumericRangeFormItem',
    components: {
      Col,
      Checkbox,
      Row,
      FormItem: Form.Item,
      CheckboxGroup: Checkbox.Group,
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
        if (!params[props.formItem.formName] || params[props.formItem.formName].length < 2) {
          return Promise.reject('请选择至少两个' + props.formItem.title);
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
      },
    },
  };
</script>

<style scoped></style>
