<template>
  <div class="edit-team-category-modal" ref="editTeamCategoryModalRef">
    <BasicModal
      @register="register"
      :canFullscreen="false"
      :defaultFullscreen="false"
      :draggable="false"
      :destroyOnClose="true"
      :getContainer="() => $refs.editTeamCategoryModalRef"
      :closable="true"
      :centered="true"
      :maskClosable="false"
      width="60vw"
    >
      <template #title>
        <div>
          <Icon icon="ant-design:edit-twotone" v-if="category === 'edit'" />
          <Icon icon="ant-design:plus-outlined" v-if="category === 'add'" />
          {{ category === 'add' ? '添加小组类型' : '修改小组类型' }}
        </div>
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
              :maxlength="20"
              :autoSize="{ minRows: 2, maxRows: 3 }"
            />
          </FormItem>
        </Form>
      </div>
      <template #footer>
        <Button @click="onCloseModal" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
        <Button
          type="primary"
          color="edit"
          :iconSize="16"
          preIcon="ion:paper-airplane"
          class="ant-btn-left-margin"
          title="提交"
          @click="onClickSubmit"
          style="top: 1px"
        >
          提交
        </Button>
      </template>
    </BasicModal>
  </div>
</template>
<script lang="ts">
  import BasicModal from '/@/components/Modal/src/BasicModal.vue';
  import { Button } from '/@/components/Button';
  import { Loading } from '/@/components/Loading';
  import { Icon } from '/@/components/Icon';
  import { Form, Input } from 'ant-design-vue';
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { useModalInner } from '/@/components/Modal';
  import { apiGetTeamCategoryDetail, apiSaveTeamCategory } from '/@/api/teamCategory/teamCategory';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';

  export default defineComponent({
    components: {
      Loading,
      Icon,
      BasicModal,
      Form,
      FormItem: Form.Item,
      TextArea: Input.TextArea,
      Button,
    },
    setup() {
      const category = ref('add');
      const fullScreenLoading = ref(false);
      const formRef = ref();
      const teamCategoryId = ref();
      const teamCategory = ref();
      const [register, { closeModal }] = useModalInner((data) => {
        teamCategory.value = null;
        category.value = data.category;
        if (data.category === 'edit') {
          teamCategoryId.value = data.teamCategory.id;
          getTeamCategoryDetail();
        } else {
          clearPrams();
        }
      });
      const clearPrams = () => {
        params.name = '';
        params.code = '';
      };
      const initParams = () => {
        params.name = teamCategory.value.name;
        params.code = teamCategory.value.code;
      };
      const getTeamCategoryDetail = () => {
        fullScreenLoading.value = true;
        apiGetTeamCategoryDetail(teamCategoryId.value)
          .then((res) => {
            console.log(res);
            if (res.code === 200) {
              teamCategory.value = res.data;
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
        code: '',
      });
      const formRules = {
        name: [
          {
            required: true,
            trigger: ['blur', 'change'],
            message: '请输入名称',
            whitespace: true,
          },
        ],
      };
      return {
        category,
        fullScreenLoading,
        params,
        ...toRefs(params),
        formRef,
        formRules,
        teamCategory,
        register,
        closeModal,
      };
    },
    methods: {
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
              this.saveTeamCategory();
            },
            onCancel() {},
          });
        });
      },
      preparePrams() {
        console.log('preparePrams ...');
        console.log(this.teamCategory);
        return {
          id: this.teamCategory?.id,
          version: this.teamCategory?.version,
          name: this.params.name,
          code: this.params.code,
        };
      },
      saveTeamCategory() {
        const params = this.preparePrams();
        this.fullScreenLoading = true;
        apiSaveTeamCategory(params)
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
  .edit-team-category-modal {
    ::v-deep(.ant-modal) {
      max-width: calc(100vw) !important;

      .scroll-container .scrollbar__wrap {
        margin-bottom: 0 !important;
      }

      .scrollbar__view {
        height: 50vh;
        overflow: hidden;
      }

      .ant-modal-body {
        height: 100%;

        .scrollbar {
          padding: 0 !important;
          overflow: hidden;
        }
      }

      .content {
        height: 50vh;
        overflow-y: auto;
        padding: 16px;
      }
    }
  }
</style>
