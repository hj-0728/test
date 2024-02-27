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
      @change="changeCheckbox"
    >
      <Row>
        <Col v-for="option in formItem.items" :key="option">
          <Checkbox :value="option.value" >{{ option.name }}</Checkbox>
        </Col>
      </Row>
    </CheckboxGroup>
  </FormItem>
</template>

<script lang="ts">
  import { Form, Checkbox, Row, Col } from 'ant-design-vue';
  import { reactive, defineComponent } from 'vue';
  export default defineComponent({
    name: 'MultipleChoiceFormItem',
    components: {
      FormItem: Form.Item,
      CheckboxGroup: Checkbox.Group,
      Checkbox,
      Row,
      Col,
    },
    inject: ['changeParams'],
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
      // 当这个组件是为了选择的等级类的得分符号，通知editModal组件
      needNotifyParent: {
        type: Boolean,
        default: false,
      },
    },
    setup(props) {
      const params = reactive({});

      const validateFormItem = async (_rule) => {
        if (!params[props.formItem.formName] || params[props.formItem.formName].length === 0) {
          return Promise.reject('请选择' + props.formItem.title);
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
      setParams(parentParams){
        console.log(22222222222222222222222,parentParams)
        this.params[this.formItem.formName] = parentParams[this.formItem.formName];
        if (this.needNotifyParent) {
          this.changeParams(this.params[this.formItem.formName]);
        }
      },
      changeCheckbox(checkedList) {
        this.params[this.formItem.formName] = this.formItem.items
          .map((option) => option.value)
          .filter((value) => checkedList.includes(value));
        if (this.needNotifyParent) {
          this.changeParams(this.params[this.formItem.formName]);
        }
      },
    },
  });
</script>

<style scoped></style>
