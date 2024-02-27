<template>
  <Form
    :model="formState"
    name="form"
    autocomplete="off"
    ref="formRef"
    layout="horizontal"
    :label-col="{ span: 4 }"
    :wrapper-col="{ span: 16 }"
    style="margin-top: 20px"
  >
    <!--    评价指导 基准guidance-->
    <FormItem
      name="guidance"
      label="评价指导："
      :colon="false"
      :rules="[
        {
          required: false,
          trigger: ['blur', 'change'],
          whitespace: true,
        },
      ]"
    >
      <TextArea
        v-model:value="guidance"
        show-count
        :maxlength="255"
        :autoSize="{ minRows: 2, maxRows: 4 }"
      />
    </FormItem>
    <!--    得分符号:也要看传入的格式-->
    <FormItem
      name="scoreSymbolName"
      label="得分符号："
      :colon="false"
      :rules="[
        {
          required: true,
          trigger: ['blur', 'change'],
          validator: validateScoreSymbolName,
        },
      ]"
    >
      <RadioGroup v-model:value="scoreSymbolName" @change="changeScoreSymbolName">
        <Radio v-for="item in scoreSymbolList" :value="item" :key="item">
          {{ item.valueTypeString }}
        </Radio>
      </RadioGroup>
    </FormItem>
    <!--选择哪一类，例如优秀、良好，例如ABCD，贴纸-->
    <!--    展示条件：得分符号选了STRING类型，并且这个类型有多种展示的sting options（否则默认第一个）-->
    <FormItem
      name="inputScoreSymbol"
      :label="scoreSymbolName.valueTypeString + '类型：'"
      :colon="false"
      v-if="scoreSymbolName"
      :rules="{
        required: true,
        trigger: ['blur'],
      }"
    >
      <RadioGroup v-model:value="inputScoreSymbol" v-if="scoreSymbolName.optionsList">
        <Radio v-for="(item, index) in scoreSymbolName.optionsList" :value="item" :key="index">
          {{ item.stringOptions || item.name }}
        </Radio>
      </RadioGroup>
    </FormItem>

    <!--    若是数字分值，设置区间，默认左右包含-->
    <!--    展示条件：得分符号选了NUM类型-->
    <FormItem
      name="scoreRange"
      label="得分区间："
      :colon="false"
      v-if="inputScoreSymbol && scoreSymbolName && scoreSymbolName.valueType === 'NUM'"
      :rules="{
        required: true,
        trigger: ['blur'],
        validator: validateNumericScore,
      }"
    >
      <InputNumber
        v-model:value="numericMinScore"
        style="width: 100px"
        min="0"
        :precision="scoreSymbolName.numericPrecision"
      />
      <span style="margin: 0 10px">至</span>
      <FormItemRest>
        <InputNumber
          v-model:value="numericMaxScore"
          style="width: 100px"
          min="0"
          :precision="scoreSymbolName.numericPrecision"
        />
      </FormItemRest>
    </FormItem>
    <!--上一类里的ABCD里选 -->
    <!--    展示条件：得分符号选了STRING类型，并且已经确定了是那种等级展示方式，类似['优秀'，'良好']，从里面选； -->
    <FormItem
      name="limitedStringOptions"
      label="可选项："
      :colon="false"
      v-if="
        inputScoreSymbol && scoreSymbolName.valueType === 'STRING' && inputScoreSymbol.stringOptions
      "
      :rules="{
        required: true,
        trigger: ['blur'],
      }"
    >
      <CheckboxGroup v-model:value="limitedStringOptions" @change="prepareOutputScoreSymbol">
        <Row>
          <Col v-for="item in inputScoreSymbol.stringOptions" :key="item" :span="8">
            <Checkbox :value="item">{{ item }}</Checkbox>
          </Col>
        </Row>
      </CheckboxGroup>
    </FormItem>
    <!--    任课老师的时候，选任教课程-->
    <FormItem
      name="radioFormItem"
      :label="rule.optionsDescription + `：`"
      :colon="false"
      v-if="rule && rule.componentType === 'SINGLE_CHOICE'"
      :rules="[
        {
          required: true,
          trigger: ['blur', 'change'],
          message:
            rule.componentType === 'SINGLE_CHOICE' ? '请选择' + rule.name : '请输入' + rule.name,
          type: 'array',
          validator: validateRule,
        },
      ]"
    >
      <RadioGroup v-model:value="optionsValue">
        <Radio v-for="radioItem in rule.options" :value="radioItem.value" :key="radioItem.value">
          {{ radioItem.name }}
        </Radio>
      </RadioGroup>
    </FormItem>
    <!--    同班同学的时候，选评价人数-->
    <FormItem
      name="classmatesCount"
      label="评价人数："
      :colon="false"
      v-if="rule && rule.componentType === 'DIGITAL_INPUT_AND_STATS'"
      :rules="[
        {
          required: true,
          trigger: ['blur', 'change'],
          message:
            rule.componentType === 'SINGLE_CHOICE' ? '请选择' + rule.name : '请输入' + rule.name,
          type: 'array',
          validator: validateRule,
        },
      ]"
    >
      <InputNumber v-model:value="classmatesCount" style="width: 100%" :precision="0" />
    </FormItem>
    <!--    选评价人数 > 1,选统计方法-->
    <FormItem
      name="statsMethod"
      label="统计方法"
      :colon="false"
      v-if="rule && rule.componentType === 'DIGITAL_INPUT_AND_STATS' && classmatesCount > 1"
      :rules="{
        required: true,
        trigger: ['blur'],
      }"
    >
      <RadioGroup v-model:value="statsMethod">
        <Radio v-for="radioItem in rule.options" :value="radioItem.value" :key="radioItem.value">
          {{ radioItem.name }}
        </Radio>
      </RadioGroup>
    </FormItem>
    <!--    若是综合等级，输入规则-->
    <!--      v-if="rule && rule.componentType === 'RULE'"-->
    <div
      v-if="
        scoreSymbolName &&
        scoreSymbolName.valueType === 'STRING' &&
        limitedStringOptions.length > 0 &&
        rule &&
        rule.componentType === 'RANGE_VALUE'
      "
    >
      <FormItem
        :name="`option${index}`"
        :label="options.matchValue + '：'"
        :colon="false"
        :rules="{
          required: true,
          trigger: ['blur', 'change'],
          validator: (_, value) => validateOutputScoreSymbol(options, index),
        }"
        v-for="(options, index) in rangeValueList"
        :key="index"
      >
        <FormItemRest>
          <InputNumber
            v-model:value="options.minScore"
            style="width: 100px"
            min="0"
            :precision="0"
          />
          <span style="margin: 0 10px">至</span>
          <InputNumber
            v-model:value="options.maxScore"
            style="width: 100px"
            min="0"
            :precision="0"
          />
        </FormItemRest>
      </FormItem>
    </div>
  </Form>
