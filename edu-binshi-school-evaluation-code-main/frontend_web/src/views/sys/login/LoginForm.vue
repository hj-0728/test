<template>
  <AppLogoV2 class="enter-x -mt-18" />
  <Divider style="border-top: none" />
  <Form
    class="p-4 enter-x"
    :model="formData"
    :rules="getFormRules"
    ref="formRef"
    v-show="getShow"
    @keypress.enter="handleLogin"
  >
    <FormItem name="account" class="enter-x">
      <Input
        size="large"
        v-model:value="formData.account"
        :placeholder="t('sys.login.userName')"
        class="fix-auto-fill"
      />
    </FormItem>
    <FormItem name="password" class="enter-x">
      <InputPassword
        size="large"
        visibilityToggle
        v-model:value="formData.password"
        :placeholder="t('sys.login.password')"
      />
    </FormItem>
    <ARow>
      <ACol :span="16">
        <FormItem name="validateCode" class="enter-x">
          <Input
            size="large"
            class="validate-code-input"
            style="width: calc(100% - 5px) !important; min-width: 100px"
            v-model:value="formData.validateCode"
            placeholder="图片验证码（忽略大小写）"
          />
        </FormItem>
      </ACol>
      <ACol :span="8">
        <Tooltip title="看不清？点击图片换一张">
          <div>
            <img
              class="enter-x"
              :src="formData.validateImageSrc"
              style="width: 100%; height: 40px"
              @click="getValidateImage"
              alt=""
            />
          </div>
        </Tooltip>
      </ACol>
    </ARow>

    <FormItem class="enter-x">
      <Button type="primary" size="large" block @click="handleLogin" :loading="loading">
        {{ t('sys.login.loginButton') }}
      </Button>
    </FormItem>
  </Form>
</template>
<script lang="ts" setup>
  import { reactive, ref, unref, computed, toRaw, onMounted } from 'vue';

  import { Form, Input, Button, Row, Col, Tooltip, Divider } from 'ant-design-vue';
  import { apiGetLoginValidateImage } from '/@/api/sys/user';
  import { useI18n } from '/@/hooks/web/useI18n';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { AppLogoV2 } from '/@/components/Application';
  import { useUserStore } from '/@/store/modules/user';
  import { LoginStateEnum, useLoginState, useFormRules, useFormValid } from './useLogin';
  import { useDesign } from '/@/hooks/web/useDesign';
  const ACol = Col;
  const ARow = Row;
  const FormItem = Form.Item;
  const InputPassword = Input.Password;
  const { t } = useI18n();
  const { createErrorModal } = useMessage();
  const { prefixCls } = useDesign('login');
  const userStore = useUserStore();

  const { getLoginState } = useLoginState();
  const { getFormRules } = useFormRules();

  const formRef = ref();
  const loading = ref(false);

  const formData = reactive({
    account: '',
    password: '',
    validateCode: '',
    validateImageSrc: '',
  });
  async function getValidateImage() {
    const data = await apiGetLoginValidateImage();
    if (data.code === 200) {
      formData.validateImageSrc = data.data;
      formRef.value.resetFields('validateCode');
    }
  }
  onMounted(() => {
    getValidateImage();
  });

  const { validForm } = useFormValid(formRef);
  const getShow = computed(() => unref(getLoginState) === LoginStateEnum.LOGIN);
  async function handleLogin() {
    if (loading.value) {
      return;
    }
    const data = await validForm();
    if (!data) return;
    try {
      loading.value = true;
      const loginRes = await userStore.login(
        toRaw({
          password: data.password,
          name: data.account,
          validateCode: data.validateCode,
          validateImageSrc: formData.validateImageSrc,
          mode: 'none', //不要默认的错误提示
        }),
      );
      if (typeof loginRes === 'boolean' && !loginRes) {
        await getValidateImage();
      }
    } catch (error) {
      const obj = document.getElementsByClassName('network-error');
      if (obj !== undefined && obj !== null) {
        if (obj.length === 0) {
          useMessage().destroyAll();
          createErrorModal({
            title: t('sys.api.errorTip'),
            content: (error as unknown as Error).message || t('sys.api.networkExceptionMsg'),
            getContainer: () => document.body.querySelector(`.${prefixCls}`) || document.body,
            class: 'network-error',
          } as any);
        }
      }
      await getValidateImage();
    } finally {
      loading.value = false;
    }
  }
</script>
