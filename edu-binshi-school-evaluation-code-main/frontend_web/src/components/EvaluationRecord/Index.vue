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
          <span v-if="effectedName"> 评价对象：{{ effectedName }} </span>
        </div>
        <div class="title-button">
          <Tooltip v-if="currentRoleCode !== 'STUDENT'">
            <template #title>
              合计数据需等所有子项评价完成后才会显示，如需查看合计数据，请先评价所有子项后点击刷新按钮。
            </template>
            <Icon icon="icon-park-outline:tips-one" size="18" />
          </Tooltip>
          <Button
            v-if="currentRoleCode !== 'STUDENT'"
            :iconSize="18"
            class="ant-btn-left-margin"
            color="success"
            preIcon="ci:refresh"
            title="刷新"
            @click="refresh"
            >刷新
          </Button>
          <Button
            :iconSize="18"
            class="ant-btn-left-margin"
            preIcon="material-symbols:close"
            title="关闭"
            @click="onCloseModel"
            >关闭
          </Button>
        </div>
      </template>
      <div style="height: 100%; overflow: hidden">
        <Card class="evaluation-record-tree-card">
          <div class="md:w-full h-full tree-container">
            <img
              src="../../assets/svg/treeEmpty.svg"
              width="300"
              v-if="treeData.length === 0 && !loading"
              style="margin: 0 auto"
              alt="empty"
            />
            <Tree
              v-else-if="treeData.length > 0"
              :treeData="treeData"
              :loading="loading"
              :defaultExpandAll="true"
              :clickRowToExpand="false"
              :selectable="false"
              :delete-default-height="true"
              style="overflow-x: auto; white-space: no-wrap"
              @expand="onExpand"
            >
              <template #switcherIcon="{ switcherCls, expanded }">
                <MinusSquareOutlined v-if="expanded" :class="[switcherCls, 'open-switcher-icon']" />
                <PlusSquareOutlined v-else :class="[switcherCls, 'close-switcher-icon']" />
              </template>
              <template #title="item">
                <div class="tree-title-wrapper">
                  <div
                    :class="[
                      'tree-title',
                      'inline-flex-center',
                      selectedKeys.includes(item.key) ? 'tree-title-selected' : '',
                    ]"
                  >
                    <div class="node-name">
                      <SvgIcon v-if="item.tagCode === 'VARIABLE'" name="xIcon" size="18px" />
                      <SvgIcon v-else-if="item.tagCode === 'CONSTANT'" name="nIcon" size="18px" />
                      <Icon v-else icon="ph:ruler-bold" color="#58a76e" size="20px" />
                      <span
                        class="node-name-span"
                        :style="item.code === '' ? '' : 'font-size: 20px; font-weight: bold'"
                        >{{ item.name }}</span
                      >
                    </div>
                    <div
                      v-if="item.benchmarkDisplayList && item.benchmarkDisplayList.length > 0"
                      class="benchmark-div inline-flex-center"
                    >
                      <Icon icon="material-symbols:label-outline" color="#aeaeaf" />
                      <div
                        v-for="benchmark in item.benchmarkDisplayList"
                        :key="benchmark.benchmarkId"
                        class="benchmark-edit-span inline-flex-center"
                      >
                        <div v-if="!benchmark.canView">
                          <SoftTag
                            class="benchmark-tag translate-and-shadow"
                            :color="'#94A3B8'"
                            :backgroundColor="'#E5E7EB'"
                          >
                            {{ benchmark.benchmarkName }}：
                            <span
                              v-if="
                                currentRoleCode !== 'STUDENT' &&
                                (benchmark.scoreResult || benchmark.scoreResult === 0)
                              "
                            >
                              {{ benchmark.scoreResult }}
                            </span>
                            <span v-else> -- </span>
                            （<SvgIcon
                              size="13"
                              :name="benchmark.scoreSymbolCode.toLocaleLowerCase()"
                            />）
                          </SoftTag>
                        </div>
                        <div v-else-if="canEvaluation === false">
                          <SoftTag
                            class="benchmark-tag translate-and-shadow"
                            :color="
                              benchmarkStrategySourceCategory[benchmark.benchmarkSourceCategory]
                                .color
                            "
                            :backgroundColor="
                              benchmarkStrategySourceCategory[benchmark.benchmarkSourceCategory]
                                .backgroundColor
                            "
                          >
                            {{ benchmark.benchmarkName }}：
                            <span v-if="benchmark.scoreResult || benchmark.scoreResult === 0">
                              {{ benchmark.scoreResult }}
                            </span>
                            <span v-else> -- </span>
                            （<SvgIcon
                              size="13"
                              :name="benchmark.scoreSymbolCode.toLocaleLowerCase()"
                            />）
                          </SoftTag>
                        </div>
                        <div v-else>
                          <Popover
                            :key="benchmark.benchmarkId"
                            :visible="needInputDict[benchmark.benchmarkId].displayPopover"
                            trigger="click"
                            :getPopupContainer="(trigger) => trigger.parentNode"
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
                                :autoFocusFirstItem="true"
                              >
                                <div v-if="benchmark.scoreSymbolValueType === 'NUM'">
                                  <FormItem name="numericScore" style="min-width: 280px">
                                    <InputNumber
                                      v-if="needInputDict[benchmark.benchmarkId].displayPopover"
                                      ref="inputRefNumericScore"
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
                                          saveBenchmarkInputScoreLog(
                                            needInputDict[benchmark.benchmarkId],
                                          )
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
                                          saveBenchmarkInputScoreLog(
                                            needInputDict[benchmark.benchmarkId],
                                          )
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

                            <SoftTag
                              class="benchmark-tag"
                              style="cursor: pointer"
                              :color="
                                benchmarkStrategySourceCategory[benchmark.benchmarkSourceCategory]
                                  .color
                              "
                              :backgroundColor="
                                benchmarkStrategySourceCategory[benchmark.benchmarkSourceCategory]
                                  .backgroundColor
                              "
                              @click="handlePopover(needInputDict[benchmark.benchmarkId])"
                            >
                              {{ benchmark.benchmarkName }}：
                              <span
                                v-if="
                                  needInputDict[benchmark.benchmarkId].scoreResult ||
                                  needInputDict[benchmark.benchmarkId].scoreResult === 0
                                "
                              >
                                {{ needInputDict[benchmark.benchmarkId].scoreResult }}
                              </span>
                              <span v-else> -- </span>
                              （<SvgIcon
                                size="13"
                                :name="benchmark.scoreSymbolCode.toLocaleLowerCase()"
                              />）
                            </SoftTag>
                          </Popover>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
            </Tree>
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
  import { Card, Form, Popover, Select, Tree, InputNumber, Tooltip } from 'ant-design-vue';
  import imgEmpty from '/@/assets/images/empty.png';
  import { Loading } from '/@/components/Loading';
  import { apiGetEvaluationRecordTree } from '/@/api/evaluationRecord/evaluationRecord';
  import { ScoreSymbolValueTypeEnum } from '/@/enums/scoreSymbolEnum';
  import { apiUpdateInputScoreLog } from '/@/api/inputScoreLog/inputScoreLog';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { BenchmarkInputNodeItem, EvaluationCriteriaTreeItem, FormState } from './data';
  import { UserInfo } from '/#/store';
  import { useUserStore } from '/@/store/modules/user';
  import { MinusSquareOutlined, PlusSquareOutlined } from '@ant-design/icons-vue';
  import { Icon, SvgIcon } from '/@/components/Icon';
  import { SoftTag } from '/@/components/Tag';
  import { benchmarkStrategySourceCategory } from '/@/utils/helper/common';

  export default defineComponent({
    components: {
      Tooltip,
      SoftTag,
      PlusSquareOutlined,
      MinusSquareOutlined,
      Form,
      FormItem: Form.Item,
      Select,
      SelectOption: Select.Option,
      InputNumber,
      Tree,
      Popover,
      BasicModal,
      Loading,
      Button,
      Card,
      Icon,
      SvgIcon,
    },
    emits: ['register', 'refresh'],
    setup() {
      const userStore = useUserStore();
      const userInfo: UserInfo = userStore.getUserInfo;
      const currentRoleCode = ref<string>(userInfo.currentRole.code);

      const formRef = ref([]);
      const inputRefNumericScore = ref();
      const { refreshPage } = useTabs();
      const expandedKeys = ref<string[]>([]);
      const selectedKeys = ref([]);

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
      const needInputDict = ref<{ [key: string]: BenchmarkInputNodeItem }>({});

      const judgeUsedPopover = ref<boolean>(false);

      const [register, { closeModal }] = useModalInner((data) => {
        treeData.splice(0, treeData.length);
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
                code: 'root',
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
          t.code = t.code ? t.code : '';
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
        inputValue,
        formRules,
        needInputDict,
        formRef,
        judgeUsedPopover,
        canEvaluation,
        currentRoleCode,
        inputNumberStep,
        selectedKeys,
        expandedKeys,
        benchmarkStrategySourceCategory,
        getEvaluationRecordTree,
        inputRefNumericScore,
      };
    },

    methods: {
      refresh() {
        this.loading = true;
        this.treeData.splice(0, this.treeData.length);
        this.getEvaluationRecordTree(this.params);
      },
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
        this.formRef.splice(0, this.formRef.length);
      },
      handlePopover(benchmark) {
        setTimeout(() => {
          if (this.inputValue.scoreSymbolValueType === 'NUM') {
            this.$refs.inputRefNumericScore[0].focus();
          }
        }, 10);
        if (this.judgeUsedPopover) {
          for (const [_key, value] of Object.entries(this.needInputDict)) {
            value.displayPopover = false;
          }
        }
        if (benchmark.scoreSymbolNumericPrecision) {
          this.inputNumberStep = this.getDecimal(benchmark.scoreSymbolNumericPrecision);
        }
        benchmark.displayPopover = true;
        this.judgeUsedPopover = true;
        console.log(this.initInputValue(benchmark));
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
        if (this.inputValue.scoreSymbolValueType === 'NUM') {
          this.formRef[this.formRef.length - 1].validateFields().then(() => {
            this.onSaveBenchmarkInputScoreLog(benchmark, inputScoreLogParams);
          });
        } else {
          if (!this.inputValue.stringScore) {
            benchmark.displayPopover = false;
          } else {
            this.onSaveBenchmarkInputScoreLog(benchmark, inputScoreLogParams);
          }
        }
      },
      onSaveBenchmarkInputScoreLog(benchmark, inputScoreLogParams) {
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
      },
      onExpand(keys, _event) {
        this.expandedKeys = keys;
      },
      onSelect(_selectedKeys) {
        this.selectedKeys = _selectedKeys;
      },
    },
  });