</template>

<script lang="ts">
  import { Checkbox, Form, InputNumber, Radio, Row, Col, Input } from 'ant-design-vue';
  import { reactive, ref, toRefs } from 'vue';
  import { apiGetScoreSymbolList } from '/@/api/scoreSymbol/scoreSymbol';

  export default {
    name: 'BenchmarkForm',
    components: {
      Form,
      FormItem: Form.Item,
      FormItemRest: Form.ItemRest,
      InputNumber,
      RadioGroup: Radio.Group,
      Radio,
      CheckboxGroup: Checkbox.Group,
      Checkbox,
      Row,
      Col,
      TextArea: Input.TextArea,
    },
    props: {
      rule: {
        type: Object,
      },
      inputScoreSymbolType: {
        type: Array,
      },
      benchmark: {
        type: Object,
      },
    },
    setup(props) {
      // 使用defineProps定义props
      const guidance1 = ref(props.benchmark.guidance);
      const formRef = ref(null);
      const formState = reactive({
        inputScoreSymbol: null,
        outputScoreSymbol: null,
        numericMinScore: null,
        numericMaxScore: null,
        limitedStringOptions: [],
        classItem: null,
        classmatesCount: null,
        statsMethod: null,
        guidance: null,
        rangeValueList: [],
        optionsValue: null,
        name: null,
        calcMethod: null,
        id: null,
        version: 1,
        benchmarkInputNodeId: null,
        benchmarkInputNodeVersion: 1,
      });
      const scoreSymbolList = ref([]);
      const scoreSymbolName = ref(null);
      // 检验得分符号，目前是只选等级还是星
      const validateScoreSymbolName = async (_rule) => {
        if (scoreSymbolName.value === null) {
          return Promise.reject('请选择得分符号');
        }
        return Promise.resolve();
      };
      // 检验得分区间，当前规则：大于0 整数
      const validateNumericScore = async (_rule) => {
        if (formState.numericMinScore === null) {
          return Promise.reject('请输入最小值');
        } else if (formState.numericMaxScore === null) {
          return Promise.reject('请输入最大值');
        } else if (formState.numericMinScore > formState.numericMaxScore) {
          return Promise.reject('最小值不能大于最大值');
        }
        return Promise.resolve();
      };
      const validateRule = async (_rule) => {
        if (formState[props.rule.itemValue] === null) {
          return Promise.reject();
        }
        return Promise.resolve();
      };
      const validateOutputScoreSymbol = async (value, index) => {
        const higherOptions = formState.rangeValueList[index - 1];
        const lowerOptions = formState.rangeValueList[index + 1];
        if (value.minScore === null) {
          return Promise.reject(`请输入${value.matchValue}的最小值`);
        } else if (value.maxScore === null) {
          return Promise.reject(`请输入${value.matchValue}的最大值`);
        } else if (value.minScore > value.maxScore) {
          return Promise.reject(`${value.matchValue}的最小值不能大于最大值`);
        } else if (higherOptions && higherOptions.minScore <= value.maxScore) {
          return Promise.reject(
            `${value.matchValue}的最大值不能小于等于${higherOptions.matchValue}的最小值`,
          );
        } else if (lowerOptions && lowerOptions.maxScore >= value.minScore) {
          return Promise.reject(
            `${value.matchValue}的最小值不能小于等于${lowerOptions.matchValue}的最大值`,
          );
        }
        return Promise.resolve();
      };

      const initFormState = () => {
        formState.guidance = props.benchmark.guidance;
        formState.name = props.benchmark.name;
        formState.calcMethod = props.benchmark.calcMethod;
        formState.id = props.benchmark.id;
        formState.version = props.benchmark.version ? props.benchmark.version : 1;
        const inputNodeInfo = props.benchmark.inputNodeInfo;
        if (inputNodeInfo) {
          formState.benchmarkInputNodeId = inputNodeInfo.id;
          formState.benchmarkInputNodeVersion = inputNodeInfo.version;
          scoreSymbolList.value.forEach((item) => {
            if (item.valueType === inputNodeInfo.inputScoreSymbol.valueType) {
              scoreSymbolName.value = item;
            }
          });
          formState.inputScoreSymbol = scoreSymbolName.value?.optionsList?.find(
            (item) => item.id === inputNodeInfo.inputScoreSymbol.id,
          );
          formState.numericMinScore = inputNodeInfo.numericMinScore;
          formState.numericMaxScore = inputNodeInfo.numericMaxScore;
          if (inputNodeInfo.limitedStringOptions) {
            formState.limitedStringOptions = inputNodeInfo.limitedStringOptions;
          }
          if (inputNodeInfo.fillerCalcContext) {
            formState.optionsValue = inputNodeInfo.fillerCalcContext.team_category_id
              ? inputNodeInfo.fillerCalcContext.team_category_id
              : inputNodeInfo.fillerCalcContext.subject;
          }
        } else {
          formState.benchmarkInputNodeId = null;
          formState.benchmarkInputNodeVersion = 1;
          formState.inputScoreSymbol = null;
          formState.numericMinScore = null;
          formState.numericMaxScore = null;
          formState.limitedStringOptions = [];
          scoreSymbolName.value = null;
        }
      };

      const getScoreSymbolList = () => {
        scoreSymbolList.value = [];
        const params = {
          valueTypeList: props.inputScoreSymbolType,
        };
        apiGetScoreSymbolList(params)
          .then((res) => {
            if (res.code === 200) {
              scoreSymbolList.value = res.data;
            }
          })
          .finally(() => {
            initFormState();
          });
      };
      getScoreSymbolList();
      // watch(guidance, (newValue, oldValue) => {
      //   console.log('guidance changed from', oldValue, 'to', newValue);
      // });
      return {
        formState,
        ...toRefs(formState),
        scoreSymbolList,
        validateRule,
        formRef,
        validateScoreSymbolName,
        validateNumericScore,
        validateOutputScoreSymbol,
        scoreSymbolName,
        guidance1,
      };
    },
    methods: {
      changeScoreSymbolName() {
        this.inputScoreSymbol = this.scoreSymbolName.optionsList[0];
        if (this.scoreSymbolName.valueType === 'STRING') {
          this.numericMinScore = null;
          this.numericMaxScore = null;
        } else {
          this.limitedStringOptions = [];
        }
      },
      prepareOutputScoreSymbol() {
        // this.outputScoreSymbol = cloneDeep(this.inputScoreSymbol);
        // const newStringOptions = [];
        // this.limitedStringOptions.forEach((options) => {
        //   newStringOptions.push({
        //     matchValue: options,
        //     minScore: null,
        //     maxScore: null,
        //     leftOperator: '>=',
        //     rightOperator: '<=',
        //   });
        // });
        // this.rangeValueList = newStringOptions;
      },
    },
  };
</script>

<style scoped></style>
