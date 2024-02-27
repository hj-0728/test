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
      @cancel="onCloseModal"
      width="60vw"
    >
      <template #title>
        <Icon icon="ri:file-list-2-line" />
        <span> 绑定标签 </span>
      </template>
      <Loading :loading="loading" :absolute="false" />
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
          <FormItem name="tagOwnershipId" label="标签：" :colon="false">
            <RadioGroup v-model:value="tagName">
              <Radio :key="option.value" v-for="option in tagOptions" :value="option.value">
                {{ option.value }}
              </Radio>
            </RadioGroup>
          </FormItem>
          <FormItem name="levelSelect" label="层级：" :colon="false">
            <RadioGroup v-model:value="level" :disabled="!canSelectLevel">
              <Radio :key="option.value" v-for="option in levelOptions" :value="option.value">
                {{ option.label }}
              </Radio>
            </RadioGroup>
          </FormItem>
          <FormItem
            name="evaluationCriteriaTreeIdList"
            label="评价项："
            :colon="false"
            :autoLink="false"
          >
            <Tabs type="card" v-model:activeKey="activeKey">
              <template v-for="item in tabsOptions" :key="item.key">
                <TabPane :tab="item.tab">
                  <EvaluationCriteriaItemList
                    ref="evaluationCriteriaItemListRef"
                    :key="tagName + evaluationCriteriaId + level + activeKey + refresh"
                    :tagName="tagName"
                    :level="level"
                    :selected="activeKey === 'selected'"
                    :evaluation-criteria-id="evaluationCriteriaId"
                    @on-select-evaluation-criteria-item="onSelectEvaluationCriteriaItem"
                  />
                </TabPane>
              </template>
            </Tabs>
          </FormItem>
        </Form>
      </div>
      <template #footer>
        <Button @click="onCloseModal" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
        <Button
          :type="'primary'"
          color="edit"
          preIcon="ion:paper-airplane"
          :iconSize="16"
          v-if="activeKey === 'notSelected'"
          @click="onClickSubmit"
        >
          绑定标签
        </Button>
        <Button
          :type="'primary'"
          color="error"
          preIcon="ion:paper-airplane"
          :iconSize="16"
          v-if="activeKey === 'selected'"
          @click="onClickSubmit"
        >
          解除绑定
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
  import { Form, Radio, Tabs } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import {
    apiEvaluationCriteriaTreeBindTag,
    apiEvaluationCriteriaTreeUnboundTag,
    apiGetEvaluationCriteriaTreeBoundTagDetail,
  } from '/@/api/evaluationCriteriaTree/evaluationCriteriaTree';
  import { apiGetTagList } from '/@/api/tag/tag';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import EvaluationCriteriaItemList from '/@/views/evaluationCriteriaTree/bindTagComponents/EvaluationCriteriaItemList.vue';
  export default defineComponent({
    components: {
      // EvaluationCriteriaItemTable,
      EvaluationCriteriaItemList,
      BasicModal,
      Loading,
      Icon,
      Form,
      FormItem: Form.Item,
      Button,
      Radio,
      RadioGroup: Radio.Group,
      Tabs,
      TabPane: Tabs.TabPane,
    },
    emit: ['saveSuccess', 'saveError'],
    setup() {
      const formRef = ref();
      const evaluationCriteriaId = ref('');
      const level = ref<number>(1);
      const evaluationCriteriaTreeIdList = ref<string[]>([]);
      const tagOptions = ref([]);
      const tagName = ref();
      const levelOptions = [
        {
          label: '第一层评价项',
          value: 1,
        },
        {
          label: '第二层评价项',
          value: 2,
        },
      ];
      const [register, { closeModal }] = useModalInner((data) => {
        clearPrams();
        evaluationCriteriaId.value = data.evaluationCriteriaId;
        getEvaluationCriteriaTreeBoundTagDetail();
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
      const clearPrams = () => {
        params.name = '';
        params.indicatorId = '';
        params.comments = null;
        params.tagOwnershipId = null;
        params.benchmarkCheckedList = [];
      };
      const getTagList = () => {
        loading.value = true;
        apiGetTagList()
          .then((res) => {
            if (res.code === 200) {
              tagOptions.value = res.data;
              tagName.value = res.data[0].value;
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
            loading.value = false;
          });
      };
      const formRules = {
        level: [
          {
            required: true,
            trigger: ['blur', 'change'],
            message: '请选择层级',
            whitespace: true,
          },
        ],
        tagName: [
          {
            required: true,
            trigger: ['blur', 'change'],
            message: '请选择标签',
            whitespace: true,
          },
        ],
      };
      getTagList();
      const canSelectLevel = ref(true);
      const getEvaluationCriteriaTreeBoundTagDetail = () => {
        if (evaluationCriteriaId.value) {
          loading.value = true;
          apiGetEvaluationCriteriaTreeBoundTagDetail(evaluationCriteriaId.value)
            .then((res) => {
              if (res.code === 200) {
                canSelectLevel.value = true;
                if (res.data.totalTagCount > 0) {
                  canSelectLevel.value = false;
                  if (res.data.rootTagCount > 0) {
                    level.value = 1;
                  } else {
                    level.value = 2;
                  }
                }
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
                description: '网络错误',
              });
            })
            .finally(() => {
              loading.value = false;
            });
        }
      };
      const activeKey = ref('notSelected');
      const tabsOptions = ref([
        {
          key: 'notSelected',
          tab: '未选',
        },
        {
          key: 'selected',
          tab: '已选',
        },
      ]);
      const refresh = ref('goRefresh');
      return {
        formRef,
        register,
        closeModal,
        params,
        ...toRefs(params),
        formRules,
        clearPrams,
        loading,
        evaluationCriteriaId,
        levelOptions,
        level,
        tagName,
        tagOptions,
        canSelectLevel,
        evaluationCriteriaTreeIdList,
        getEvaluationCriteriaTreeBoundTagDetail,
        activeKey,
        tabsOptions,
        refresh,
      };
    },
    methods: {
      onCloseModal() {
        this.$emit('saveSuccess');
        this.closeModal();
        this.clearPrams();
      },
      onCloseModalParent() {
        this.closeModal();
        this.clearPrams();
      },
      onClickSubmit() {
        if (this.evaluationCriteriaTreeIdList.length === 0) {
          useMessage().createErrorNotification({
            message: '提示',
            description: '请选择评价项',
          });
          this.loading = false;
          return;
        }
        let content = '确定要解除绑定吗？';
        if (this.activeKey === 'notSelected') {
          content = '确定要提交吗？';
        }
        this.formRef.validateFields().then(() => {
          useMessage().createConfirm({
            iconType: 'info',
            title: '提示',
            content: content,
            onOk: () => {
              this.saveEvaluationCriteriaTreeBindTag();
            },
            onCancel() {},
          });
        });
      },
      saveEvaluationCriteriaTreeBindTag() {
        this.loading = true;
        let api = apiEvaluationCriteriaTreeUnboundTag;
        let description = '解除绑定成功';
        if (this.activeKey === 'notSelected') {
          api = apiEvaluationCriteriaTreeBindTag;
          description = '绑定成功';
        }
        api({
          tagName: this.tagName,
          evaluationCriteriaId: this.evaluationCriteriaId,
          evaluationCriteriaTreeIdList: this.evaluationCriteriaTreeIdList,
        })
          .then((res) => {
            if (res.code === 200) {
              this.getEvaluationCriteriaTreeBoundTagDetail();
              this.refresh += '1';
              useMessage().createSuccessNotification({
                message: '成功',
                description: description,
              });
              this.evaluationCriteriaTreeIdList = [];
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
              description: '网络异常',
            });
          })
          .finally(() => {
            this.loading = false;
          });
      },
      onSelectEvaluationCriteriaItem(evaluationCriteriaTreeIdList: string[]) {
        this.evaluationCriteriaTreeIdList = evaluationCriteriaTreeIdList;
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
