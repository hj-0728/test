<template>
  <div ref="evaluationRecordTree" class="evaluation-record-tree">
    <Loading :loading="loading" style="z-index: 9999" />
    <BasicModal
      v-bind="$attrs"
      @register="register"
      :destroyOnClose="true"
      :canFullscreen="false"
      :defaultFullscreen="true"
      :maskClosable="false"
      :footer="null"
      :closable="false"
      :centered="true"
      :getContainer="() => $refs.evaluationRecordTree"
      width="100%"
      :afterClose="afterClose"
    >
      <template #title>
        <div class="title-tips">
          <span v-if="effectedName">
            {{ effectedName }}
          </span>
        </div>
        <div class="title-button">
          <Button :iconSize="18" preIcon="material-symbols:close" title="关闭" @click="onCloseModel"
            >关闭
          </Button>
        </div>
      </template>
      <div>
        <Card class="evaluation-record-tree-card">
          <div class="md:w-full h-full tree-container">
            <BasicTree
              v-if="treeData.length"
              :treeData="treeData"
              :defaultExpandAll="true"
              :clickRowToExpand="false"
              :selectable="false"
            >
              <template #title="item">
                {{ item.name }}
                <div v-for="benchmark in item.benchmarkDisplayList" :key="benchmark.benchmarkId">
                  <div v-if="benchmark.canView === false">
                    <Tag style="margin-left: 50px" color="gray">
                      {{ benchmark.benchmarkName }}（{{ benchmark.scoreSymbolName }}）
                      <span v-if="currentRoleCode !== 'STUDENT' && benchmark.scoreResult">
                        ：{{ benchmark.scoreResult }}
                      </span>
                    </Tag>
                  </div>
                  <div v-else-if="canEvaluation === false">
                    <Tag
                      style="margin-left: 50px"
                      :color="
                        colorData[benchmark['fillerCalcMethod']]
                          ? colorData[benchmark['fillerCalcMethod']]
                          : ''
                      "
                    >
                      {{ benchmark.benchmarkName }}（{{ benchmark.scoreSymbolName }}）：
                      {{ needInputDict[benchmark.benchmarkId].scoreResult }}
                    </Tag>
                  </div>
                  <div v-else>
                    <Popover
                      :key="benchmark.benchmarkId"
                      :visible="needInputDict[benchmark.benchmarkId].displayPopover"
                      trigger="click"
                    >
                      <template #title>
                        <span style="font-size: 16px; font-weight: bold">{{
                          benchmark.benchmarkName
                        }}</span>
                        <span v-if="inputValue.scoreSymbolValueType === 'NUM'">
                          （范围：[{{ inputValue.numericMinScore }},
                          {{ inputValue.numericMaxScore }}]）
                        </span>
                      </template>
                      <template #content>
                        <Form
                          ref="formRef"
                          :model="inputValue"
                          name="basic"
                          autocomplete="off"
                          layout="horizontal"
                          :rules="formRules"
                        >
                          <div v-if="benchmark.scoreSymbolValueType === 'NUM'">
                            <FormItem name="numericScore" style="min-width: 200px">
                              <InputNumber
                                v-model:value="inputValue.numericScore"
                                style="min-width: calc(100% - 70px)"
                                :min="inputValue.numericMinScore"
                                :max="inputValue.numericMaxScore"
                                :precision="inputValue.scoreSymbolNumericPrecision"
                                :step="inputNumberStep"
                              />
                              <div class="btn-content">
                                <Button
                                  type="primary"
                                  style="width: 28px; height: 28px"
                                  color="success"
                                  :iconSize="18"
                                  preIcon="ant-design:check-outlined"
                                  size="small"
                                  @click="
                                    saveBenchmarkInputScoreLog(needInputDict[benchmark.benchmarkId])
                                  "
                                />
                                <Button
                                  type="primary"
                                  color="error"
                                  :iconSize="18"
                                  preIcon="ant-design:close-outlined"
                                  size="small"
                                  @click="hidePopover(needInputDict[benchmark.benchmarkId])"
                                  style="width: 28px; height: 28px; margin-left: 5px"
                                />
                              </div>
                            </FormItem>
                          </div>
                          <div v-else-if="benchmark.scoreSymbolValueType === 'STRING'">
                            <FormItem name="stringScore">
                              <div style="width: calc(100% - 70px)">
                                <Select v-model:value="inputValue.stringScore">
                                  <SelectOption
                                    v-for="[
                                      id,
                                      limitedString,
                                    ] of benchmark.limitedStringOptions.entries()"
                                    :value="limitedString"
                                    :key="'select' + id"
                                  >
                                    {{ limitedString }}
                                  </SelectOption>
                                </Select>
                              </div>
                              <div class="btn-content">
                                <Button
                                  type="primary"
                                  style="width: 28px; height: 28px"
                                  color="success"
                                  :iconSize="18"
                                  preIcon="ant-design:check-outlined"
                                  size="small"
                                  @click="
                                    saveBenchmarkInputScoreLog(needInputDict[benchmark.benchmarkId])
                                  "
                                />
                                <Button
                                  type="primary"
                                  color="error"
                                  :iconSize="18"
                                  preIcon="ant-design:close-outlined"
                                  size="small"
                                  @click="hidePopover(needInputDict[benchmark.benchmarkId])"
                                  style="width: 28px; height: 28px; margin-left: 5px"
                                />
                              </div>
                            </FormItem>
                          </div>
                        </Form>
                      </template>
                      <Tag
                        style="margin-left: 50px; cursor: pointer"
                        :color="
                          colorData[benchmark['fillerCalcMethod']]
                            ? colorData[benchmark['fillerCalcMethod']]
                            : ''
                        "
                        @click="handlePopover(needInputDict[benchmark.benchmarkId])"
                      >
                        {{ benchmark.benchmarkName }}（{{ benchmark.scoreSymbolName }}）：
                        {{ needInputDict[benchmark.benchmarkId].scoreResult }}
                      </Tag>
                    </Popover>
                  </div>
                </div>
              </template>
            </BasicTree>
          </div>
        </Card>
      </div>
    </BasicModal>
  </div>
