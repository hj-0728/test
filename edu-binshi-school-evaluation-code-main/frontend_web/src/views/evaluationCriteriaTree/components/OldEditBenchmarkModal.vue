<template>
  <div ref="editBenchmarkModalRef" class="edit-benchmark-modal">
    <BasicModal
      @register="register"
      :canFullscreen="false"
      :defaultFullscreen="false"
      :draggable="false"
      :destroyOnClose="true"
      :getContainer="() => $refs.editBenchmarkModalRef"
      :closable="true"
      :centered="true"
      :maskClosable="false"
      width="60vw"
    >
      <template #title>
        <Icon icon="ri:file-list-2-line" />
        <span v-if="modalCategory === 'EDIT'"> 编辑{{ benchmark.name }}评价项 </span>
        <span v-if="modalCategory === 'ADD'"> 添加评价项 </span>
      </template>
      <Loading :loading="fullScreenLoading" :absolute="false" />
      <div class="content">
        <Row v-if="modalCategory === 'ADD'">
          <Col :span="3" />
          <Col :span="18">
            <Alert :message="'当前节点：' + evaluationCriteriaTreeNode?.name" type="info" />
          </Col>
          <Col :span="3" />
        </Row>
        <Form
          :model="params"
          name="form"
          autocomplete="off"
          ref="formRef"
          layout="horizontal"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          style="margin-top: 20px"
        >
          <FormItem name="name" label="名称">
            <TextArea
              v-model:value="name"
              show-count
              :maxlength="255"
              :autoSize="{ minRows: 2, maxRows: 4 }"
              :rules="[
                {
                  required: false,
                  trigger: ['blur', 'change'],
                  whitespace: true,
                },
              ]"
            />
          </FormItem>
          <FormItem
            name="guidance"
            label="评价指导"
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
          <!--          <FormItem-->
          <!--            name="tag"-->
          <!--            label="类型"-->
          <!--            -->
          <!--            v-if="evaluationCriteriaTreeNode?.level === 1"-->
          <!--          >-->
          <!--            <RadioGroup v-model:checked="tag" @change="hasMetricUnitChange" />-->
          <!--          </FormItem>-->
          <FormItem name="benchmark" label="评价类型">
            <RadioGroup v-model:value="benchmarkDefinition" @change="changeBenchmarkDefinition">
              <Radio v-for="item in benchmarkOptions" :value="item" :key="item">
                {{ item.name }}
              </Radio>
            </RadioGroup>
          </FormItem>
          <FormItem
            name="scoreSymbolName"
            label="得分类型"
            :rules="[
              {
                required: true,
                trigger: ['blur', 'change'],
                validator: validateScoreSymbolName,
              },
            ]"
            v-if="benchmarkDefinition"
          >
            <RadioGroup v-model:value="scoreSymbolName" @change="changeScoreSymbolName">
              <Radio v-for="item in scoreSymbolList" :value="item" :key="item">
                {{ item.valueTypeString }}
              </Radio>
            </RadioGroup>
          </FormItem>
          <!--选择哪一类，例如优秀、良好，例如ABCD，贴纸-->
          <!--    展示条件得分符号选了STRING类型，并且这个类型有多种展示的sting options（否则默认第一个）-->
          <FormItem
            name="inputScoreSymbol"
            :label="scoreSymbolName.valueTypeString + '类型'"
            v-if="scoreSymbolName"
            :rules="{
              required: true,
              trigger: ['blur'],
            }"
          >
            <RadioGroup v-model:value="inputScoreSymbol">
              <Radio v-for="item in scoreSymbolName.optionsList" :value="item">
                {{ item.stringOptions || item.name }}
              </Radio>
            </RadioGroup>
          </FormItem>

          <!--    若是数字分值，设置区间，默认左右包含-->
          <!--    展示条件得分符号选了NUM类型-->
          <FormItem
            name="scoreRange"
            label="得分区间"
            v-if="
              inputScoreSymbol &&
              scoreSymbolName?.valueType === 'NUM' &&
              !['AggregatedBenchmark', 'GradeBenchmark'].includes(benchmarkDefinition?.calcMethod)
            "
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
            label="可选项"
            v-if="scoreSymbolName?.valueType === 'STRING' && inputScoreSymbol?.stringOptions"
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
            :label="benchmarkDefinition?.rule?.optionsDescription"
            v-if="benchmarkDefinition?.rule?.componentType === 'SINGLE_CHOICE'"
            :rules="[
              {
                required: true,
                trigger: ['blur', 'change'],
                validator: validateRadioFormItem,
              },
            ]"
          >
            <RadioGroup v-model:value="args.optionsValue">
              <Radio
                v-for="radioItem in benchmarkDefinition?.rule?.options"
                :value="radioItem.value"
                :key="radioItem.value"
              >
                {{ radioItem.name }}
              </Radio>
            </RadioGroup>
          </FormItem>
          <!--          若是综合，得让用户选总分是来源于自身的benchmark还是子节点的任意benchmark-->
          <FormItem
            name="scoreSource"
            label="综合得分来源"
            :rules="{
              required: true,
              trigger: ['blur'],
              validator: validateScoreSource,
            }"
            v-if="inputScoreSymbol && benchmarkDefinition?.calcMethod === 'AggregatedBenchmark'"
          >
            <RadioGroup v-model:value="scoreSource" @change="changeScoreSource">
              <Radio v-for="item in scoreSourceList" :value="item">
                {{ item.name }}
              </Radio>
            </RadioGroup>
          </FormItem>
          <FormItem
            name="weight"
            label="权重"
            :rules="{
              required: true,
              trigger: ['blur', 'change'],
              validator: validateWeight,
            }"
            v-if="scoreSource?.value === 'current'"
          >
            <FormItemRest>
              <div
                v-for="benchmark in benchmarkList"
                :key="benchmark"
                style="display: flex; align-items: center"
              >
                <InputNumber
                  v-model:value="benchmark.weight"
                  style="width: 300px; padding: 5px 0"
                  min="0"
                  :precision="0"
                  @change="changeWeight"
                >
                  <template #addonBefore>
                    <span style="display: block; width: 60px">{{ benchmark.name }}</span>
                  </template>
                </InputNumber>
              </div>
            </FormItemRest>
          </FormItem>
          <!--    若是综合等级，输入规则-->
          <!--      v-if="rule && rule.componentType === 'RULE'"-->
          <div
            v-if="
              scoreSymbolName?.valueType === 'STRING' &&
              limitedStringOptions?.length > 0 &&
              benchmarkDefinition?.rule?.componentType === 'RANGE_VALUE'
            "
          >
            <FormItem
              :name="`option${index}`"
              :label="options.matchValue"
              :rules="{
                required: true,
                trigger: ['blur', 'change'],
                validator: (_, value) => validateOutputScoreSymbol(options, index),
              }"
              v-for="(options, index) in args?.rangeValueList"
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
          <BenchmarkTransferSelect :benchmarkTree="benchmarkTree"/>
