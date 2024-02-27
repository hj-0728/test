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
      width="80vw"
    >
      <template #title>
        <Icon icon="ri:file-list-2-line" />
        <span> {{ readonly ? '查看' : modalCategory === 'ADD' ? '添加' : '编辑' }}评价分类 </span>
      </template>
      <!--      <Loading :loading="fullScreenLoading" :absolute="false" />-->
      <Skeleton :loading="fullScreenLoading" style="margin: 100px">
        <div class="content">
          <Row>
            <Col :span="3" />
            <Col :span="18">
              <Alert :type="modalCategory === 'ADD' ? 'success' : 'info'">
                <template #description>
                  <span v-if="modalCategory === 'ADD'">
                    为评价项 <SvgIcon name="leftQuotation" size="16" /><span
                      style="font-weight: bolder; font-size: 20px"
                      >{{ evaluationCriteriaTreeNode?.name }}</span
                    ><SvgIcon name="rightQuotation" size="16" />添加评价分类
                  </span>
                  <span v-else>
                    {{ readonly ? '查看' : '编辑' }}评价项<SvgIcon
                      name="leftQuotation"
                      size="16"
                    /><span style="font-weight: bolder; font-size: 20px">{{
                      evaluationCriteriaTreeNode?.name
                    }}</span
                    ><SvgIcon name="rightQuotation" size="16" />的评价分类
                  </span>
                </template>
              </Alert>
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
            <FormItem
              name="name"
              label="名称"
              :rules="[
                {
                  required: true,
                  trigger: ['blur', 'change'],
                  whitespace: true,
                },
              ]"
            >
              <span v-if="readonly">{{ name }}</span>
              <TextArea
                v-else
                v-model:value="name"
                show-count
                :readonly="readonly"
                :maxlength="10"
                :autoSize="{ minRows: 2, maxRows: 4 }"
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
              <span v-if="readonly">
                <span v-if="guidance">{{ guidance }}</span>
                <span v-else>暂无内容</span>
              </span>
              <TextArea
                v-else
                v-model:value="guidance"
                show-count
                :maxlength="255"
                :autoSize="{ minRows: 2, maxRows: 4 }"
                :readonly="readonly"
              />
            </FormItem>

            <!--            <FormItem-->
            <!--              name="selectTag"-->
            <!--              label="标签"-->
            <!--              :rules="{-->
            <!--                required: true,-->
            <!--                trigger: ['blur'],-->
            <!--                validator: validateSelectTag,-->
            <!--              }"-->
            <!--            >-->
            <!--              <Input v-if="readonly" v-model:value="JSON.parse(selectTag).name" readonly />-->
            <!--              <Select-->
            <!--                v-else-->
            <!--                ref="select"-->
            <!--                v-model:value="selectTag"-->
            <!--                style="width: 100%"-->
            <!--                placeholder="请选择标签"-->
            <!--                show-search-->
            <!--                allowClear-->
            <!--                mode="combobox"-->
            <!--                :filter-option="false"-->
            <!--                :autoClearSearchValue="true"-->
            <!--                @search="onSearchTag"-->
            <!--                @change="onChangeTag"-->
            <!--              >-->
            <!--                <SelectOption-->
            <!--                  v-for="option in computedTagList"-->
            <!--                  :key="option.id"-->
            <!--                  :value="JSON.stringify(option)"-->
            <!--                >-->
            <!--                  {{ option.name }}-->
            <!--                </SelectOption>-->
            <!--              </Select>-->
            <!--            </FormItem>-->
            <FormItem
              name="benchmarkStrategy"
              label="评价策略"
              :rules="[
                {
                  required: true,
                  trigger: ['blur', 'change'],
                  validator: validateBenchmarkStrategy,
                },
              ]"
            >
              <Input
                v-if="readonly && benchmarkStrategy"
                v-model:value="JSON.parse(benchmarkStrategy).name"
                readonly
                style="width: 100%"
              />
              <Select
                v-if="!readonly"
                v-model:value="benchmarkStrategy"
                show-search
                placeholder="请选择评价策略"
                :filter-option="filterOption"
                :disabled="readonly"
                @change="changeBenchmarkStrategy"
              >
                <SelectOptGroup v-for="(source, index) in benchmarkStrategyList" :key="index">
                  <template #label>
                    <Icon
                      icon="ic:round-square"
                      :color="benchmarkStrategySourceCategory[source.sourceCategory].color"
                      size="10"
                    />
                    <span style="font-size: 12px; font-weight: bolder; margin-left: 5px"
                      >{{ source.sourceCategoryName }}类</span
                    >
                  </template>
                  <SelectOption
                    v-for="option in source.options"
                    :key="option.value"
                    :value="JSON.stringify(option)"
                  >
                    {{ option.name }}
                  </SelectOption>
                </SelectOptGroup>
              </Select>
            </FormItem>
            <FormItem name="category" label="类型：" :colon="false">
              <div>
                <RadioGroup
                  v-model:value="category"
                  :options="eventCategoryOptions"
                  @click="clearInput"
                />
              </div>
            </FormItem>

            <div>
              <component
                ref="scoreSymbolRef"
                v-if="benchmarkStrategy && JSON.parse(benchmarkStrategy).scoreSymbol"
                :is="getComponent(JSON.parse(benchmarkStrategy).scoreSymbol)"
                :formItem="JSON.parse(benchmarkStrategy).scoreSymbol"
                @get-benchmark-input-params="getBenchmarkInputParams"
                :key="refreshScoreSymbolKey"
                :readonly="readonly"
              />
              <component
                ref="componentsRef"
                v-for="formItem in componentList"
                :key="formItem"
                :is="getComponent(formItem)"
                :formItem="formItem"
                :readonly="readonly"
              />
            </div>
          </Form>
        </div>
      </Skeleton>
      <template #footer>
        <Button @click="onCloseModal" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
        <Button
          v-if="!readonly && modalCategory === 'EDIT'"
          :type="'primary'"
          color="error"
          preIcon="material-symbols:delete-outline"
          :iconSize="16"
          @click="toDeleteBenchmark()"
        >
          删除
        </Button>
        <Button
          v-if="!readonly"
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
  import { computed, defineComponent, nextTick, provide, reactive, ref, toRefs } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Loading } from '/@/components/Loading';
  import { Icon, SvgIcon } from '/@/components/Icon';
  import { Checkbox, Form, Input, Alert, Select, Row, Col, Skeleton, Radio } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import {
    apiDeleteBenchmark,
    apiGetBenchmarkDetail,
    apiSaveBenchmark,
  } from '/@/api/benchmark/benchmark';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import BenchmarkTransferSelect from '/@/views/evaluationCriteriaTree/components/BenchmarkTransferSelect.vue';
  import {
    apiGetBenchmarkStrategyInputParamsByStrategyId,
    apiGetBenchmarkStrategyList,
  } from '/@/api/benchmarkStrategy/benchmarkStrategy';
  import SingleChoiceFormItem from '/@/views/evaluationCriteriaTree/components/BenchmarkFormItem/SingleChoiceFormItem.vue';
  import IntegerFormItem from '/@/views/evaluationCriteriaTree/components/BenchmarkFormItem/IntegerFormItem.vue';
  import WeightFormItem from '/@/views/evaluationCriteriaTree/components/BenchmarkFormItem/WeightFormItem.vue';
  import TreeSelectFormItem from '/@/views/evaluationCriteriaTree/components/BenchmarkFormItem/TreeSelectFormItem.vue';
  import RangeValueFormItem from '/@/views/evaluationCriteriaTree/components/BenchmarkFormItem/RangeValueFormItem.vue';
  import StatsTreeFormItem from '/src/views/evaluationCriteriaTree/components/BenchmarkFormItem/StatsTreeFormItem.vue';
  import StatsCheckboxFormItem from '/src/views/evaluationCriteriaTree/components/BenchmarkFormItem/StatsCheckboxFormItem.vue';
  import { benchmarkStrategySourceCategory } from '/@/utils/helper/common';

  export default defineComponent({
    components: {
      BasicModal,
      Loading,
      Icon,
      Form,
      FormItem: Form.Item,
      TextArea: Input.TextArea,
      Button,
      Alert,
      Checkbox,
      BenchmarkTransferSelect,
      Select,
      SelectOption: Select.Option,
      SelectOptGroup: Select.OptGroup,
      SingleChoiceFormItem,
      IntegerFormItem,
      Row,
      Col,
      WeightFormItem,
      TreeSelectFormItem,
      RangeValueFormItem,
      StatsTreeFormItem,
      StatsCheckboxFormItem,
      SvgIcon,
      Skeleton,
      RadioGroup: Radio.Group,
    },
    emit: ['saveSuccess', 'saveError'],
    setup() {
      const formRef = ref();
      const fullScreenLoading = ref(false);
      const readonly = ref(false);
      const evaluationCriteriaTreeNode = ref();
      const modalCategory = ref('ADD');
      const errorMessage = ref(null);
      const category = ref('ADD_POINTS');
      const [register, { closeModal }] = useModalInner((data) => {
        modalCategory.value = data.modalCategory;
        clearPrams();
        // fullScreenLoading.value = true;
        evaluationCriteriaTreeNode.value = data.evaluationCriteriaTreeNode;
        if (modalCategory.value === 'EDIT') {
          params.id = data.benchmark.id;
          readonly.value = data.readonly;
        }
        getBenchmarkStrategy();
      });
      const params = reactive({
        id: null,
        name: null,
        version: 1,
        guidance: null,
      });
      // 当前节点可选择的benchmark Strategy List
      const benchmarkStrategyList = ref([]);
      // 当前选择的benchmark Strategy
      const benchmarkStrategy = ref();
      // 当前选择的benchmark componentList
      const componentList = ref([]);
      //
      const computedTagList = ref([]);
      //
      const selectTag = ref();
      const refreshScoreSymbolKey = ref(new Date().getTime());
      const limitedStringOptions = ref([]);
      const scoreSymbolRef = ref();
      const componentsRef = ref([]);
      const filterOption = (input: string, option: any) => {
        if (option.value) {
          return JSON.parse(option.value).name.toLowerCase().indexOf(input.toLowerCase()) >= 0;
        }
      };
      const clearPrams = () => {
        params.id = null;
        params.name = null;
        params.version = 1;
        params.guidance = null;
        // benchmarkStrategyList.value = [];
        benchmarkStrategy.value = null;
        componentList.value = [];
        // computedTagList.value = [];
        selectTag.value = null;
      };

      const getBenchmarkStrategy = () => {
        fullScreenLoading.value = true;
        apiGetBenchmarkStrategyList(params.id)
          .then((res) => {
            if (res.code === 200 && res.data.length > 0) {
              // 使用一个对象来分类
              let categorized = {};

              res.data.forEach((item) => {
                if (!categorized[item.sourceCategory]) {
                  categorized[item.sourceCategory] = {
                    options: [],
                    sourceCategoryName: item.sourceCategoryName,
                  };
                }
                categorized[item.sourceCategory].options.push(item);
              });

              // 将分类后的对象转换为数组
              benchmarkStrategyList.value = Object.keys(categorized).map((key) => ({
                sourceCategory: key,
                sourceCategoryName: categorized[key].sourceCategoryName,
                options: categorized[key].options,
              }));
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
          .finally(() => {
            if (params.id) {
              getBenchmarkDetail();
            } else {
              fullScreenLoading.value = false;
            }
          });
      };
      const validateBenchmarkStrategy = async (_rule) => {
        if (!benchmarkStrategy.value) {
          return Promise.reject('请选择评价策略');
        }
        return Promise.resolve();
      };
      const validateSelectTag = async (_rule) => {
        if (!selectTag.value) {
          return Promise.reject('请选择或输入标签');
        }
        return Promise.resolve();
      };
      const getBenchmarkDetail = () => {
        fullScreenLoading.value = true;
        apiGetBenchmarkDetail(params.id)
          .then((res) => {
            if (res.code === 200) {
              fullScreenLoading.value = false;
              params.id = res.data.id;
              params.name = res.data.name;
              params.version = res.data.version;
              params.guidance = res.data.guidance;
              //   准备选择的benchmarkStrategy
              const foundCategory = benchmarkStrategyList.value.find((category) =>
                category.options.some((item) => item.id === res.data.benchmarkStrategyId),
              );

              benchmarkStrategy.value = foundCategory
                ? JSON.stringify(
                    foundCategory.options.find((item) => item.id === res.data.benchmarkStrategyId),
                  )
                : null;
              // benchmarkStrategy.value = JSON.stringify(
              //   benchmarkStrategyList.value.find(
              //     (item) => item.id === res.data.benchmarkStrategyId,
              //   ),
              // );
              // 准备benchmarkStrategy
              if (res.data.benchmarkStrategySchema) {
                Object.keys(res.data.benchmarkStrategySchema).forEach((item) => {
                  componentList.value.push(res.data.benchmarkStrategySchema[item]);
                });
              }
              nextTick(() => {
                // 准备symbol及其嵌套子组件
                scoreSymbolRef.value?.setParams(res.data.benchmarkStrategyParams);
                componentList.value?.forEach((formItem, index) => {
                  componentsRef.value[index].setParams(res.data.benchmarkStrategyParams);
                });
              });
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
          .finally(() => {
            fullScreenLoading.value = false;
          });
      };
      const changeParams = (checkedList) => {
        limitedStringOptions.value = checkedList;
      };
      provide('changeParams', changeParams);
      provide(
        'limitedStringOptions',
        computed(() => {
          return limitedStringOptions.value;
        }),
      );
      provide(
        'test',
        computed(() => {
          return limitedStringOptions.value.length;
        }),
      );

      const eventCategoryOptions = ref([
        { label: '表扬', value: 'ADD_POINTS' },
        { label: '待改进', value: 'DEDUCT_POINTS' },
      ]);

      // getBenchmarkStrategy();
      return {
        formRef,
        fullScreenLoading,
        modalCategory,
        register,
        closeModal,
        params,
        ...toRefs(params),
        evaluationCriteriaTreeNode,
        clearPrams,
        benchmarkStrategyList,
        benchmarkStrategy,
        filterOption,
        componentList,
        validateBenchmarkStrategy,
        refreshScoreSymbolKey,
        selectTag,
        computedTagList,
        validateSelectTag,
        limitedStringOptions,
        componentsRef,
        scoreSymbolRef,
        readonly,
        benchmarkStrategySourceCategory,
        errorMessage,
        category,
        eventCategoryOptions,
      };
    },
    methods: {
      onCloseModal() {
        this.closeModal();
        this.clearPrams();
      },
      onClickSubmit() {
        if (this.errorMessage) {
          useMessage().createErrorNotification({
            message: '错误',
            description: this.errorMessage,
          });
          return;
        }
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
          tagOwnershipId: JSON.parse(this.benchmarkStrategy).tagOwnershipId,
          evaluationCriteriaId: this.evaluationCriteriaTreeNode.evaluationCriteriaId,
          benchmark: {
            id: this.id,
            version: this.version,
            indicatorId: this.evaluationCriteriaTreeNode.indicatorId,
            name: this.name,
            guidance: this.guidance,
            benchmarkStrategyId: JSON.parse(this.benchmarkStrategy).id,
            benchmarkStrategyParams: {},
          },
        };

        let inputParams = {};
        this.$refs.componentsRef?.forEach((compInstance) => {
          Object.assign(inputParams, compInstance.params);
        });
        inputParams = {
          ...this.$refs.scoreSymbolRef.getParams(),
          ...inputParams,
        };
        params.benchmark.benchmarkStrategyParams = inputParams;
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
              // setTimeout(() => {
              //   this.$emit('saveSuccess');
              // }, 1000);
              this.$emit('saveSuccess');
              this.onCloseModal();
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
              this.$emit('saveError');
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
      getComponent(formItem) {
        const type = formItem.componentType;
        switch (type) {
          case 'SINGLE_CHOICE':
            return 'SingleChoiceFormItem';
          case 'INTEGER':
            return 'IntegerFormItem';
          case 'WEIGHT':
            return 'WeightFormItem';
          case 'TREE_SELECT':
            return 'TreeSelectFormItem';
          case 'RANGE_VALUE':
            return 'RangeValueFormItem';
          case 'STATS_TREE':
            return 'StatsTreeFormItem';
          case 'STATS_CHOICE':
            return 'StatsCheckboxFormItem';
          default:
            return null; // 或者返回一个默认组件
        }
      },
      changeBenchmarkStrategy() {
        this.componentList = [];
        this.refreshScoreSymbolKey = new Date().getTime();
        // this.getBenchmarkInputParams();
        this.errorMessage = null;
      },
      getBenchmarkInputParams(scoreSymbolId) {
        const params = {
          strategyId: JSON.parse(this.benchmarkStrategy).id,
          scoreSymbolId: scoreSymbolId,
          indicatorId: this.evaluationCriteriaTreeNode.indicatorId,
          benchmarkId: this.id,
        };
        apiGetBenchmarkStrategyInputParamsByStrategyId(params)
          .then((res) => {
            if (res.code === 200 && res.data) {
              this.componentList = [];
              Object.keys(res.data).forEach((item) => {
                this.componentList.push(res.data[item]);
              });
              this.errorMessage = null;
            } else if (res.code !== 200) {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
              this.errorMessage = res.error.message;
            }
          })
          .catch((error) => {
            console.log(error);
            useMessage().createErrorNotification({
              message: '错误',
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
            this.errorMessage = ErrorNotificationEnum.networkExceptionMsg;
          })
          .finally(() => {});
      },

      toDeleteBenchmark() {
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: `确定要<text style="color: #f00; font-weight: bold">删除评价分类</text>【<text>${this.name}</text>】吗？`,
          onOk: () => {
            this.doDeleteBenchmark();
          },
          onCancel() {},
        });
      },
      doDeleteBenchmark() {
        const params = {
          benchmarkId: this.id,
          benchmarkVersion: this.version,
        };
        apiDeleteBenchmark(params)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '删除成功',
              });
              setTimeout(() => {
                this.$emit('saveSuccess');
              }, 1000);
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
            // this.loading = false;
          });
      },
      clearInput() {
        console.log('clearInput');
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
        height: 80vh;
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
        height: 80vh;
        //background-color: #00acc1;
        overflow-y: auto;
        padding: 16px;
      }
    }
  }

  ::v-deep(.ant-card-body) {
    padding: 0 24px;
  }

  .list-enter-active,
  .list-leave-active {
    transition: opacity 0.5s;
  }

  .list-enter,
  .list-leave-to {
    opacity: 0;
  }
</style>