</template>
<script lang="ts">
  import { defineComponent, reactive, ref, UnwrapRef } from 'vue';
  import { useTabs } from '/@/hooks/web/useTabs';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Button } from '/@/components/Button';
  import { Card, Form, Popover, Select, Tag, InputNumber } from 'ant-design-vue';
  import imgEmpty from '/@/assets/images/empty.png';
  import { Loading } from '/@/components/Loading';
  import { apiGetEvaluationRecordTree } from '/@/api/evaluationRecord/evaluationRecord';
  import { BasicTree } from '/@/components/Tree';
  import { ScoreSymbolValueTypeEnum } from '/@/enums/scoreSymbolEnum';
  import { apiUpdateInputScoreLog } from '/@/api/inputScoreLog/inputScoreLog';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { EvaluationCriteriaTreeItem, FormState } from './data';
  import { UserInfo } from '/#/store';
  import { useUserStore } from '/@/store/modules/user';

  export default defineComponent({
    components: {
      Form,
      FormItem: Form.Item,
      Select,
      SelectOption: Select.Option,
      InputNumber,
      BasicTree,
      Popover,
      Tag,
      BasicModal,
      Loading,
      Button,
      Card,
    },
    emits: ['register', 'refresh'],
    setup() {
      const colorData = ref({
        SelfBenchmark: 'blue',
        TeacherBenchmark: 'pink',
        HeadTeacherBenchmark: 'green',
        TeamCategoryBenchmark: 'purple',
        OtherClassmatesBenchmark: 'orange',
        GradeBenchmark: 'yellow',
        AggregatedBenchmark: 'red',
      });
      const userStore = useUserStore();
      const userInfo: UserInfo = userStore.getUserInfo;
      const currentRoleCode = ref<string>(userInfo.currentRole.code);

      const formRef = ref();
      const { refreshPage } = useTabs();

      const inputValue: UnwrapRef<FormState> = reactive({
        id: '',
        version: undefined,
        numericScore: undefined,
        stringScore: undefined,
        scoreSymbolValueType: undefined,
        scoreSymbolNumericPrecision: undefined,
        numericMinScore: undefined,
        numericMaxScore: undefined,
      });
      const inputNumberStep = ref<number>(1);

      const emptyDescription = ref<string | null>(null);
      const treeData = reactive<Array<EvaluationCriteriaTreeItem>>([]);
      const effectedName = ref<string | null>(null);
      const canEvaluation = ref<boolean | null>(null);
      const params = reactive({
        evaluationCriteriaId: null,
        evaluationAssignmentId: null,
        evaluationCriteriaPlanId: null,
      });
      const loading = ref(false);
      const refreshKey = ref(new Date().getTime());
      const needInputDict = ref({});

      const judgeUsedPopover = ref<boolean>(false);

      const [register, { closeModal }] = useModalInner((data) => {
        treeData.splice(0, 1);
        params.evaluationCriteriaId = data.evaluationCriteriaId;
        params.evaluationAssignmentId = data.evaluationAssignmentId;
        params.evaluationCriteriaPlanId = data.evaluationCriteriaPlanId;
        effectedName.value = data.effectedName;
        canEvaluation.value = data.canEvaluation;
        loading.value = true;
        getEvaluationRecordTree(params);
      });
      const getEvaluationRecordTree = (params) => {
        apiGetEvaluationRecordTree(params)
          .then((res) => {
            if (res.code === 200) {
              needInputDict.value = res.data.needInputDict;
              treeData.push({
                id: res.data.treeData[0].evaluationCriteriaId,
                name: res.data.treeData[0].evaluationCriteriaName,
                children: res.data.treeData,
              });
              expandTree(treeData);
            } else {
              emptyDescription.value = res.error.message;
            }
          })
          .finally(() => {
            loading.value = false;
          });
      };

      const expandTree = (tree) => {
        tree.map((t) => {
          t.key = t.id;
          t.title = t.name;
          if (t.children && t.children.length > 0) {
            expandTree(t.children);
          }
        });
      };

      function countDecimals(value) {
        const valueSplit = value.toString().split('.');
        if (valueSplit.length > 1) {
          return valueSplit[1].length;
        }
        return 0;
      }

      const validateNumericScore = async (_rule, value) => {
        if (value === null || value === '') {
          return Promise.reject('请输入分数');
        }
        if (countDecimals(value) > inputValue.scoreSymbolNumericPrecision) {
          return Promise.reject(
            '填写的精度超过了规定，规定的精度为：' + inputValue.scoreSymbolNumericPrecision,
          );
        }
        if (value > inputValue.numericMaxScore) {
          return Promise.reject('最高分为：' + inputValue.numericMaxScore);
        }
        if (value < inputValue.numericMinScore) {
          return Promise.reject('最低分为：' + inputValue.numericMinScore);
        }
        return Promise.resolve();
      };

      const formRules = {
        numericScore: [
          {
            required: true,
            trigger: ['change', 'blur'],
            validator: validateNumericScore,
            whitespace: true,
          },
          /*{
            min: inputValue.numericMinScore,
            max: inputValue.numericMaxScore,
            message:
              '范围是[' + inputValue.numericMinScore + ',' + inputValue.numericMaxScore + ']',
            trigger: 'blur',
          },*/
        ],
      };
      return {
        register,
        closeModal,
        refreshPage,
        params,
        emptyDescription,
        loading,
        imgEmpty,
        effectedName,
        treeData,
        refreshKey,
        colorData,
        inputValue,
        formRules,
        needInputDict,
        formRef,
        judgeUsedPopover,
        canEvaluation,
        currentRoleCode,
        inputNumberStep,
      };
    },

    methods: {
      getDecimal(n) {
        return 1 / Math.pow(10, n);
      },
      initInputValue(benchmark) {
        this.inputValue.id = benchmark.inputScoreLogId;
        this.inputValue.version = benchmark.inputScoreLogVersion;
        this.inputValue.numericScore = benchmark.numericScore;
        this.inputValue.stringScore = benchmark.stringScore;
        this.inputValue.scoreSymbolValueType = benchmark.scoreSymbolValueType;
        this.inputValue.scoreSymbolNumericPrecision = benchmark.scoreSymbolNumericPrecision;
        this.inputValue.numericMaxScore = benchmark.numericMaxScore;
        this.inputValue.numericMinScore = benchmark.numericMinScore;
      },
      hidePopover(benchmark) {
        benchmark.displayPopover = false;
        this.judgeUsedPopover = false;
      },
      handlePopover(benchmark) {
        if (this.judgeUsedPopover) {
          for (const [key, value] of Object.entries(this.needInputDict)) {
            value.displayPopover = false;
          }
        }
        if (benchmark.scoreSymbolNumericPrecision) {
          this.inputNumberStep = this.getDecimal(benchmark.scoreSymbolNumericPrecision);
        }
        benchmark.displayPopover = true;
        this.judgeUsedPopover = true;
        this.initInputValue(benchmark);
      },
      onCloseModel() {
        this.emptyDescription = null;
        this.effectedName = null;
        this.closeModal();
      },
      afterClose() {
        this.$emit('refresh');
      },
      saveBenchmarkInputScoreLog(benchmark) {
        const inputScoreLogParams = {
          id: this.inputValue.id,
          version: this.inputValue.version,
          numericScore: this.inputValue.numericScore,
          stringScore: this.inputValue.stringScore,
          evaluationCriteriaPlanId: this.params.evaluationCriteriaPlanId,
        };
        this.formRef[this.formRef.length - 1].validateFields().then(() => {
          apiUpdateInputScoreLog(inputScoreLogParams)
            .then((res) => {
              if (res.code === 200) {
                benchmark.inputScoreLogVersion++;
                benchmark.numericScore = this.inputValue.numericScore;
                benchmark.stringScore = this.inputValue.stringScore;
                benchmark.displayPopover = false;
                if (benchmark.scoreSymbolValueType === ScoreSymbolValueTypeEnum.NUM) {
                  benchmark.scoreResult = this.inputValue.numericScore;
                } else {
                  benchmark.scoreResult = this.inputValue.stringScore;
                }
              } else {
                useMessage().createErrorNotification({
                  message: '错误',
                  description: res.error.message,
                });
              }
            })
            .finally(() => {
              this.formRef.splice(0, 1);
              // console.log(benchmark);
            });
        });
      },
    },
  });
