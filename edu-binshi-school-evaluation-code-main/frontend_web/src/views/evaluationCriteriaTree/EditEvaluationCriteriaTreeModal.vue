<template>
  <div ref="editEvaluationCriteriaTreeModalRef" class="edit-evaluation-criteria-tree-modal">
    <BasicModal
      @register="register"
      :canFullscreen="false"
      :defaultFullscreen="false"
      :draggable="false"
      :destroyOnClose="true"
      :getContainer="() => $refs.editEvaluationCriteriaTreeModalRef"
      :closable="true"
      :centered="true"
      :maskClosable="false"
      width="60vw"
    >
      <template #title>
        <Icon icon="ri:file-list-2-line" />
        <span> {{ readonly ? '查看' : modalCategory === 'ADD' ? '添加' : '编辑' }}评价项 </span>
      </template>
      <Loading :loading="fullScreenLoading" :absolute="false" />
      <div class="content">
        <Row v-if="evaluationCriteriaTreeNode">
          <Col :span="3" />
          <Col :span="18">
            <Alert :type="modalCategory === 'ADD' ? 'success' : 'info'">
              <template #description>
                <span v-if="modalCategory === 'ADD'">
                  在评价项 <SvgIcon name="leftQuotation" size="16" /><span
                    style="font-weight: bolder; font-size: 20px"
                    >{{ evaluationCriteriaTreeNode?.name }}</span
                  ><SvgIcon name="rightQuotation" size="16" />下添加子级评价项
                </span>
                <span v-else>
                  {{ readonly ? '查看' : '编辑' }}评价项<SvgIcon
                    name="leftQuotation"
                    size="16"
                  /><span style="font-weight: bolder; font-size: 20px">{{
                    evaluationCriteriaTreeNode?.name
                  }}</span
                  ><SvgIcon name="rightQuotation" size="16" />下的子级评价项
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
          :rules="formRules"
          style="margin-top: 20px"
        >
          <FormItem name="name" label="名称：" :colon="false">
            <span v-if="readonly">{{ name }}</span>
            <TextArea
              v-else
              v-model:value="name"
              show-count
              :maxlength="100"
              :autoSize="{ minRows: 2, maxRows: 4 }"
              :readonly="readonly"
            />
          </FormItem>
          <FormItem name="comments" label="描述：" :colon="false">
            <span v-if="readonly">
              <span v-if="comments">{{ comments }}</span>
              <span v-else>暂无描述</span>
            </span>
            <TextArea
              v-else
              v-model:value="comments"
              show-count
              :maxlength="255"
              :autoSize="{ minRows: 2, maxRows: 4 }"
              :readonly="readonly"
            />
          </FormItem>
          <!--          <FormItem-->
          <!--            name="tagOwnershipId"-->
          <!--            label="标签："-->
          <!--            :colon="false"-->
          <!--            v-if="-->
          <!--              !evaluationCriteriaTreeNode ||-->
          <!--              (modalCategory === 'EDIT' && evaluationCriteriaTreeNode.level === 1)-->
          <!--            "-->
          <!--          >-->
          <!--            <RadioGroup v-model:value="tagOwnershipId">-->
          <!--              <Radio v-for="option in tagOptions" :value="option.tagOwnershipId">-->
          <!--                {{ option.name }}-->
          <!--              </Radio>-->
          <!--            </RadioGroup>-->
          <!--          </FormItem>-->
        </Form>
      </div>
      <template #footer>
        <Button @click="onCloseModal" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
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
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Loading } from '/@/components/Loading';
  import { Icon, SvgIcon } from '/@/components/Icon';
  import { Form, Input, Row, Col, Alert } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import {
    apiGetEvaluationCriteriaTreeDetail,
    apiSaveEvaluationCriteriaTree,
  } from '/@/api/evaluationCriteriaTree/evaluationCriteriaTree';
  import { apiGetTagList } from '/@/api/tag/tag';

  export default defineComponent({
    components: {
      BasicModal,
      Loading,
      Icon,
      Form,
      FormItem: Form.Item,
      TextArea: Input.TextArea,
      Button,
      Row,
      Col,
      Alert,
      SvgIcon,
    },
    emit: ['saveSuccess', 'saveError'],
    setup() {
      const formRef = ref();
      const fullScreenLoading = ref(false);
      const evaluationCriteriaTreeNode = ref();
      const evaluationCriteriaTree = ref({});
      const modalCategory = ref('ADD');
      const readonly = ref(false);
      const refreshKey = ref(new Date().getTime());
      const [register, { closeModal }] = useModalInner((data) => {
        console.log(data);
        clearPrams();
        refreshKey.value = new Date().getTime();
        modalCategory.value = data.modalCategory;
        readonly.value = data.readonly;
        evaluationCriteriaTreeNode.value = data.evaluationCriteriaTreeNode;
        if (modalCategory.value === 'EDIT') {
          getEvaluationCriteriaDetail();
        }
      });
      const params = reactive({
        name: '',
        indicatorId: '',
        isActivated: false,
        comments: null,
        benchmarkCheckedList: [],
        tagOwnershipId: null,
      });
      const loading = ref(true);
      const tagOptions = ref([]);
      const clearPrams = () => {
        params.name = '';
        params.indicatorId = '';
        params.comments = null;
        params.tagOwnershipId = null;
        params.benchmarkCheckedList = [];
        evaluationCriteriaTreeNode.value = null;
        evaluationCriteriaTree.value = null;
      };
      const initParams = () => {
        params.name = evaluationCriteriaTree.value.name;
        params.comments = evaluationCriteriaTree.value?.comments;
      };

      const getEvaluationCriteriaDetail = () => {
        fullScreenLoading.value = true;
        apiGetEvaluationCriteriaTreeDetail(evaluationCriteriaTreeNode.value.id)
          .then((res) => {
            console.log(res);
            if (res.code === 200) {
              evaluationCriteriaTree.value = res.data;
              params.tagOwnershipId = evaluationCriteriaTree.value?.tagOwnershipId;
              initParams();
            } else {
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
            loading.value = false;
          });
      };

      const getTagList = () => {
        fullScreenLoading.value = true;
        apiGetTagList('EVALUATION_CRITERIA_TREE')
          .then((res) => {
            if (res.code === 200) {
              tagOptions.value = res.data;
            } else {
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
            loading.value = false;
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
        tagOwnershipId: [
          {
            required: true,
            trigger: ['blur', 'change'],
            message: '请选择标签',
            whitespace: true,
          },
        ],
      };
      getTagList();
      return {
        formRef,
        fullScreenLoading,
        modalCategory,
        register,
        closeModal,
        params,
        ...toRefs(params),
        formRules,
        evaluationCriteriaTree,
        evaluationCriteriaTreeNode,
        clearPrams,
        refreshKey,
        loading,
        tagOptions,
        readonly,
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
        return {
          id: this.evaluationCriteriaTree?.id,
          version: this.evaluationCriteriaTree?.version,
          indicatorVersion: this.evaluationCriteriaTree?.indicatorVersion,
          parentIndicatorId:
            this.evaluationCriteriaTreeNode?.indicatorId === 'root'
              ? null
              : this.evaluationCriteriaTreeNode?.indicatorId,
          indicatorId: this.evaluationCriteriaTree?.indicatorId,
          evaluationCriteriaId: this.$route.params.evaluationCriteriaId,
          name: this.params.name,
          comments: this.params.comments,
          tagOwnershipId: this.tagOwnershipId,
        };
      },
      saveBenchmark() {
        const params = this.preparePrams();
        this.fullScreenLoading = true;
        apiSaveEvaluationCriteriaTree(params)
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
    },
  });
</script>

<style scoped lang="less">
  .edit-evaluation-criteria-tree-modal {
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
