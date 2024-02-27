<template>
  <BasicModal
    v-bind="$attrs"
    @register="register"
    :title="action === 'create' ? '添加菜单' : '编辑菜单'"
    :destroyOnClose="true"
    width="60%"
  >
    <div class="m-4">
      <BasicForm
        @register="registerForm"
        v-if="onClickMenu"
        :labelWidth="100"
        :schemas="schemas"
        :actionColOptions="{ span: 24 }"
        :show-action-button-group="false"
        :submitButtonOptions="{ text: '提交' }"
        @submit="onSubmitEditMenuForm"
      />
    </div>

    <template #footer>
      <div style="display: flex; justify-content: flex-end; align-items: center">
        <Button
          type="primary"
          style="display: flex; justify-content: center; align-items: center"
          @click="onClickSaveMenu"
        >
          <div style="margin-top: 2px">
            <Icon icon="mdi:content-save-outline" size="16" />
          </div>
          <span style="margin-left: 10px">保存</span>
        </Button>
      </div>
    </template>
  </BasicModal>
</template>
<script lang="ts">
  import { createVNode, defineComponent, ref } from 'vue';
  import { BasicForm, FormSchema, useForm } from '/@/components/Form';
  import { apiAddMenu, apiEditMenu } from '/@/api/menu/menu';
  import { Modal } from 'ant-design-vue';
  import { ExclamationCircleOutlined } from '@ant-design/icons-vue';
  import { useTabs } from '/@/hooks/web/useTabs';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Icon } from '/@/components/Icon';
  import { Button } from 'ant-design-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { TRANSITION_NAME, MASK_TRANSITION_NAME } from '/@/settings/transitionSetting';
  export default defineComponent({
    components: { BasicModal, BasicForm, Icon, Button },
    setup() {
      const onClickMenu = ref({});
      const schemas: FormSchema[] = ref([]);
      const action = ref('');
      const parentId = ref('');
      const { refreshPage } = useTabs();
      const [register, { closeModal }] = useModalInner();
      const [registerForm, { getFieldsValue }] = useForm();
      return {
        schemas,
        onClickMenu,
        action,
        parentId,
        register,
        closeModal,
        refreshPage,
        registerForm,
        getFieldsValue,
        TRANSITION_NAME,
        MASK_TRANSITION_NAME,
      };
    },
    methods: {
      prepareFormFiledSchema(action) {
        this.action = action;
        let defaultValue = {};
        if (action === 'edit') {
          defaultValue = this.onClickMenu;
        }
        this.schemas.length = 0;
        this.schemas = [
          {
            field: 'name',
            component: 'Input',
            label: '名称',
            required: true,
            defaultValue: defaultValue.name,
            colProps: {
              span: 20,
            },
          },
          {
            field: 'path',
            component: 'Input',
            label: '路径',
            required: true,
            defaultValue: defaultValue.path,
            colProps: {
              span: 20,
            },
          },
          {
            field: 'icon',
            component: 'Input',
            label: 'icon',
            required: true,
            defaultValue: defaultValue.icon,
            colProps: {
              span: 20,
            },
          },
        ];
      },
      onSubmitEditMenuForm(params) {
        Modal.confirm({
          transitionName: this.TRANSITION_NAME,
          maskTransitionName: this.MASK_TRANSITION_NAME,
          title: () => '确定要提交吗？',
          centered: true,
          icon: () => createVNode(ExclamationCircleOutlined),
          onOk: () => {
            if (this.action == 'create') {
              this.addMenu(params);
            } else if (this.action === 'edit') {
              this.editMenu(params);
            }
          },
        });
      },
      addMenu(params) {
        if (this.onClickMenu.key !== '#') {
          params['parentId'] = this.onClickMenu.key;
        }
        apiAddMenu(params)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '操作成功',
                description: '添加成功',
              });
              setTimeout(() => {
                this.refreshPage();
              }, 2000);
            } else {
              useMessage().createErrorNotification({
                message: '操作失败',
                description: res.error.message,
              });
            }
          })
          .catch(() => {
            useMessage().createErrorModal({
              title: '操作失败',
              content: '网络异常，请检查您的网络连接是否正常!',
              closable: true,
              maskClosable: false,
              showOkBtn: true,
              showCancelBtn: false,
            });
          });
      },

      editMenu(params) {
        params['id'] = this.onClickMenu.id;
        params['version'] = this.onClickMenu.version;
        apiEditMenu(params)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '操作成功',
                description: '修改成功',
              });
              setTimeout(() => {
                this.refreshPage();
              }, 2000);
            } else {
              useMessage().createErrorNotification({
                message: '操作失败',
                description: res.error.message,
              });
            }
          })
          .catch(() => {
            useMessage().createErrorModal({
              title: '操作失败',
              content: '网络异常，请检查您的网络连接是否正常!',
              closable: true,
              maskClosable: false,
              showOkBtn: true,
              showCancelBtn: false,
            });
          });
      },

      onClickSaveMenu() {
        const menu = this.getFieldsValue();
        console.log(menu);
        if (!menu.name) {
          useMessage().createErrorNotification({
            message: '操作失败',
            description: '请输入菜单名称',
          });
          return;
        }
        if (!menu.path) {
          useMessage().createErrorNotification({
            message: '操作失败',
            description: '请输入菜单路径',
          });
          return;
        }
        if (!menu.icon) {
          useMessage().createErrorNotification({
            message: '操作失败',
            description: '请输入菜单icon',
          });
          return;
        }
        this.onSubmitEditMenuForm(menu);
      },
    },
  });
</script>
