<template>
  <template v-if="getShow">
    <LoginFormTitle class="enter-x" />
    <Form class="p-4 enter-x" :model="formData" :rules="getFormRules" ref="formRef">
      <label for="hidden-password"></label>
      <Input id="hidden-password" type="password" hidden autocomplete="new-password" />
      <FormItem name="account" class="enter-x">
        <Input
          size="large"
          v-model:value="formData.account"
          :placeholder="t('sys.login.userName')"
          :onblur="usernameOnblur"
          :style="invalidUsername ? 'box-shadow: 0 0 2px red' : ''"
        />
        <div style="position: absolute; color: red" v-if="invalidUsername"> 请输入账号</div>
      </FormItem>
      <FormItem name="mobile" class="enter-x">
        <Input
          size="large"
          v-model:value="formData.mobile"
          :placeholder="t('sys.login.mobile')"
          :onblur="mobileOnblur"
          :style="invalidMobile || errorMobile ? 'box-shadow: 0 0 2px red' : ''"
        />
        <div style="position: absolute; color: red" v-if="invalidMobile"> 请输入手机号码</div>

        <div style="position: absolute; color: red" v-if="!invalidMobile && errorMobile">
          请输入合法的手机号</div
        >
      </FormItem>
      <FormItem name="sms" class="enter-x">
        <CountdownInput
          size="large"
          v-model:value="formData.sms"
          :count="60"
          :sendCodeApi="sendMessage"
          :placeholder="t('sys.login.smsCode')"
          :onblur="smsCodeOnblur"
          :class="invalidSmsCode ? 'sms-code' : ''"
        />
        <div
          style="position: absolute; color: red"
          v-if="invalidSmsCode && unref(formData).account && unref(formData).mobile"
        >
          请输入验证码</div
        >
      </FormItem>
      <FormItem name="password" class="enter-x">
        <InputPassword
          size="large"
          visibilityToggle
          v-model:value="formData.newPassword"
          :placeholder="'请输入新密码'"
          :onblur="passwordOnblur"
          :style="invalidPassword || chinesePassword ? 'box-shadow: 0 0 2px red' : ''"
        />
        <div style="position: absolute; color: red" v-if="invalidPassword"> 请输入新密码</div>
        <div style="position: absolute; color: red" v-if="!invalidPassword && chinesePassword">
          密码不能包含中文</div
        >
        <div
          style="color: red; max-width: fit-content"
          v-if="!invalidPassword && !chinesePassword && pwdTooEasy"
        >
          您的密码复杂度太低（密码中必须包含字母、数字、特殊字符，至少8个字符，最多30个字符），请修改密码！</div
        >
      </FormItem>
      <FormItem name="password" class="enter-x">
        <InputPassword
          size="large"
          visibilityToggle
          v-model:value="formData.verifyPassword"
          :placeholder="'请再次输入密码'"
          :onblur="verifyPasswordOnblur"
          :style="invalidVerifyPassword || passwordNotMatch ? 'box-shadow: 0 0 2px red' : ''"
        />
        <div style="position: absolute; color: red" v-if="invalidVerifyPassword">
          请再次输入密码</div
        >
        <div
          style="position: absolute; color: red"
          v-if="!invalidVerifyPassword && passwordNotMatch"
        >
          密码不一致</div
        >
      </FormItem>

      <FormItem class="enter-x">
        <Button type="primary" size="large" block @click="handleReset" :loading="loading">
          {{ t('common.okText') }}
        </Button>
        <Button size="large" block class="mt-4" @click="customHandleBackLogin">
          {{ t('sys.login.backSignIn') }}
        </Button>
      </FormItem>
    </Form>
  </template>
