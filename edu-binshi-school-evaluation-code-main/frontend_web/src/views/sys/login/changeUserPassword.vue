<template>
  <BasicModal
    v-bind="$attrs"
    :showOkBtn="false"
    :showCancelBtn="false"
    :canFullscreen="false"
    :destroyOnClose="true"
    :afterClose="initParams"
    :draggable="false"
    @register="register"
    width="35%"
  >
    <template #title>
      <div>
        <KeyOutlined />
        修改密码
      </div>
    </template>
    <template #footer>
      <div style="display: flex; justify-content: flex-end; align-items: center">
        <Button @click="closeModal" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
        <Button
          type="primary"
          color="edit"
          style="display: flex; justify-content: center; align-items: center"
          @click="changePassword"
        >
          <Icon icon="ion:paper-airplane" />
          <span style="margin-left: 10px">确认</span>
        </Button>
      </div>
    </template>
    <Form
      class="p-4 enter-x"
      :model="inpValue"
      :rules="rules"
      ref="formRef"
      :label-col="{ span: 4 }"
    >
      <FormItem label="原密码" name="password" class="enter-x">
        <InputPassword v-model:value="password" :placeholder="'请输入原密码'" />
      </FormItem>
      <FormItem label="新密码" name="newPassword" class="enter-x">
        <InputPassword v-model:value="newPassword" :placeholder="'请输入新密码'" />
      </FormItem>
      <FormItem label="确认密码" name="verifyNewPassword" class="enter-x">
        <InputPassword v-model:value="verifyNewPassword" :placeholder="'请输入确认密码'" />
      </FormItem>
    </Form>
  </BasicModal>
</template>
<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { Input, Form, Modal } from 'ant-design-vue';
  import { aipChangePassword } from '/@/api/sys/user';
  import { useUserStore } from '/@/store/modules/user';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { useAppStore } from '/@/store/modules/app';
  import { KeyOutlined } from '@ant-design/icons-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { RuleObject } from 'ant-design-vue/lib/form/interface';
  import { Icon } from '/@/components/Icon';
  import { Button } from '/@/components/Button';

  export default defineComponent({
    components: {
      Button,
      InputPassword: Input.Password,
      BasicModal,
      KeyOutlined,
      Form,
      FormItem: Form.Item,
      Icon,
    },
    setup() {
      const appStore = useAppStore();
      const formRef = ref();
      const inpValue = reactive({
        password: '',
        newPassword: '',
        verifyNewPassword: '',
      });

      const userStore = useUserStore();

      const validatePassword = async (_rule: RuleObject, value: string) => {
        if (value.trim() === '') {
          return Promise.reject('请输入原密码');
        }
      };

      const validateNewPassword = async (_rule: RuleObject, value: string) => {
        value = value.trim();
        const regex = new RegExp('(?=.*?\\d)(?=.*?[a-zA-Z])(?=.*?[^\\w\\s]|.*?[_]).{8,30}');
        if (value === '') {
          return Promise.reject('请输入新密码。');
        } else if (/.*[\u4e00-\u9fa5]+.*$/.test(value)) {
          return Promise.reject('密码不能包含中文。');
        } else if (!regex.test(value)) {
          return Promise.reject(
            '密码复杂度太低（密码中必须包含字母、数字、特殊字符，至少8个字符，最多30个字符）。',
          );
        } else if (value === inpValue.password) {
          return Promise.reject('输入的新密码与原密码一致。');
        }
      };

      const validateVerifyNewPassword = async (_rule: RuleObject, value: string) => {
        value = value.trim();
        if (value === '') {
          return Promise.reject('请输入确认密码。');
        } else if (value !== inpValue.newPassword) {
          return Promise.reject('新密码和确认密码不一致。');
        }
      };

      const rules = {
        password: [{ required: true, validator: validatePassword, trigger: 'blur' }],
        newPassword: [{ required: true, validator: validateNewPassword, trigger: 'blur' }],
        verifyNewPassword: [
          {
            required: true,
            validator: validateVerifyNewPassword,
            trigger: 'blur',
          },
        ],
      };

      const [register, { closeModal }] = useModalInner();

      return {
        inpValue,
        userStore,
        appStore,
        rules,
        formRef,
        ...toRefs(inpValue),
        register,
        closeModal,
      };
    },
    created() {
      this.initParams();
    },
    methods: {
      initParams() {
        this.password = '';
        this.newPassword = '';
        this.verifyNewPassword = '';
      },
      changePassword() {
        console.log(this.password);
        console.log(this.newPassword);
        console.log(this.verifyNewPassword);
        this.formRef
          .validate()
          .then(async () => {
            const params = {
              password: this.password,
              newPassword: this.newPassword,
              verifyNewPassword: this.verifyNewPassword,
            };
            aipChangePassword(params)
              .then((res) => {
                if (res.code === 200) {
                  this.appStore.setUpdatePasswordStatus('');
                  this.userStore.logout(true).then(() => {
                    useMessage().createSuccessNotification({
                      message: '密码修改成功',
                      description: '请重新登录',
                    });
                    setTimeout(() => {
                      Modal.destroyAll();
                    }, 2000);
                  });
                } else {
                  useMessage().createErrorNotification({
                    message: '操作失败',
                    description: res.error.message,
                  });
                }
              })
              .catch((error) => {
                console.log(error);
                useMessage().createErrorModal({
                  title: '操作失败',
                  content: '网络异常，请检查您的网络连接是否正常!',
                  closable: true,
                  maskClosable: false,
                  showOkBtn: true,
                  showCancelBtn: false,
                });
              });
          })
          .catch((error) => {
            console.log('error', error);
          });
      },
    },
  });
</script>
<style lang="less" scoped></style>
