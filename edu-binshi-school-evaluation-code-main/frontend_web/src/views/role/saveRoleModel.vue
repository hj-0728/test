<template>
  <BasicModal
    v-bind="$attrs"
    @register="register"
    @visible-change="handleVisibleChange"
    width="60%"
  >
    <template #title>
      <div v-if="!disabledCode">
        <PlusSquareOutlined />
        添加角色
      </div>
      <div v-else>
        <EditOutlined />
        编辑角色
      </div>
    </template>
    <BasicForm
      @register="registerForm"
      :labelWidth="100"
      :label-col="{ span: 6 }"
      :schemas="schemas"
      :actionColOptions="{ span: 24 }"
      :showActionButtonGroup="false"
      ref="formRef"
      :key="basicFormRefreshKey"
    />

    <template #footer>
      <div style="display: flex; justify-content: flex-end; align-items: center">
        <Button
          type="primary"
          style="display: flex; justify-content: center; align-items: center"
          @click="submitButton"
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
  import { defineComponent, reactive, ref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { BasicForm, FormSchema, useForm } from '/@/components/Form';
  import { roleInfoApi, SaveRoleApi } from '/@/api/role/role';
  import { Button } from 'ant-design-vue';
  import { useTabs } from '/@/hooks/web/useTabs';
  import { getCurrentOrganization } from '/@/utils/helper/common';
  import { Icon } from '/@/components/Icon';
  import { PlusSquareOutlined, EditOutlined } from '@ant-design/icons-vue';
  import { useMessage } from '/@/hooks/web/useMessage';

  export default defineComponent({
    components: { BasicModal, BasicForm, Icon, Button, PlusSquareOutlined, EditOutlined },
    setup() {
      const formRef = ref();
      const disabledCode = ref(true);
      const basicFormRefreshKey = ref(new Date().getTime());
      const schemas: FormSchema[] = [
        {
          field: 'id',
          component: 'Input',
          label: '编号',
          colProps: {
            span: 20,
          },
          ifShow: false,
        },
        {
          defaultValue: '1',
          field: 'version',
          component: 'Input',
          label: '版本',
          colProps: {
            span: 20,
          },
          ifShow: false,
        },
        {
          field: 'name',
          component: 'Input',
          label: '名称',
          colProps: {
            span: 20,
          },
          required: true,
          defaultValue: '',
          componentProps: {
            placeholder: '请输入名称',
          },
        },
        {
          field: 'code',
          component: 'Input',
          label: '编码',
          colProps: {
            span: 20,
          },
          required: true,
          defaultValue: '',
          componentProps: {
            placeholder: '请输入编码',
            disabled: disabledCode.value,
          },
        },
        {
          field: 'comments',
          component: 'InputTextArea',
          label: '描述',
          colProps: {
            span: 20,
          },
          defaultValue: '',
          componentProps: {
            placeholder: '请输入描述',
          },
        },
        {
          field: 'isActivated',
          component: 'Switch',
          label: '状态',
          defaultValue: true,
          colProps: {
            span: 20,
          },
          componentProps: {
            onChange: (e: any) => {
              roleInfo.isActivated = e;
            },
          },
        },
      ];
      const masterDimensionList = ref<string[]>([]);
      const currentOrganization = getCurrentOrganization();
      const roleInfo = reactive<any>({
        id: '',
        version: 1,
        name: '',
        code: '',
        comments: '',
        isActivated: false,
      });
      const okText = ref<string>('保存');
      const getRoleInfo = async (roleId) => {
        await roleInfoApi(roleId).then((res) => {
          console.log('这个是获取页面数据的函数啊！------------->', res.data);
          setFieldsValue({
            id: res.data.id,
            version: res.data.version,
            name: res.data.name,
            code: res.data.code,
            comments: res.data.comments,
            isActivated: res.data.isActivated,
          });
        });
      };
      const callBack = async (data) => {
        disabledCode.value = data.event !== 'add';
        basicFormRefreshKey.value = new Date().getTime();
        console.log('看这里', basicFormRefreshKey.value);
        schemas[3] = {
          field: 'code',
          component: 'Input',
          label: '编码',
          colProps: {
            span: 20,
          },
          required: true,
          defaultValue: '',
          componentProps: {
            placeholder: '请输入编码',
            disabled: disabledCode.value,
          },
        };
        setModalProps({ title: data.title });
        if (data.roleId) {
          await getRoleInfo(data.roleId);
        } else {
          await resetFields();
        }
      };
      const [register, { closeModal, setModalProps }] = useModalInner(callBack);
      const [registerForm, { setFieldsValue, resetFields, getFieldsValue }] = useForm({
        labelWidth: 120,
        schemas,
        showActionButtonGroup: false,
        actionColOptions: {
          span: 24,
        },
      });
      const { refreshPage } = useTabs();
      return {
        formRef,
        register,
        closeModal,
        setModalProps,
        callBack,
        masterDimensionList,
        roleInfo,
        currentOrganization,
        schemas,
        registerForm,
        resetFields,
        getFieldsValue,
        okText,
        refreshPage,
        basicFormRefreshKey,
        disabledCode,
      };
    },
    methods: {
      handleVisibleChange(visible) {
        console.log(visible);
      },
      submitButton() {
        this.roleInfo = this.getFieldsValue();
        this.formRef.validateFields().then(() => {
          SaveRoleApi(this.roleInfo)
            .then((res) => {
              if (res.code === 200) {
                useMessage().createSuccessNotification({
                  message: '修改成功',
                });
                this.closeModal();
                setTimeout(() => {
                  this.refreshPage();
                }, 1000);
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
        });
      },
    },
  });
</script>
