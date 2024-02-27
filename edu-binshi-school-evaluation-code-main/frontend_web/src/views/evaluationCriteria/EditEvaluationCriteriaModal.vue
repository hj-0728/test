<template>
  <div class="edit-evaluation-criteria-modal" ref="editEvaluationCriteriaModalRef">
    <BasicModal
      @register="register"
      :canFullscreen="false"
      :defaultFullscreen="false"
      :draggable="false"
      :destroyOnClose="true"
      :getContainer="() => $refs.editEvaluationCriteriaModalRef"
      :closable="true"
      :centered="true"
      :maskClosable="false"
      width="60vw"
    >
      <template #title>
        <Icon icon="ri:file-list-2-line" />
        <span v-if="modalCategory === 'EDIT'"> 编辑评价标准 </span>
        <span v-if="modalCategory === 'ADD'"> 添加评价标准 </span>
      </template>
      <Loading :loading="fullScreenLoading" :absolute="true" />
      <div class="content">
        <Form
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
          <FormItem name="name" label="名称：" :colon="false">
            <TextArea
              v-model:value="name"
              show-count
              :maxlength="50"
              :autoSize="{ minRows: 2, maxRows: 4 }"
            />
          </FormItem>
          <FormItem name="comments" label="描述：" :colon="false">
            <TextArea v-model:value="comments" :autoSize="{ minRows: 2, maxRows: 4 }" />
          </FormItem>
          <FormItem name="focusPeriodId" label="周期：" :colon="false">
            <FormItemRest>
              <Select
                v-model:value="periodCategoryCode"
                style="width: 30%"
                :options="periodCategoryList"
                :fieldNames="{ label: 'name', value: 'code' }"
                @change="periodCategoryChange"
                placeholder="选择周期类型"
              />
            </FormItemRest>
            <Select
              :fieldNames="{ label: 'name', value: 'id' }"
              :options="periodList"
              style="width: 70%"
              v-model:value="focusPeriodId"
              placeholder="请选择周期"
              :allowClear="false"
            />
          </FormItem>
          <FormItem
            name="limitedStringOptions"
            label="是否可拓展："
            :colon="false"
            :rules="{
              required: true,
              trigger: ['blur'],
            }"
          >
            <CheckboxGroup v-model:value="selectedOption">
              <Row>
                <Col v-for="item in selectOptions" :key="item" :span="8">
                  <Checkbox :value="item">{{ item }}</Checkbox>
                </Col>
              </Row>
            </CheckboxGroup>
          </FormItem>
          <!--          <FormItem-->
          <!--            name="evaluation_object_category"-->
          <!--            label="评价对象："-->
          <!--            :colon="false"-->
          <!--            v-if="modalCategory === 'ADD'"-->
          <!--          >-->
          <!--            <RadioGroup v-model:value="evaluation_object_category">-->
          <!--              <Radio value="STUDENT"> 学生 </Radio>-->
          <!--              <Radio value="PARENTS"> 家长 </Radio>-->
          <!--              <Radio value="TEACHER"> 老师 </Radio>-->
          <!--            </RadioGroup>-->
          <!--          </FormItem>-->
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
  import { defineComponent, reactive, nextTick, ref, toRefs } from 'vue';
  import { Loading } from '/@/components/Loading';
  import { Icon } from '/@/components/Icon';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Checkbox, Col, Form, Input, Row, Select } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import {
    apiGetEvaluationCriteriaDetail,
    apiSaveEvaluationCriteria,
  } from '/@/api/evaluationCriteria/evaluationCriteria';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import { apiGetPeriodCategoryList } from '/@/api/periodCategory/periodCategory';
  import { apiGetPeriodListByCategory } from '/@/api/period/period';

  export default defineComponent({
    components: {
      Row,
      Col,
      Checkbox,
      Select,
      Loading,
      Icon,
      BasicModal,
      Form,
      FormItem: Form.Item,
      TextArea: Input.TextArea,
      Button,
      FormItemRest: Form.ItemRest,
      CheckboxGroup: Checkbox.Group,
      // Radio,
      // RadioGroup: Radio.Group,
    },
    setup() {
      const modalCategory = ref('ADD');
      const fullScreenLoading = ref(false);
      const formRef = ref();
      const evaluationCriteriaId = ref();
      const evaluationCriteria = ref();
      const selectOptions = ['是'];
      const [register, { closeModal }] = useModalInner((data) => {
        console.log(data);
        evaluationCriteria.value = null;
        modalCategory.value = data.modalCategory;
        getPeriodCategoryList('SEMESTER');
        getPeriodList('SEMESTER');
        if (data.modalCategory === 'EDIT') {
          evaluationCriteriaId.value = data.evaluationCriteria.id;
          getEvaluationCriteriaDetail();
        } else {
          clearPrams();
        }
      });
      const selectedOption = ref('是');
      const periodCategoryLoading = ref(false);
      const periodCategoryList = ref<Object[]>([]);
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

      const clearPrams = () => {
        params.name = '';
        params.comments = null;
      };

      const initParams = () => {
        params.name = evaluationCriteria.value.name;
        params.status = modalCategory.value === 'ADD' ? 'DRAFT' : evaluationCriteria.value.status;
        params.comments = evaluationCriteria.value.comments;
        params.evaluation_object_category = evaluationCriteria.value.evaluationObjectCategory;
      };

      const getEvaluationCriteriaDetail = () => {
        fullScreenLoading.value = true;
        apiGetEvaluationCriteriaDetail(evaluationCriteriaId.value)
          .then((res) => {
            console.log(res);
            if (res.code === 200) {
              evaluationCriteria.value = res.data;
              initParams();
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
            fullScreenLoading.value = false;
          });
      };

      const params = reactive({
        name: '',
        status: 'DRAFT',
        comments: null,
        evaluation_object_category: 'STUDENT',
        periodCategoryCode: 'SEMESTER',
        focusPeriodId: null,
      });
      const periodLoading = ref(false);
      const periodFilterTotal = ref(0);
      const periodList = ref<Object[]>([]);
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
      const formRules = {
        name: [
          {
            required: true,
            trigger: ['blur', 'change'],
            message: '请输入名称',
            whitespace: true,
          },
        ],
        // evaluation_object_category: [
        //   {
        //     required: true,
        //     trigger: ['blur', 'change'],
        //     message: '请选择评价对象',
        //     whitespace: true,
        //   },
        // ],
      };
      return {
        modalCategory,
        register,
        closeModal,
        fullScreenLoading,
        params,
        ...toRefs(params),
        formRules,
        formRef,
        evaluationCriteria,
        periodCategoryList,
        periodCategoryName,
        getPeriodList,
        periodList,
        periodName,
        periodLoading,
        selectOptions,
        selectedOption,
      };
    },
    methods: {
      periodCategoryChange() {
        this.params.focusPeriodId = null;
        this.getPeriodList(this.periodCategoryCode);
      },
      onCloseModal() {
        this.closeModal();
      },
      onClickSubmit() {
        this.formRef.validateFields().then(() => {
          useMessage().createConfirm({
            iconType: 'info',
            title: '提示',
            content: '确定要提交吗？',
            onOk: () => {
              this.saveEvaluationCriteria();
            },
            onCancel() {},
          });
        });
      },
      preparePrams() {
        console.log('preparePrams ...');
        console.log(this.evaluationCriteria);
        return {
          id: this.evaluationCriteria?.id,
          version: this.evaluationCriteria?.version,
          name: this.params.name,
          status: this.modalCategory === 'ADD' ? 'DRAFT' : this.params.status,
          evaluation_object_category: this.params.evaluation_object_category,
          comments: this.params.comments,
        };
      },
      saveEvaluationCriteria() {
        const params = this.preparePrams();
        this.fullScreenLoading = true;
        apiSaveEvaluationCriteria(params)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '保存成功',
              });
              this.$emit('saveSuccess');
              this.closeModal();
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
    },
  });
</script>

<style scoped lang="less">
  .edit-evaluation-criteria-modal {
    ::v-deep(.ant-modal) {
      max-width: calc(100vw) !important;

      .scroll-container .scrollbar__wrap {
        margin-bottom: 0 !important;
      }

      .scrollbar__view {
        //height: calc(100% - 50px);
        height: 50vh;
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
        height: 50vh;
        //background-color: #00acc1;
        overflow-y: auto;
        padding: 16px;
      }
    }
  }
</style>
