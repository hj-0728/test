<template>
  <div class="edit-evaluation-criteria-plan-modal" ref="editEvaluationCriteriaPlanModalRef">
    <BasicModal
      @register="register"
      :canFullscreen="false"
      :defaultFullscreen="false"
      :draggable="false"
      :destroyOnClose="true"
      :getContainer="() => $refs.editEvaluationCriteriaPlanModalRef"
      :closable="true"
      :centered="true"
      :maskClosable="false"
      @cancel="onCloseModal"
      width="60vw"
    >
      <template #title>
        <Icon icon="material-symbols:deployed-code-outline" />
        <span v-if="modalCategory === 'EDIT'"> 编辑评价标准计划 </span>
        <span v-if="modalCategory === 'ADD'"> 添加评价标准计划 </span>
        <span v-if="modalCategory === 'CHECK'"> 查看评价标准计划 </span>
      </template>
      <Loading
        :loading="
          fullScreenLoading || periodCategoryLoading || periodLoading || evaluationCriteriaLoading
        "
        :absolute="false"
      />
      <div class="steps" v-if="modalCategory !== 'CHECK'">
        <Steps :current="currentStep">
          <Step v-for="(title, index) in stepsTitle" :key="index" :title="title" />
        </Steps>
      </div>
      <div class="content">
        <Form
          v-show="currentStep === 0"
          :model="params"
          name="form"
          autocomplete="off"
          ref="formRef"
          layout="horizontal"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          :rules="formRules"
          style="margin-top: 20px"
        >
          <FormItem name="evaluationCriteriaId" label="评价标准：" :colon="false">
            <span v-if="modalCategory === 'CHECK'">{{ evaluationCriteriaName }}</span>
            <Select
              ref="select"
              v-else
              v-model:value="evaluationCriteriaId"
              style="width: 100%"
              :options="
                evaluationCriteriaParams.searchText
                  ? evaluationCriteriaSearchList
                  : evaluationCriteriaList
              "
              @change="evaluationCriteriaChange"
              :fieldNames="{ label: 'name', value: 'id' }"
              :maxTagCount="1"
              :maxTagTextLength="5"
              placeholder="选择评价标准进行过滤"
              show-search
              :filter-option="false"
              allowClear
              :disabled="
                (evaluationCriteriaPlan?.status === 'PUBLISHED' && !(modalCategory === 'ADD')) ||
                modalCategory === 'CHECK'
              "
              @search="searchEvaluationCriteria"
              :autoClearSearchValue="false"
            />
          </FormItem>
          <FormItem name="name" label="名称：" :colon="false">
            <span v-if="modalCategory === 'CHECK'">{{ name }}</span>
            <TextArea
              v-else
              v-model:value="name"
              show-count
              :maxlength="255"
              placeholder="输入名称"
              :disabled="modalCategory === 'CHECK'"
              :autoSize="{ minRows: 2, maxRows: 4 }"
            />
          </FormItem>
          <FormItem name="focusPeriodId" label="周期：" :colon="false">
            <div v-if="modalCategory === 'CHECK'">
              <Tag color="green"> {{ periodCategoryName }} </Tag>
              <span>{{ periodName }}</span>
            </div>
            <div v-else>
              <FormItemRest>
                <Select
                  v-model:value="periodCategoryCode"
                  style="width: 30%"
                  :options="periodCategoryList"
                  :fieldNames="{ label: 'name', value: 'code' }"
                  :disabled="
                    (evaluationCriteriaPlan?.status === 'PUBLISHED' &&
                      !(modalCategory === 'ADD')) ||
                    modalCategory === 'CHECK'
                  "
                  @change="periodCategoryChange"
                  placeholder="选择周期类型"
                />
              </FormItemRest>
              <Select
                :disabled="
                  (evaluationCriteriaPlan?.status === 'PUBLISHED' && !(modalCategory === 'ADD')) ||
                  modalCategory === 'CHECK'
                "
                :fieldNames="{ label: 'name', value: 'id' }"
                :options="periodList"
                style="width: 70%"
                v-model:value="focusPeriodId"
                placeholder="请选择周期"
                :allowClear="false"
              />
            </div>
          </FormItem>
          <FormItem name="dateRange" label="执行时间：" :colon="false">
            <span v-if="modalCategory === 'CHECK'"
              >{{ dayjs(dateRange[0]).local().format('YYYY-MM-DD HH:00') }} 至
              {{ dayjs(dateRange[1]).local().format('YYYY-MM-DD HH:00') }}</span
            >
            <FormItemRest v-else>
              <DatePicker
                v-model:value="dateRange[0]"
                :disabled-date="disabledDate"
                :show-time="{
                  format: 'HH',
                  defaultValue: dayjs().add(1, 'hour'),
                }"
                style="width: 50%"
                format="YYYY-MM-DD HH:00"
                placeholder="开始执行时间"
                :disabled="disableStartDate || modalCategory === 'CHECK'"
                :inputReadOnly="true"
                :showNow="false"
                :defaultPickerValue="dayjs().add(1, 'hour')"
                @open-change="handleStartOpenChange"
              />
              <DatePicker
                v-model:value="dateRange[1]"
                :disabled-date="disabledEndDate"
                :show-time="{
                  format: 'HH',
                }"
                style="width: 50%"
                format="YYYY-MM-DD HH:00"
                placeholder="结束执行时间"
                :open="endOpen"
                :inputReadOnly="true"
                :showNow="false"
                :disabled="modalCategory === 'CHECK'"
                @open-change="handleEndOpenChange"
              />
            </FormItemRest>
          </FormItem>
        </Form>
        <SelectScopeFrom
          ref="selectScopeFromRef"
          v-if="scopedPlanId || modalCategory === 'ADD'"
          v-show="currentStep === 1"
          :plan-id="scopedPlanId"
          :disabled="scopeDisable"
          @save-success="onCloseModal"
        />
      </div>
      <template #footer>
        <Button
          @click="stepAction"
          :preIcon="
            currentStep
              ? 'material-symbols:arrow-circle-left-outline'
              : 'material-symbols:arrow-circle-right-outline'
          "
          v-if="modalCategory !== 'CHECK'"
        >
          {{ currentStep ? '上' : '下' }}一步
        </Button>
        <Button
          @click="onClickSubmit('DRAFT')"
          preIcon="ant-design:save-outlined"
          v-if="showSetupLaterButton"
        >
          稍后设置
        </Button>
        <Button
          @click="onClickSubmit('DRAFT')"
          preIcon="ant-design:save-outlined"
          v-if="showDraftButton"
        >
          保存草稿
        </Button>
        <Button
          :type="'primary'"
          color="edit"
          preIcon="ion:paper-airplane"
          :iconSize="16"
          v-if="showPublishButton"
          @click="onClickSubmit('PUBLISHED')"
        >
          提交发布
        </Button>
      </template>
    </BasicModal>
  </div>
