<template>
<!--  <div style="width: 80%; margin: 50px auto;" ref="slider"></div>-->
  <FormItem
    :name="formItem.formName"
    :label="options.matchValue + formItem.title"
    :rules="{
      required: required,
      trigger: ['blur'],
      validator: (_, value) => validateFormItem(options, index),
    }"
    v-for="(options, index) in params[formItem.formName]"
  >
    <FormItemRest>
      <div style="display: inline-flex;align-items: center">
      <InputNumber v-model:value="options.minScore" style="width: 150px" min="0" :precision="0" :readonly="readonly">
        <template #addonBefore>
          <Select
            v-model:value="options.leftOperator"
            :options="leftOperatorOptions"
            style="width: 60px"
            :disabled="readonly"
          />
        </template>
      </InputNumber>
      <span style="margin: 0 10px">至</span>
      <InputNumber v-model:value="options.maxScore" style="width: 150px" min="0" :precision="0" :readonly="readonly">
        <template #addonAfter>
          <Select
            v-model:value="options.rightOperator"
            :options="rightOperatorOptions"
            style="width: 60px"
            :disabled="readonly"
          />
        </template>
      </InputNumber>
      </div>
    </FormItemRest>
  </FormItem>
</template>

<script lang="ts">
  import { Form, InputNumber, Select } from 'ant-design-vue';
  import { inject, reactive, ref, computed, onMounted, onBeforeUnmount, watch } from 'vue';
  import 'nouislider/dist/nouislider.css';
  import noUiSlider from 'nouislider';
  export default {
    name: 'RangeValueFormItem',
    components: {
      FormItem: Form.Item,
      InputNumber,
      FormItemRest: Form.ItemRest,
      Select,
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
      // const { formItem } = toRefs(props);
      const params = reactive({
        [props.formItem.formName]: computed(() => {
          return rangeValueList.value;
        }),
      });
      const leftOperatorOptions = ref([
        {
          value: '>=',
          label: '[',
        },
        {
          value: '>',
          label: '(',
        },
      ]);
      const rightOperatorOptions = ref([
        {
          value: '<=',
          label: ']',
        },
        {
          value: '<',
          label: ')',
        },
      ]);
      const limitedStringOptions: any = ref(inject('limitedStringOptions'));
      watch(limitedStringOptions, (newValue, oldValue) => {
        updateObjectList();
      });
      const rangeValueList = ref([]);
      const updateObjectList = () => {
        // 首先，确保 rangeValueList 中的所有项都在 limitedStringOptions 中
        for (let i = rangeValueList.value.length - 1; i >= 0; i--) {
          if (!limitedStringOptions.value.includes(rangeValueList.value[i].matchValue)) {
            rangeValueList.value.splice(i, 1);
          }
        }

        // 按 limitedStringOptions.value 的顺序重新排列或添加项目
        for (let i = 0; i < limitedStringOptions.value.length; i++) {
          const name = limitedStringOptions.value[i];
          const existingItem = rangeValueList.value.find((item) => item.matchValue === name);

          if (existingItem) {
            // 如果项目已经在 rangeValueList 中，将其移动到正确的位置
            const currentIndex = rangeValueList.value.indexOf(existingItem);
            if (currentIndex !== i) {
              rangeValueList.value.splice(currentIndex, 1);
              rangeValueList.value.splice(i, 0, existingItem);
            }
          } else {
            // 否则，添加新项目到正确的位置
            rangeValueList.value.splice(i, 0, {
              minScore: null,
              maxScore: null,
              leftOperator: '>=',
              rightOperator: '<=',
              matchValue: name,
            });
          }
        }
        console.log(' rangeValueList.value', rangeValueList.value)
      };
      const validateFormItem = async (value, index) => {
        const higherOptions = params[props.formItem.formName][index - 1];
        const lowerOptions = params[props.formItem.formName][index + 1];
        if (value.minScore === null) {
          return Promise.reject(`请输入${value.matchValue}的最小值`);
        }
        if (value.maxScore === null) {
          return Promise.reject(`请输入${value.matchValue}的最大值`);
        }
        if (value.minScore > value.maxScore ) {
          return Promise.reject(`${value.matchValue}的最大值必须大于最小值`);
        }
        if (value.rightOperator !== '<=' && value.minScore === value.maxScore ) {
          return Promise.reject(`此区间取值不成立`);
        }

        // Check against higher range (the one before the current)
        if (lowerOptions) {
          if (value.leftOperator === '>=' && lowerOptions.rightOperator === '<=') {
            if (value.maxScore <= lowerOptions.minScore) {
              return Promise.reject(
                `${value.matchValue}的区间取值必须大于${lowerOptions.matchValue}的区间取值`,
              );
            } else if (value.minScore < lowerOptions.maxScore) {
              return Promise.reject(
                `${value.matchValue}的区间取值与${lowerOptions.matchValue}的区间取值重叠`,
              );
            }
          } else {
            if (value.maxScore <= lowerOptions.minScore) {
              return Promise.reject(
                `${value.matchValue}的区间取值必须大于${lowerOptions.matchValue}的区间取值`,
              );
            } else if (value.minScore < lowerOptions.maxScore) {
              return Promise.reject(
                `${value.matchValue}的区间取值与${lowerOptions.matchValue}的区间取值重叠`,
              );
            }
          }
        }

        // Check against lower range (the one after the current)
        if (higherOptions) {
          if (value.rightOperator === '<=' && higherOptions.leftOperator === '>=') {
            if (value.maxScore >= higherOptions.minScore) {
              return Promise.reject(
                `${value.matchValue}的区间取值必须小于${higherOptions.matchValue}的区间取值`,
              );
            } else if (value.maxScore >= higherOptions.minScore) {
              return Promise.reject(
                `${value.matchValue}的区间取值与${higherOptions.matchValue}的区间取值重叠`,
              );
            }
          } else {
            if (value.minScore >= higherOptions.maxScore) {
              return Promise.reject(
                `${value.matchValue}的区间取值必须小于${higherOptions.matchValue}的区间取值`,
              );
            } else if (value.maxScore > higherOptions.minScore) {
              return Promise.reject(
                `${value.matchValue}的区间取值与${higherOptions.matchValue}的区间取值重叠`,
              );
            }
          }
        }
        return Promise.resolve();
      };
      const slider = ref(null);

      // onMounted(() => {
      //   if (slider.value) {
      //     noUiSlider.create(slider.value, {
      //       start: [0, 100],
      //       range: {
      //         min: 0,
      //         max: 100,
      //       },
      //       step: 150,
      //       connect: true,
      //     });
      //   }
      // });

      return {
        params,
        validateFormItem,
        rangeValueList,
        limitedStringOptions,
        leftOperatorOptions,
        rightOperatorOptions,
        slider,
      };
    },
    methods: {
      setParams(benchmarkStrategyParams) {
        console.log(222222222222,benchmarkStrategyParams[this.formItem.formName])
        this.rangeValueList = benchmarkStrategyParams[this.formItem.formName]
        console.log(this.params[this.formItem.formName])
      },
    },
  };
</script>

<style scoped lang="less">
</style>