</script>

<style lang="less" scoped>
  .evaluation-record-tree {
    ::v-deep(.ant-modal) {
      max-width: calc(100vw) !important;
    }
  }

  .title-tips {
    text-align: center;
    display: inline-block;
    width: calc(100vw - 10em);
  }

  .title-button {
    display: inline-block;
  }

  :deep(.ant-modal-wrap) {
    overflow: hidden;
  }

  :deep(.ant-modal-body) {
    background-color: #e9eaeb;
    overflow: auto !important;
  }

  :deep(.ant-modal-header) {
    cursor: auto !important;
  }

  .evaluation-record-tree-card {
    width: 100%;
    //border-radius: 8px;
  }

  :deep(.ant-empty-description) {
    margin-top: 40px;
  }

  .btn-content {
    display: flex;
    height: 100%;
    align-items: center;
    margin-left: 5px;
    position: absolute;
    top: 0;
    right: 0;
  }

  ::v-deep(.vben-tree .ant-tree-node-content-wrapper .ant-tree-title) {
    width: fit-content;
  }

  ::v-deep(.ant-tree-title) {
    position: relative !important;
    white-space: normal !important;
  }

  ::v-deep(.ant-tree .ant-tree-node-content-wrapper) {
    cursor: auto;
  }
</style>
