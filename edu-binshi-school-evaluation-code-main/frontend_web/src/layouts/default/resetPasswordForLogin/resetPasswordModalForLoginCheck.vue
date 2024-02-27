<template>
  <div class="reset-password-modal-for-login-check">
    <Loading :loading="loading" />
    <Card class="content">
      <template #title>
        <div style="display: flex">
          <SvgIcon name="password" size="24" style="margin-top: 5px" />
          <span style="margin-left: 8px; font-size: 20px">修改密码</span>
        </div>
      </template>
      <div>
        <Alert
          message="当前为初始密码或重置后的密码，请重新设置"
          type="warning"
          show-icon
          closable
        />
        <Form
          :model="formState"
          autocomplete="off"
          :rules="formRules"
          :label-col="{ style: { width: '80px' } }"
          style="margin-top: 20px"
          @finish="changePassword"
        >
          <FormItem label="新密码" name="newPassword">
            <InputPassword placeholder="请输入密码" v-model:value="newPassword" />
          </FormItem>
          <FormItem label="确认密码" name="verifyNewPassword">
            <InputPassword placeholder="请输入确认密码" v-model:value="verifyNewPassword" />
          </FormItem>
          <FormItem>
            <Row style="margin-top: 10px">
              <Col :span="11">
                <Button type="warning" size="large" block @click="handleLoginOut()">
                  <Icon icon="ic:twotone-arrow-back-ios-new" size="17" />
                  返回
                </Button>
              </Col>
              <Col :span="2" />
              <Col :span="11">
                <Button type="primary" html-type="submit" size="large" block>
                  <Icon icon="ion:md-paper-plane" size="18" />
                  提交
                </Button>
              </Col>
            </Row>
          </FormItem>
        </Form>
      </div>
    </Card>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, toRefs, ref } from 'vue';
  import { Card, Alert, Form, Input, Row, Col } from 'ant-design-vue';
  import { RuleObject } from 'ant-design-vue/lib/form/interface';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { useUserStore } from '/@/store/modules/user';
  import { aipImproveUserPassword } from '/@/api/sys/user';
  import { ImproveUserPasswordParams } from '/@/api/sys/model/userModel';
  import { Loading } from '/@/components/Loading';
  import { Icon, SvgIcon } from '/@/components/Icon';
  export default defineComponent({
    components: {
      Card,
      Alert,
      Form,
      FormItem: Form.Item,
      InputPassword: Input.Password,
      Button,
      Row,
      Col,
      Icon,
      SvgIcon,
      Loading,
    },
    emit: ['resetPasswordSuccess'],
    setup: function () {
      const loading = ref(false);
      const userStore = useUserStore();
      const formState = reactive({
        newPassword: '',
        verifyNewPassword: '',
      });
      const validateNewPassword = async (_rule: RuleObject, value: string | undefined) => {
        if (value === undefined) {
          return Promise.reject('请输入新密码');
        }
        value = value.trim();
        const regex = new RegExp('^(?=.*?\\d)(?=.*?[a-zA-Z])(?=.*?[^\\w\\s]|.*?[_]).{8,30}$');
        if (value === '') {
          return Promise.reject('请输入新密码');
        } else if (/.*[\u4e00-\u9fa5]+.*$/.test(value)) {
          return Promise.reject('密码不能包含中文');
        } else if (!regex.test(value)) {
          return Promise.reject(
            '密码复杂度太低（密码中必须包含字母、数字、特殊字符，至少8个字符，最多30个字符）',
          );
        }
      };
      const validateNewVerifyPassword = async (_rule: RuleObject, value: string | undefined) => {
        if (value === undefined) {
          return Promise.reject('请再次确认密码');
        }
        value = value.trim();
        if (value === '') {
          return Promise.reject('请再次确认密码');
        } else if (value !== formState.newPassword) {
          return Promise.reject('确认密码与新密码不一致');
        }
      };
      const formRules = {
        newPassword: [{ required: true, validator: validateNewPassword, trigger: 'blur' }],
        verifyNewPassword: [
          { required: true, validator: validateNewVerifyPassword, trigger: 'blur' },
        ],
      };
      return {
        formRules,
        ...toRefs(formState),
        formState,
        userStore,
        loading,
      };
    },
    methods: {
      handleLoginOut() {
        useMessage().createConfirm({
          iconType: 'warning',
          title: () => '温馨提示',
          content: () => '是否返回登录页',
          onOk: () => {
            this.userStore.doLogout();
          },
        });
      },
      changePassword() {
        const params: ImproveUserPasswordParams = {
          newPassword: this.newPassword,
          verifyNewPassword: this.verifyNewPassword,
        };
        this.loading = true;
        aipImproveUserPassword(params)
          .then((res) => {
            if (res.code === 200) {
              this.$emit('resetPasswordSuccess');
            } else {
              useMessage().createErrorNotification(
                {
                  message: '错误',
                  description: res.error.message,
                },
                'pre-wrap',
              );
            }
          })
          .catch(() => {
            useMessage().notification.destroy();
            useMessage().createErrorModal({
              title: '网络错误',
              content: '请联系管理员！',
              closable: true,
              maskClosable: false,
              showOkBtn: true,
              showCancelBtn: false,
            });
          })
          .finally(() => {
            this.loading = false;
          });
      },
    },
  });
</script>

<style scoped lang="less">
  .reset-password-modal-for-login-check {
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;

    .content {
      max-width: 500px;
      min-width: 200px;
      width: 34vw;
      box-shadow: 0 0 2px #818181;
      border-radius: 3px;
    }

    ::v-deep(.ant-card-head-title) {
      padding: 10px 0 !important;
    }

    ::v-deep(.ant-card-body) {
      padding: 20px 24px 0 24px !important;
    }
  }
</style>