<!--          <BenchmarkTransferSelect v-if="scoreSource?.value === 'child'" :benchmarkTree="benchmarkTree"/>-->
        </Form>
      </div>
      <template #footer>
        <Button @click="onCloseModal" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
        <Button
          :type="'primary'"
          color="edit"
          preIcon="ion:paper-airplane"
          :iconSize="16"
          @click="onClickSubmit"
        >
          提交
        </Button>
      </template>
    </BasicModal>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Loading } from '/@/components/Loading';
  import { Icon } from '/@/components/Icon';
  import { Checkbox, Form, Input, Row, Col, Alert, Radio, InputNumber } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import {
    apiGetBenchmarkListByIndicatorId,
    apiGetChildNodeBenchmarkList,
    apiSaveBenchmark,
  } from '/@/api/benchmark/benchmark';
  import { apiGetScoreSymbolList } from '/@/api/scoreSymbol/scoreSymbol';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import BenchmarkTransferSelect from '/@/views/evaluationCriteriaTree/components/BenchmarkTransferSelect.vue';
  import {apiGetBenchmarkStrategyList} from "/@/api/benchmarkStrategy/benchmarkStrategy";

  export default defineComponent({
    components: {
      BasicModal,
      Loading,
      Icon,
      Form,
      FormItem: Form.Item,
      FormItemRest: Form.ItemRest,
      TextArea: Input.TextArea,
      Button,
      Row,
      Col,
      Alert,
      Radio,
      CheckboxGroup: Checkbox.Group,
      RadioGroup: Radio.Group,
      Checkbox,
      InputNumber,
      BenchmarkTransferSelect,
    },
    setup() {
      const formRef = ref();
      const fullScreenLoading = ref(false);
      const evaluationCriteriaTreeNode = ref();
      const modalCategory = ref('ADD');
      const refreshKey = ref(new Date().getTime());
      const [register, { closeModal }] = useModalInner((data) => {
        console.log(data);
        clearPrams();
        refreshKey.value = new Date().getTime();
        modalCategory.value = data.modalCategory;
        evaluationCriteriaTreeNode.value = data.evaluationCriteriaTreeNode;
      });
      const params = reactive({
        id: null,
        name: null,
        version: 1,
        indicatorId: null,
        guidance: null,
        benchmarkDefinition: null,
        numericMinScore: null,
        numericMaxScore: null,
        limitedStringOptions: null,
        inputScoreSymbol: null,
        outputScoreSymbol: null,
        weightNodeList: null,
        args: {
          optionsValue: null,
          rangeValueList: null,
        },
      });
      const benchmarkOptions = ref();
      const scoreSymbolList = ref();
      const scoreSymbolName = ref();
      const loading = ref(true);
      // 当前综合分来源['当前节点','子节点']
      const scoreSourceList = ref([
        // {
        //   name: '当前节点',
        //   value: 'current',
        // },
        // {
        //   name: '子节点',
        //   value: 'children',
        // },
      ]);
      const scoreSource = ref();
      // 当前节点可选择的benchmark
      const benchmarkList = ref([]);
      // 当前节点可选择的benchmark tree
      const benchmarkTree = ref([]);
      // 当前节点可选择的benchmark Strategy List
      const benchmarkStrategyList = ref([]);
      const clearPrams = () => {
        params.id = null;
        params.name = null;
        params.version = 1;
        params.indicatorId = null;
        params.guidance = null;
        params.benchmarkDefinition = null;
        params.numericMinScore = null;
        params.numericMaxScore = null;
        params.limitedStringOptions = null;
        params.inputScoreSymbol = null;
        params.outputScoreSymbol = null;
        params.weightNodeList = null;
        params.args = {
          optionsValue: null,
          rangeValueList: null,
        };
        scoreSourceList.value = [];
        benchmarkTree.value = [];
        benchmarkList.value = [];
        scoreSource.value = null;
      };
      const initParams = () => {};

      // 检验得分符号，目前是只选等级还是星
      const validateScoreSymbolName = async (_rule) => {
        if (scoreSymbolName.value === null) {
          return Promise.reject('请选择得分符号');
        }
        return Promise.resolve();
      };

      const validateOutputScoreSymbol = async (value, index) => {
        const higherOptions = params.args.rangeValueList[index - 1];
        const lowerOptions = params.args.rangeValueList[index + 1];
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
      const validateNumericScore = async (_rule) => {
        if (params.numericMinScore === null) {
          return Promise.reject('请输入最小值');
        } else if (params.numericMaxScore === null) {
          return Promise.reject('请输入最大值');
        } else if (params.numericMinScore > params.numericMaxScore) {
          return Promise.reject('最小值不能大于最大值');
        }
        return Promise.resolve();
      };

      const validateRadioFormItem = async (_rule) => {
        if (!params.args.optionsValue) {
          return Promise.reject('请选择单选项');
        }
        return Promise.resolve();
      };

      const validateScoreSource = async (_rule) => {
        if (!scoreSource.value) {
          return Promise.reject('请选择综合得分来源');
        }
        return Promise.resolve();
      };

      const validateWeight = async (_rule) => {
        return Promise.resolve();
      };
      const getScoreSymbolList = (valueTypeList) => {
        const params = {
          valueTypeList: valueTypeList,
        };
        apiGetScoreSymbolList(params)
          .then((res) => {
            if (res.code === 200) {
              scoreSymbolList.value = res.data;
            }
          })
          .finally(() => {});
      };
      // 如果是综合，先去获取当前节点是否有标准
      const getBenchmarkListByIndicatorId = () => {
        apiGetBenchmarkListByIndicatorId(
          evaluationCriteriaTreeNode.value.indicatorId,
          params.inputScoreSymbol?.id,
        )
          .then((res) => {
            console.log(res);
            if (res.code === 200 && res.data.length > 0) {
              scoreSourceList.value.push({
                name: '当前节点',
                value: 'current',
              });
              benchmarkList.value = res.data;
            } else if (res.error) {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch((error) => {
            console.log(error);
            useMessage().createErrorNotification({
              message: '错误',
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
          })
          .finally(() => {});
      };
      // 如果是综合，先去获取当前节点的子节点是否有标准
      const getChildNodeBenchmarkListByIndicatorId = () => {
        apiGetChildNodeBenchmarkList(
          evaluationCriteriaTreeNode.value.indicatorId,
          params.inputScoreSymbol?.id,
        )
          .then((res) => {
            console.log(res);
            if (res.code === 200 && res.data.length > 0) {
              scoreSourceList.value.push({
                name: '子节点',
                value: 'child',
              });
              benchmarkTree.value = res.data;
            } else if (res.error) {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch((error) => {
            console.log(error);
            useMessage().createErrorNotification({
              message: '错误',
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
          })
          .finally(() => {});
      };

      const getBenchmarkStrategy = () => {
        apiGetBenchmarkStrategyList()
          .then((res) => {
            console.log(res);
            if (res.code === 200 && res.data.length > 0) {
              benchmarkStrategyList.value = res.data;
            } else if (res.error) {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch((error) => {
            console.log(error);
            useMessage().createErrorNotification({
              message: '错误',
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
          })
          .finally(() => {});
      }
      getBenchmarkStrategy()
      return {
        formRef,
        fullScreenLoading,
        modalCategory,
        register,
        closeModal,
        params,
        ...toRefs(params),
        evaluationCriteriaTreeNode,
        benchmarkOptions,
        scoreSymbolList,
        clearPrams,
        refreshKey,
        loading,
        validateScoreSymbolName,
        scoreSymbolName,
        getScoreSymbolList,
        validateNumericScore,
        validateOutputScoreSymbol,
        validateScoreSource,
        scoreSourceList,
        scoreSource,
        benchmarkList,
        getBenchmarkListByIndicatorId,
        getChildNodeBenchmarkListByIndicatorId,
        validateWeight,
        validateRadioFormItem,
        benchmarkTree,
        benchmarkStrategyList,
      };
    },
    methods: {
      onCloseModal() {
        this.closeModal();
        this.clearPrams();
      },
      onClickSubmit() {
        this.formRef.validateFields().then(() => {
          useMessage().createConfirm({
            iconType: 'info',
            title: '提示',
            content: '确定要提交吗？',
            onOk: () => {
              this.saveBenchmark();
            },
            onCancel() {},
          });
        });
      },
      preparePrams() {
        let params = {
          benchmarkId: this.id,
          benchmarkVersion: this.version,
          indicatorId: this.evaluationCriteriaTreeNode.indicatorId,
          benchmarkName: this.name,
          guidance: this.guidance,
          inputScoreSymbolId: this.inputScoreSymbol?.id,
          calcMethod: this.benchmarkDefinition?.calcMethod,
          saveInputBenchmarkEm: null as {} | null,
          saveGradeBenchmarkEm: null as {} | null,
          saveAggregatedBenchmarkEm: null as {} | null,
        };
        if (this.benchmarkDefinition?.calcMethod === 'AggregatedBenchmark') {
          params.saveAggregatedBenchmarkEm = {
            weightNodeList: this.weightNodeList,
          };
        } else if (this.benchmarkDefinition?.calcMethod === 'GradeBenchmark') {
        } else {
          params.saveInputBenchmarkEm = {
            numericMinScore: this.numericMinScore,
            numericMaxScore: this.numericMaxScore,
            limitedStringOptions: this.limitedStringOptions,
            args: {
              options_value: this.args.optionsValue,
            },
          };
        }
        return params;
      },
      saveBenchmark() {
        const params = this.preparePrams();
        this.fullScreenLoading = true;
        apiSaveBenchmark(params)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '保存成功',
              });
              this.$emit('saveSuccess');
              this.onCloseModal();
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch(() => {
            useMessage().createErrorNotification({
              message: '错误',
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
          })
          .finally(() => {
            this.fullScreenLoading = false;
          });
      },
      changeBenchmarkDefinition(checkedValue) {
        console.log(checkedValue);
        this.scoreSymbolName = null;
        this.inputScoreSymbol = null;
        this.limitedStringOptions = null;
        this.getScoreSymbolList(checkedValue.inputScoreSymbolType);
      },

      changeScoreSymbolName() {
        this.inputScoreSymbol = this.scoreSymbolName.optionsList[0];
        if (this.scoreSymbolName.valueType === 'STRING') {
          this.numericMinScore = null;
          this.numericMaxScore = null;
        } else {
          this.limitedStringOptions = [];
        }
        if (this.benchmarkDefinition.calcMethod === 'AggregatedBenchmark') {
          this.getBenchmarkListByIndicatorId();
          this.getChildNodeBenchmarkListByIndicatorId();
        }
      },
      changeScoreSource() {},
      changeWeight() {
        let weightNodeList = [];
        this.benchmarkList.forEach((benchmark, index) => {
          if (benchmark.weight) {
            weightNodeList.push({
              sourceBenchmarkId: benchmark.id,
              weight: benchmark.weight,
              seq: index + 1,
            });
          }
        });
        this.weightNodeList = weightNodeList;
      },
    },
  });
</script>

<style scoped lang="less">
  .edit-benchmark-modal {
    ::v-deep(.ant-modal) {
      max-width: calc(100vw) !important;

      .scroll-container .scrollbar__wrap {
        margin-bottom: 0 !important;
      }

      .scrollbar__view {
        //height: calc(100% - 50px);
        height: 60vh;
        overflow: hidden;
      }

      .ant-modal-body {
        height: 100%;
        //background-color: #f0f2f5;
        .scrollbar {
          padding: 0 !important;
          overflow: hidden;
        }
      }

      .content {
        //height: 100%;
        height: 60vh;
        //background-color: #00acc1;
        overflow-y: auto;
        padding: 16px;
      }
    }
  }

  ::v-deep(.ant-card-body) {
    padding: 0 24px;
  }
</style>