</template>

<script lang="ts">
  import { computed, defineComponent, nextTick, reactive, ref, toRefs } from 'vue';
  import { Loading } from '/@/components/Loading';
  import { Icon } from '/@/components/Icon';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { DatePicker, Form, Input, Select, Steps, Tag } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import {
    apiGetEvaluationCriteriaPlanDetail,
    apiSaveEvaluationCriteriaPlanAndScope,
  } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlan';
  import { apiGetEvaluationCriteriaList } from '/@/api/evaluationCriteria/evaluationCriteria';
  import { apiGetPeriodListByCategory } from '/@/api/period/period';
  import { apiGetPeriodCategoryList } from '/@/api/periodCategory/periodCategory';
  import dayjs from 'dayjs';
  import utc from 'dayjs/plugin/utc';
  import weekday from 'dayjs/plugin/weekday';
  import localeData from 'dayjs/plugin/localeData';
  import SelectScopeFrom from '/src/views/evaluationCriteriaPlan/components/SelectScopeForm.vue';
  import 'dayjs/locale/zh-cn';
  import { evaluationCriteriaPlanStatusEnum } from '/@/enums/bizEnum';

  export default defineComponent({
    components: {
      Tag,
      SelectScopeFrom,
      Loading,
      Icon,
      BasicModal,
      Form,
      FormItem: Form.Item,
      FormItemRest: Form.ItemRest,
      TextArea: Input.TextArea,
      Button,
      Select,
      DatePicker: DatePicker,
      Steps,
      Step: Steps.Step,
    },
    setup() {
      dayjs.extend(utc);
      dayjs.extend(weekday);
      dayjs.extend(localeData);
      const evaluationCriteriaIdList = ref<string[]>([]);
      const periodCategoryList = ref<Object[]>([]);
      const evaluationCriteriaList = ref<Object[]>([]);
      const evaluationCriteriaSearchList = ref<Object[]>([]);
      const periodIdList = ref<string[]>([]);
      const periodList = ref<Object[]>([]);
      const periodFilterTotal = ref(0);
      const formRef = ref();
      const evaluationCriteriaPlan = ref();
      const evaluationCriteriaPlanId = ref();
      const fullScreenLoading = ref(false);
      const evaluationCriteriaLoading = ref(false);
      const periodCategoryLoading = ref(false);
      const periodLoading = ref(false);
      const modalCategory = ref('ADD');
      const scopedPlanId = computed(() => {
        return evaluationCriteriaPlanId.value !== null ? evaluationCriteriaPlanId.value : undefined;
      });
      const evaluationCriteriaParams = ref({
        searchText: '',
        status_list: [evaluationCriteriaPlanStatusEnum.PUBLISHED],
      });
      const params = reactive({
        evaluationCriteriaId: null,
        focusPeriodId: null,
        name: '',
        dateRange: ['', ''],
        periodCategoryCode: 'SEMESTER',
        status: null,
      });
      const disableStartDate = ref(false);
      const readonly = ref(false);
      const scopeDisable = computed(() => {
        return params.dateRange
          ? dayjs(params.dateRange[1]).local().format('YYYY-MM-DD HH:00') <
              dayjs().local().format('YYYY-MM-DD HH:00')
          : null;
      });
      const [register, { closeModal }] = useModalInner((data) => {
        modalCategory.value = data.modalCategory;
        evaluationCriteriaList.value = [];
        if (data.modalCategory === 'ADD') {
          clearParams();
          getEvaluationCriteriaList();
          getPeriodList('SEMESTER');
          getPeriodCategoryList('SEMESTER');
          currentStep.value = 0;
          evaluationCriteriaPlanId.value = null;
        } else {
          evaluationCriteriaPlanId.value = data.evaluationCriteriaPlan.id;
          if (selectScopeFromRef.value?.formState) {
            selectScopeFromRef.value.formState.evaluationCriteriaPlanId =
              evaluationCriteriaPlanId.value;
            selectScopeFromRef.value.getPlanScope();
          }
          getEvaluationCriteriaPlanDetail();
        }
      });
      const clearParams = () => {
        params.evaluationCriteriaId = null;
        params.focusPeriodId = null;
        params.name = '';
        params.dateRange = ['', ''];
        params.periodCategoryCode = '';
        params.status = null;
      };

      const initParams = () => {
        currentStep.value = 0;
        const periodCategoryCode = evaluationCriteriaPlan.value.periodCategoryCode;
        const evaluationCriteriaId = evaluationCriteriaPlan.value.evaluationCriteriaId;
        const focusPeriodId = evaluationCriteriaPlan.value.focusPeriodId;
        params.name = evaluationCriteriaPlan.value.name;
        const executedStartAt = dayjs.utc(evaluationCriteriaPlan.value.executedStartAt).local();
        const executedFinishAt = dayjs.utc(evaluationCriteriaPlan.value.executedFinishAt).local();
        const dateRange = [executedStartAt, executedFinishAt];
        params.status = evaluationCriteriaPlan.value.status;
        disableStartDate.value =
          evaluationCriteriaPlan.value.status === evaluationCriteriaPlanStatusEnum.PUBLISHED &&
          dayjs().isAfter(dayjs(executedStartAt));
        getEvaluationCriteriaList(evaluationCriteriaId);
        getPeriodList(periodCategoryCode, dateRange, focusPeriodId);
        getPeriodCategoryList(periodCategoryCode);
      };
      const getEvaluationCriteriaPlanDetail = () => {
        fullScreenLoading.value = true;
        apiGetEvaluationCriteriaPlanDetail(evaluationCriteriaPlanId.value)
          .then((res) => {
            if (res.code === 200) {
              evaluationCriteriaPlan.value = res.data;
              initParams();
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch((err) => {
            console.log(`error: ${err}`);
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络异常',
            });
          })
          .finally(() => {
            fullScreenLoading.value = false;
          });
      };
      const evaluationCriteriaName = ref('');
      const getEvaluationCriteriaList = (evaluationCriteriaId = null) => {
        evaluationCriteriaLoading.value = true;
        apiGetEvaluationCriteriaList(evaluationCriteriaParams.value)
          .then((res) => {
            if (res.code === 200) {
              evaluationCriteriaList.value.push(...res.data);
              if (evaluationCriteriaId) {
                nextTick(() => {
                  // 如果标准被废除后，查看时需要显示标准名
                  evaluationCriteriaName.value =
                    evaluationCriteriaPlan.value.evaluationCriteriaName;
                  params.evaluationCriteriaId = evaluationCriteriaList.value.some(
                    (item) => item.id === evaluationCriteriaId,
                  )
                    ? evaluationCriteriaId
                    : evaluationCriteriaPlan.value.evaluationCriteriaName;
                });
              }
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch((err) => {
            console.log(`error: ${err}`);
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络异常',
            });
          })
          .finally(() => {
            evaluationCriteriaLoading.value = false;
          });
      };
      const periodName = ref('');
      const getPeriodList = (
        periodCategoryCode: null | string = null,
        dateRange: null | Object[] = null,
        focusPeriodId: string[] | null = null,
      ) => {
        periodLoading.value = true;
        apiGetPeriodListByCategory(periodCategoryCode)
          .then((res) => {
            if (res.code === 200) {
              periodFilterTotal.value = res.data.filterCount;
              periodList.value = res.data;
              if (dateRange) {
                nextTick(() => {
                  // @ts-ignore
                  params.dateRange = dateRange;
                });
              }
              if (focusPeriodId) {
                nextTick(() => {
                  // @ts-ignore
                  params.focusPeriodId = focusPeriodId;
                  periodName.value = res.data.find((item) => item.id === focusPeriodId).name;
                });
              }
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch((err) => {
            console.log(`error: ${err}`);
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络异常',
            });
          })
          .finally(() => {
            periodLoading.value = false;
          });
      };
      const periodCategoryName = ref('');
      const getPeriodCategoryList = (periodCategoryCode: string | null = null) => {
        periodCategoryLoading.value = true;
        apiGetPeriodCategoryList()
          .then((res) => {
            if (res.code === 200) {
              periodCategoryList.value = res.data;
              if (periodCategoryCode) {
                nextTick(() => {
                  params.periodCategoryCode = periodCategoryCode;
                  periodCategoryName.value = res.data.find(
                    (item) => item.code === periodCategoryCode,
                  ).name;
                });
              }
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch((err) => {
            console.log(`error: ${err}`);
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络异常',
            });
          })
          .finally(() => {
            periodCategoryLoading.value = false;
          });
      };

      const validateFocusPeriodIdList = async (_rule, _value) => {
        if (!params.focusPeriodId) {
          return Promise.reject('请选择周期');
        }

        return Promise.resolve();
      };

      const validateDateRange = async (_rule, _value) => {
        const [planStartAt, planFinishAt] = params.dateRange;

        if (!planStartAt || !planFinishAt) {
          return Promise.reject('请选择执行时间');
        }

        if (
          dayjs(planStartAt).isBefore(dayjs().startOf('hour')) &&
          evaluationCriteriaPlan.value?.status === evaluationCriteriaPlanStatusEnum.DRAFT
        ) {
          params.dateRange = ['', ''];
          return Promise.reject('计划执行开始时间需要大于当前时间');
        }

        if (
          dayjs(planFinishAt) < dayjs() &&
          evaluationCriteriaPlan.value.status === evaluationCriteriaPlanStatusEnum.PUBLISHED
        ) {
          params.dateRange[1] = '';
          return Promise.reject('计划执行结束时间需要大于当前时间');
        }

        if (
          dayjs(planFinishAt).isBefore(dayjs()) &&
          evaluationCriteriaPlan.value.status === evaluationCriteriaPlanStatusEnum.DRAFT
        ) {
          params.dateRange[1] = '';
          return Promise.reject('计划执行结束时间需要大于当前时间');
        }

        return Promise.resolve();
      };

      const formRules = {
        evaluationCriteriaId: [
          {
            required: true,
            trigger: ['blur', 'change'],
            message: '请选择评价标准',
            whitespace: true,
          },
        ],
        name: [
          {
            required: true,
            trigger: ['blur', 'change'],
            message: '请输入名称',
            whitespace: true,
          },
        ],
        focusPeriodId: [
          {
            required: true,
            trigger: ['blur', 'change'],
            whitespace: true,
            validator: validateFocusPeriodIdList,
          },
        ],
        dateRange: [
          {
            required: true,
            trigger: ['blur', 'change'],
            whitespace: true,
            validator: validateDateRange,
          },
        ],
        status: [
          {
            required: true,
            trigger: ['blur', 'change'],
            message: '请选择状态',
            whitespace: true,
          },
        ],
      };

      const disabledDate = (current: dayjs.Dayjs) => {
        return current && current.isBefore(dayjs().add(1, 'hour').startOf('hour'));
      };

      const disabledEndDate = (current: dayjs.Dayjs) => {
        const startLimit = dayjs(params.dateRange[0]);
        return startLimit.isAfter(current.startOf('hour'));
      };

      const selectScopeFromRef = ref();

      const currentStep = ref<number>(0);

      const stepsTitle = ref(['编辑评价计划', '计划适用范围']);

      const stepAction = () => {
        checkDate();
        formRef.value.validateFields().then(() => {
          currentStep.value = Number(!currentStep.value);
        });
      };
      const checkDate = () => {
        let invalidDate = false;
        const now = dayjs().local().format('YYYY-MM-DD HH:mm');
        params.dateRange.forEach((d, idx) => {
          if (params.status === evaluationCriteriaPlanStatusEnum.PUBLISHED && idx === 0) {
            return; // 在 forEach 中，使用 return 相当于在常规循环中的 continue
          }
          const formatDate = dayjs(d).format('YYYY-MM-DD HH:00');
          if (formatDate < now) {
            invalidDate = true;
          }
        });

        if (invalidDate) {
          useMessage().createErrorNotification({
            message: '错误',
            description: '计划执行时间需要大于当前时间,请重新设置',
          });
        }
      };

      const showPublishButton = computed(() => {
        return (
          modalCategory.value !== 'CHECK' &&
          selectScopeFromRef &&
          ((params.status === 'PUBLISHED' &&
            (selectScopeFromRef.value?.formState.deptIdList ||
              selectScopeFromRef.value?.formState.peopleIdList)) ||
            (params.status !== 'PUBLISHED' &&
              (selectScopeFromRef.value?.formState.deptIdList?.length > 0 ||
                selectScopeFromRef.value?.formState.peopleIdList?.length > 0)))
        );
      });

      const showDraftButton = computed(() => {
        return (
          (evaluationCriteriaPlan.value?.status === evaluationCriteriaPlanStatusEnum.DRAFT ||
            modalCategory.value === 'ADD') &&
          selectScopeFromRef &&
          (currentStep.value === 0 ||
            (currentStep.value === 1 &&
              (selectScopeFromRef.value.formState.deptIdList ||
                selectScopeFromRef.value.formState.peopleIdList)))
        );
      });

      const showSetupLaterButton = computed(() => {
        return (
          selectScopeFromRef.value &&
          !selectScopeFromRef.value.formState.deptIdList &&
          !selectScopeFromRef.value.formState.peopleIdList &&
          currentStep.value === 1
        );
      });

      const endOpen = ref<boolean>(false);

      const handleStartOpenChange = (open: boolean) => {
        const [planStartAt, planFinishAt] = params.dateRange;
        if (!open) {
          endOpen.value = true;
          if (!planFinishAt && planStartAt) {
            params.dateRange[1] = dayjs(planStartAt).add(1, 'hour');
          }

          if (
            dayjs(planFinishAt).format('YYYY-MM-DD HH:00') <=
              dayjs(planStartAt).format('YYYY-MM-DD HH:00') &&
            planStartAt
          ) {
            params.dateRange[1] = dayjs(planStartAt).add(1, 'hour');
          }
        }

        if (dayjs(planFinishAt).isBefore(dayjs(planStartAt))) {
          params.dateRange[1] = '';
        }
      };

      const handleEndOpenChange = (open: boolean) => {
        endOpen.value = open;
      };

      return {
        evaluationCriteriaIdList,
        evaluationCriteriaList,
        periodFilterTotal,
        periodList,
        periodIdList,
        formRef,
        evaluationCriteriaPlan,
        fullScreenLoading,
        modalCategory,
        register,
        closeModal,
        params,
        ...toRefs(params),
        formRules,
        evaluationCriteriaLoading,
        evaluationCriteriaParams,
        getEvaluationCriteriaList,
        periodLoading,
        periodCategoryList,
        getPeriodList,
        periodCategoryLoading,
        disabledDate,
        evaluationCriteriaPlanId,
        selectScopeFromRef,
        stepsTitle,
        currentStep,
        stepAction,
        readonly,
        scopedPlanId,
        showPublishButton,
        showDraftButton,
        showSetupLaterButton,
        evaluationCriteriaSearchList,
        scopeDisable,
        clearParams,
        handleStartOpenChange,
        handleEndOpenChange,
        endOpen,
        disabledEndDate,
        disableStartDate,
        dayjs,
        evaluationCriteriaName,
        periodCategoryName,
        periodName,
      };
    },
    methods: {
      periodCategoryChange() {
        this.params.focusPeriodId = null;
        this.getPeriodList(this.periodCategoryCode);
      },
      evaluationCriteriaChange() {
        this.evaluationCriteriaParams.searchText = '';
      },
      searchEvaluationCriteria(value) {
        this.evaluationCriteriaParams.searchText = value;
        this.evaluationCriteriaSearchList = this.evaluationCriteriaList.filter((item) =>
          // @ts-ignore
          item.name.includes(this.evaluationCriteriaParams.searchText),
        );
      },
      onCloseModal() {
        this.closeModal();
        this.clearParams();
        this.currentStep = 0;
        this.disableStartDate = false;
        this.evaluationCriteriaPlanId = '';
        this.evaluationCriteriaPlan = null;
        this.evaluationCriteriaParams.searchText = '';
        this.selectScopeFromRef.formState.deptIdList = [];
        this.selectScopeFromRef.formState.peopleIdList = [];
      },
      onClickSubmit(status) {
        this.formRef
          .validateFields()
          .then(() => {
            const startDate = this.params.dateRange ? this.params.dateRange[0] : dayjs();
            if (
              startDate.startOf('day') < dayjs().startOf('day') &&
              this.params.status === evaluationCriteriaPlanStatusEnum.DRAFT
            ) {
              useMessage().createErrorNotification({
                message: '错误',
                description: '计划开始执行日期小于当前日期，请重新选择',
              });
              return;
            }
            const formData = this.selectScopeFromRef.formState;
            const hasPeople = formData.peopleIdList && formData.peopleIdList.length > 0;
            const hasDept = formData.deptIdList && formData.deptIdList.length > 0;
            if (status === evaluationCriteriaPlanStatusEnum.PUBLISHED && !hasPeople && !hasDept) {
              useMessage().createErrorNotification({
                message: '错误',
                description: '请选择部门或人员',
              });
              return;
            }
            useMessage().createConfirm({
              iconType: 'info',
              title: '提示',
              content: '确定要提交吗？',
              onOk: () => {
                this.params.status = status;
                this.saveEvaluationCriteriaPlan();
              },
              onCancel() {},
            });
          })
          .catch(() => {
            this.currentStep = 0;
            useMessage().createErrorNotification({
              message: '错误',
              description: '请完善评价计划信息',
            });
          });
      },
      preparePrams() {
        let executedStartAt = null;
        let executedFinishAt = null;
        if (this.params.dateRange) {
          // @ts-ignore
          executedStartAt = dayjs(this.params.dateRange[0]).format('YYYY-MM-DD HH:00:00');
          // @ts-ignore
          executedFinishAt = dayjs(this.params.dateRange[1]).format('YYYY-MM-DD HH:00:00');
        }
        let focusPeriodId = null;
        if (this.params.focusPeriodId) {
          // @ts-ignore
          focusPeriodId = this.params.focusPeriodId;
        }
        return {
          evaluationCriteriaPlan: {
            id: this.evaluationCriteriaPlan?.id,
            version: this.evaluationCriteriaPlan?.version,
            evaluationCriteriaId: this.params.evaluationCriteriaId,
            focusPeriodId: focusPeriodId,
            name: this.params.name,
            executedStartAt: executedStartAt,
            executedFinishAt: executedFinishAt,
            status: this.params.status,
          },
          evaluationCriteriaPlanScope: this.selectScopeFromRef.formState,
        };
      },
      saveEvaluationCriteriaPlan() {
        const params = this.preparePrams();
        this.fullScreenLoading = true;
        apiSaveEvaluationCriteriaPlanAndScope(params)
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
          .catch((err) => {
            console.log(`error: ${err}`);
            useMessage().createErrorNotification({
              message: '错误',
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
          })
          .finally(() => {
            this.fullScreenLoading = false;
          });
      },
    },
  });
</script>

<style scoped lang="less">
  .edit-evaluation-criteria-plan-modal {
    ::v-deep(.ant-modal) {
      max-width: calc(100vw) !important;

      .scroll-container .scrollbar__wrap {
        margin-bottom: 0 !important;
      }

      .content {
        height: 40vh;
        padding: 16px;
      }

      .steps {
        width: 50%;
        margin: 20px auto;
      }
    }

    ::v-deep(.ant-picker-dropdown
        > .ant-picker-panel-container
        > .ant-picker-footer
        > .ant-picker-ranges
        > .ant-picker-now) {
      display: none;
    }
  }
</style>
