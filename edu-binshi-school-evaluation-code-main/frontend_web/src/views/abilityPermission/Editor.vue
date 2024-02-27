<template>
  <BasicModal
    v-bind="$attrs"
    @register="register"
    :title="action === 'create' ? '添加功能权限' : '编辑功能权限'"
    :destroyOnClose="true"
    width="60%"
  >
    <div class="m-4">
      <BasicForm
        @register="registerForm"
        v-if="onClickAbilityPermission"
        :labelWidth="100"
        :schemas="schemas"
        :actionColOptions="{ span: 24 }"
        :show-action-button-group="false"
        @submit="onSubmitEditAbilityPermissionForm"
      />
    </div>

    <template #footer>
      <div style="display: flex; justify-content: flex-end; align-items: center">
        <Button
          type="primary"
          style="display: flex; justify-content: center; align-items: center"
          @click="onClickSaveAbilityPermission"
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
  import { useMessage } from '/@/hooks/web/useMessage';
  import { useTabs } from '/@/hooks/web/useTabs';
  import {
    apiCreateAbilityPermission,
    apiEditAbilityPermission,
  } from '/@/api/abilityPermission/abilityPermission';
  import { Modal, Button } from 'ant-design-vue';
  import { ExclamationCircleOutlined } from '@ant-design/icons-vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Icon } from '/@/components/Icon';
  import { TRANSITION_NAME, MASK_TRANSITION_NAME } from '/@/settings/transitionSetting';
  export default defineComponent({
    components: { BasicModal, BasicForm, Icon, Button },
    setup() {
      const onClickAbilityPermission = ref({});
      const schemas: FormSchema[] = ref([]);
      const action = ref('');
      const { refreshPage } = useTabs();
      const [register] = useModalInner();
      const [registerForm, { getFieldsValue }] = useForm();
      return {
        schemas,
        onClickAbilityPermission,
        register,
        registerForm,
        getFieldsValue,
        action,
        refreshPage,
        TRANSITION_NAME,
        MASK_TRANSITION_NAME,
      };
    },
    methods: {
      prepareFormFiledSchema(action) {
        this.action = action;
        let defaultValue = {};
        if (action === 'edit') {
          defaultValue = this.onClickAbilityPermission;
        }
        this.schemas.length = 0;
        const schemas = [
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
            field: 'code',
            component: 'Input',
            label: '编码',
            required: true,
            defaultValue: defaultValue.code,
            colProps: {
              span: 20,
            },
          },
        ];
        if (
          action === 'create' &&
          this.onClickAbilityPermission.id &&
          this.onClickAbilityPermission.id !== '#'
        ) {
          schemas.push({
            field: 'is_permission',
            component: 'Checkbox',
            label: '是否为权限',
            defaultValue: this.onClickAbilityPermission.node_type === 'ability_permission',
            colProps: {
              span: 20,
            },
          });
        }
        this.schemas = schemas;
      },
      onSubmitEditAbilityPermissionForm(params) {
        Modal.confirm({
          transitionName: this.TRANSITION_NAME,
          maskTransitionName: this.MASK_TRANSITION_NAME,
          title: () => '确定要提交吗？',
          centered: true,
          icon: () => createVNode(ExclamationCircleOutlined),
          onOk: () => {
            if (this.action == 'create') {
              this.createAbilityPermission(params);
            } else if (this.action === 'edit') {
              this.editAbilityPermission(params);
            }
          },
        });
      },
      createAbilityPermission(params) {
        if (this.onClickAbilityPermission.key !== '#') {
          params['parent_id'] = this.onClickAbilityPermission.key;
        }
        apiCreateAbilityPermission(params)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '操作成功',
                description: '创建成功',
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

      editAbilityPermission(params) {
        params['id'] = this.onClickAbilityPermission.id;
        params['version'] = this.onClickAbilityPermission.version;
        params['node_type'] = this.onClickAbilityPermission.node_type;
        apiEditAbilityPermission(params)
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

      onClickSaveAbilityPermission() {
        const permission = this.getFieldsValue();
        if (!permission.name) {
          useMessage().createErrorNotification({
            message: '操作失败',
            description: '请输入名称',
          });
          return;
        }
        this.onSubmitEditAbilityPermissionForm(permission);
      },
    },
  });
</script>
