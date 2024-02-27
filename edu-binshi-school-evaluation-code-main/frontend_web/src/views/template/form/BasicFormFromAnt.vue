<template>
  <div>
    <Form
      :model="formState"
      name="basic"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 14 }"
      autocomplete="off"
      @finishFailed="onFinishFailed"
      ref="formRef"
    >
      <FormItem
        label="Username"
        name="username"
        :rules="[{ required: true, message: 'Please input your username!' }]"
      >
        <Input v-model:value="formState.username" />
      </FormItem>

      <FormItem
        label="Password"
        name="password"
        :rules="[{ required: true, message: 'Please input your password!' }]"
      >
        <InputPassword v-model:value="formState.password" />
      </FormItem>
      <FormItem name="remember" :wrapper-col="{ offset: 6, span: 14 }">
        <Checkbox v-model:checked="formState.remember">Remember me</Checkbox>
      </FormItem>

      <FormItem :wrapper-col="{ offset: 6, span: 14 }">
        <Button type="primary" @click="clickInfo">Info</Button>
        <Button color="error" @click="clickError" class="ant-btn-left-margin">Error</Button>
        <Button color="warning" @click="clickWarning" class="ant-btn-left-margin">Warning</Button>
        <Button color="success" @click="clickSuccess" class="ant-btn-left-margin">Success</Button>
      </FormItem>
    </Form>
    <Loading :loading="loading" />
  </div>
</template>
<script lang="ts">
  import { Form, Input, Checkbox } from 'ant-design-vue';
  import { defineComponent, reactive, ref } from 'vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { Button } from '/@/components/Button';
  import { Loading } from '/@/components/Loading';
  interface FormState {
    username: string;
    password: string;
    remember: boolean;
  }
  export default defineComponent({
    components: {
      Form,
      FormItem: Form.Item,
      Input,
      InputPassword: Input.Password,
      Checkbox,
      Button,
      Loading,
    },
    setup() {
      const formState = reactive<FormState>({
        username: '',
        password: '',
        remember: true,
      });
      const formRef = ref();

      const onFinishFailed = (errorInfo: any) => {
        console.log('Failed:', errorInfo);
      };
      const loading = ref(false);
      return {
        formState,
        onFinishFailed,
        loading,
        formRef,
      };
    },
    methods: {
      clickInfo() {
        useMessage().createInfoNotification({
          message: 'Tip',
          description: 'content message...',
        });
      },
      clickError() {
        useMessage().createErrorNotification({
          message: 'Tip',
          description: 'content message...',
        });
      },
      clickWarning() {
        useMessage().createWarningNotification({
          message: 'Tip',
          description: 'content message...',
        });
      },
      clickSuccess() {
        useMessage().createSuccessNotification({
          message: 'Tip',
          description: 'content message...',
        });
      },
      onSubmit() {
        this.formRef.validateFields().then(() => {
          useMessage().createSuccessNotification({
            message: 'Tip',
            description: 'content message...',
          });
        });
      },
    },
  });
</script>

<style scoped></style>
