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
    <span v-if="readonly">{{ getSpanValue() }}</span>
    <RadioGroup
      v-else
      v-model:value="params[formItem.formName]"
      @change="changeRadioValue"
      :disabled="readonly"
    >
      <Tooltip v-for="option in formItem.items" :key="option.value">
        <template #title v-if="option.disabled === true">该选项不可选，或已禁用，请选择其它项</template>
        <Radio :disabled="option.disabled" :value="option.value">
          {{ option.name }}
        </Radio>
      </Tooltip>
    </RadioGroup>
  </FormItem>
  <component
    ref="childrenComponentRef"
    v-if="formItem.itemParams && params[formItem.formName]"
    :is="getComponent()"
    :formItem="formItem.itemParams[params[formItem.formName]]"
    :needNotifyParent="true"
    :readonly="readonly"
    :key="refreshKey"
  />
</template>

<script lang="ts">
  import { Form, Radio, Tooltip } from 'ant-design-vue';
  import { nextTick, reactive, ref } from 'vue';
  import IntegerFormItem from '/@/views/evaluationCriteriaTree/components/BenchmarkFormItem/IntegerFormItem.vue';
  import NumericRangeFormItem from '/@/views/evaluationCriteriaTree/components/BenchmarkFormItem/NumericRangeFormItem.vue';
  import MultipleChoiceFormItem from '/@/views/evaluationCriteriaTree/components/BenchmarkFormItem/MultipleChoiceFormItem.vue';

  export default {
    name: 'SingleChoiceFormItem',
    components: {
      FormItem: Form.Item,
      RadioGroup: Radio.Group,
      Radio,
      IntegerFormItem,
      NumericRangeFormItem,
      MultipleChoiceFormItem,
      Tooltip,
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
    emits: ['getBenchmarkInputParams'],
    setup(props) {
      const params = reactive({});
      const validateFormItem = async (_rule) => {
        if (!params[props.formItem.formName]) {
          return Promise.reject('请选择' + props.formItem.title);
        }
        if (
          props.formItem.items.find((item) => item.value === params[props.formItem.formName])
            .disabled === true
        ) {
          return Promise.reject('该选项不可选，或已禁用，请选择其它项');
        }
        return Promise.resolve();
      };
      const refreshKey = ref(new Date().getTime());
      return {
        params,
        validateFormItem,
        refreshKey,
      };
    },
    methods: {
      getParams() {
        //   循环求所有子节点的params
        const childParams = this.$refs.childrenComponentRef?.getParams() || {};
        return {
          ...this.params,
          ...childParams,
        };
      },
      setParams(parentParams) {
        this.formItem.items.forEach((item) => {
          if (JSON.stringify(item.value) === JSON.stringify(parentParams[this.formItem.formName])) {
            this.params[this.formItem.formName] = item.value;
          }
        });
        // this.params[this.formItem.formName] = cloneDeep(parentParams[this.formItem.formName]);
        nextTick(() => {
          console.log('this.$refs.childrenComponentRef?.setParams(parentParams)');
          this.$refs.childrenComponentRef?.setParams(parentParams);
        });
      },
      changeRadioValue() {
        this.refreshKey = new Date().getTime();
        // 选了符号再去加载，虽然是嵌套组件，但是只在第一级组件加了emit事件，后续就算是单选也不会触发
        this.$emit('getBenchmarkInputParams', this.params[this.formItem.formName]);
      },
      getComponent() {
        const item = this.formItem.itemParams[this.params[this.formItem.formName]];
        const type = item?.componentType;
        switch (type) {
          case 'SINGLE_CHOICE':
            return 'SingleChoiceFormItem';
          case 'INTEGER':
            return 'IntegerFormItem';
          case 'NUMERIC_RANGE':
            return 'NumericRangeFormItem';
          case 'MULTIPLE_CHOICE':
            return 'MultipleChoiceFormItem';
          default:
            return null; // 或者返回一个默认组件
        }
      },
      getSpanValue() {
        let spanValue = this.formItem.items.find(
          (item) => item.value === this.params[this.formItem.formName],
        );
        return spanValue?.name;
        // return this.formItem.items.find(
        //   (item) => item.value === this.params[this.formItem.formName],
        // ).name;
      },
    },
  };
</script>

<style scoped></style>