</script>

<style lang="less" scoped>
  .title-tips {
    text-align: center;
    display: inline-block;
    width: calc(100vw - 15em);
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

  .evaluation-record-tree {
    ::v-deep(.ant-modal) {
      max-width: calc(100vw) !important;
    }

    ::v-deep(.vben-tree .ant-tree-node-content-wrapper) {
      // tree 横向滚动自适应
      width: 100%;
      flex: 0 0 auto;
    }

    ::v-deep(.scrollbar__view) {
      height: 100%;
    }

    ::v-deep(.ant-tree) {
      height: 100%;
    }

    ::v-deep(.ant-tree-title) {
      // tree 节点换行
      position: relative !important;
      display: flex;
      //white-space: normal !important;
    }

    ::v-deep(.ant-tree-switcher) {
      align-items: center;
      display: inline-flex;
      justify-content: flex-end;
    }

    ::v-deep(.ant-tree-switcher_close) {
      svg {
        transform: rotate(0deg);
      }
    }

    .open-switcher-icon {
      margin-right: 8px;
      justify-content: center;
      align-items: center;
      margin-left: 2px;
      font-size: 18px;
    }

    .close-switcher-icon {
      margin-right: 8px;
      justify-content: center;
      align-items: center;
      margin-left: 2px;
      font-size: 18px;
      transform: rotate(180deg);
    }

    ::v-deep(.ant-tree-treenode.dragging::after) {
      border: none !important;
    }

    ::v-deep(.ant-tree-node-content-wrapper:hover) {
      background-color: white;
    }

    ::v-deep(.ant-tree-list) {
      height: 100%;
      padding: 5px 4% 50px 2.5%;
    }

    ::v-deep(.tree-title:hover) {
      //border: 0 0 0 1px #5248dd;
      box-shadow: 0 0 0 1px #5248dd;
    }

    ::v-deep(.ant-tree-switcher-noop) {
      visibility: hidden;
    }
  }

  .evaluation-record-tree-card {
    width: 100%;
    height: 100%;
    //border-radius: 8px;
  }

  .tree-title-wrapper {
    position: relative;
    width: 100%; /* 根据需要调整 */
    height: 40px;
  }

  .tree-title {
    width: 100%;
    height: auto;
    padding: 0 10px;
    background: #f7f7f9;
    border-radius: 8px;
    top: 0;
    left: 0;
    transition: transform 0.3s, box-shadow 0.3s;
    z-index: 1;
    overflow: hidden;
    white-space: nowrap;
  }

  .node-name {
    display: inline-flex;
    margin: 0 10px 0 0;
    height: 100%;
    align-items: center;
    white-space: pre-wrap;
  }

  .node-name-span {
    margin: 7px;
    height: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .benchmark-edit-span {
    height: 100%;
  }

  .benchmark-div {
    height: 100%;
    background: white;
    border-radius: 10px;
    padding: 0 10px;
    border: 1px solid #efeff0;
  }

  .benchmark-tag {
    margin: 3px 5px;
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

  ::v-deep([ant-click-animating-without-extra-node='true']::after) {
    display: none;
  }
</style>