</template>
<script lang="ts" setup>
  import { reactive, ref, computed, unref } from 'vue';
  import LoginFormTitle from './LoginFormTitle.vue';
  import { Form, Input, message, Button } from 'ant-design-vue';
  import { CountdownInput } from '/@/components/CountDown';
  import { useI18n } from '/@/hooks/web/useI18n';
  import { useLoginState, useFormRules, LoginStateEnum } from './useLogin';
  import { useMessage } from '/@/hooks/web/useMessage';
  import _ from 'lodash';
  const FormItem = Form.Item;
  const { t } = useI18n();
  const { handleBackLogin, getLoginState } = useLoginState();
  const { getFormRules } = useFormRules();
  const InputPassword = Input.Password;

  const formRef = ref();
  const loading = ref(false);

  const formData = reactive({
    account: '',
    mobile: '',
    sms: '',
    newPassword: '',
    verifyPassword: '',
  });
  // const newPassword = ref('');
  const getShow = computed(() => unref(getLoginState) === LoginStateEnum.RESET_PASSWORD);

  function verifyFormValue() {
    const form = unref(formData);
    if (!form.account) {
      message.destroy();
      // message.error('请输入账号');
      invalidUsername.value = true;
      return false;
    }

    if (!form.mobile) {
      message.destroy();
      // message.error('请输入账号');
      invalidMobile.value = true;
      return false;
    }

    const flag = /^[1][3,4,5,7,8,9][0-9]{9}$/;
    if (!flag.test(form.mobile)) {
      message.destroy();
      // message.error('请输入合法的手机号');
      errorMobile.value = true;
      return false;
    }

    if (!form.sms) {
      message.destroy();
      // message.error('请输入验证码');
      invalidSmsCode.value = true;
      return false;
    }
    if (!form.newPassword) {
      message.destroy();
      // message.error('请输入新的密码');
      invalidPassword.value = true;
      return false;
    }
    if (form.verifyPassword === '') {
      message.destroy();
      // message.error(msg);
      invalidVerifyPassword.value = true;
      return false;
    }
    if (form.verifyPassword !== form.newPassword) {
      // const msg = '密码不一致！';
      message.destroy();
      // message.error(msg);
      passwordNotMatch.value = true;
      return false;
    }
    if (/.*[\u4e00-\u9fa5]+.*$/.test(form.newPassword)) {
      // const msg = '密码不能包含中文';
      message.destroy();
      // message.error(msg);
      chinesePassword.value = true;
      return false;
    }
    const regex = new RegExp('(?=.*?\\d)(?=.*?[a-zA-Z])(?=.*?[^\\w\\s]|.*?[_]).{8,30}');
    if (!regex.test(form.newPassword)) {
      pwdTooEasy.value = true;
      return false;
    }
    return true;
  }

  async function handleReset() {
    const form = unref(formData);
    const verifyValue = verifyFormValue();
    if (!verifyValue) {
      return;
    }
    const res = await apiForgetPasswordToReset(
      form.sms,
      form.mobile,
      form.newPassword,
      form.account,
    );
    if (res.code == 200) {
      useMessage().createSuccessNotification({
        message: '操作成功',
        description: '密码重置成功',
      });
      resetData();
      handleBackLogin();
    } else {
      useMessage().createErrorNotification({
        message: '操作失败',
        description: res.error.message,
      });
    }
    // await form.resetFields();
  }

  async function sendMessage() {
    const form = unref(formData);
    if (!form.account) {
      message.destroy();
      // message.error('请输入账号');
      invalidUsername.value = true;
      return false;
    }
    if (!form.mobile) {
      message.destroy();
      invalidMobile.value = true;
      return false;
    }
    const flag = /^[1][3,4,5,7,8,9][0-9]{9}$/;
    if (!flag.test(form.mobile)) {
      message.destroy();
      // message.error('请输入合法的手机号');
      errorMobile.value = true;
      return false;
    }
    const res = await apiGetVerificationCode(form.mobile, form.account);
    if (res.data.code === 200) {
      return true;
    } else {
      useMessage().createErrorNotification({
        message: '操作失败',
        description: res.data.error.message,
      });
      return false;
    }
  }

  const invalidUsername = ref(false);
  const usernameOnblur = () => {
    invalidUsername.value = !formData.account || !_.trim(formData.account);
  };

  const invalidMobile = ref(false);
  const errorMobile = ref(false);
  const mobileOnblur = () => {
    invalidMobile.value = !formData.mobile || !_.trim(formData.mobile);
    const flag = /^[1][3,4,5,7,8,9][0-9]{9}$/;
    errorMobile.value = !flag.test(formData.mobile);
  };

  const invalidSmsCode = ref(false);
  const smsCodeOnblur = () => {
    invalidSmsCode.value = !formData.sms || !_.trim(formData.sms);
  };

  const passwordNotMatch = ref(false);
  const invalidPassword = ref(false);
  const invalidVerifyPassword = ref(false);
  const chinesePassword = ref(false);
  const pwdTooEasy = ref(false);

  const passwordOnblur = () => {
    invalidPassword.value = !formData.newPassword || !_.trim(formData.newPassword);
    passwordNotMatch.value =
      !invalidPassword.value &&
      !(!formData.verifyPassword || !_.trim(formData.verifyPassword)) &&
      formData.newPassword !== formData.verifyPassword;
    chinesePassword.value = /.*[\u4e00-\u9fa5]+.*$/.test(formData.newPassword);

    const regex = new RegExp('(?=.*?\\d)(?=.*?[a-zA-Z])(?=.*?[^\\w\\s]|.*?[_]).{8,30}');
    pwdTooEasy.value = !regex.test(formData.newPassword);
  };

  const verifyPasswordOnblur = () => {
    invalidVerifyPassword.value = !formData.verifyPassword || !_.trim(formData.verifyPassword);
    passwordNotMatch.value =
      !invalidPassword.value &&
      !invalidVerifyPassword.value &&
      formData.newPassword !== formData.verifyPassword;
  };
  const resetData = () => {
    invalidUsername.value = false;
    invalidMobile.value = false;
    errorMobile.value = false;
    invalidSmsCode.value = false;
    passwordNotMatch.value = false;
    invalidPassword.value = false;
    invalidVerifyPassword.value = false;
    chinesePassword.value = false;
    pwdTooEasy.value = false;
    formData.account = '';
    formData.mobile = '';
    formData.sms = '';
    formData.newPassword = '';
    formData.verifyPassword = '';
  };
  const customHandleBackLogin = () => {
    resetData();
    handleBackLogin();
  };
</script>
<style lang="less" scoped>
  .sms-code > span > #sms {
    box-shadow: 0 0 2px red;
  }
</style>
