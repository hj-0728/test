import { Button, Container, LoadingOverlay, Paper, PasswordInput, TextInput, Title, Grid, Tooltip, Image } from '@mantine/core';
import { useForm } from '@mantine/form';
import { useRouter } from 'next/router';
import React, {useEffect, useState} from 'react';
import {apiGetCurrentUserInfo, apiGetLoginValidateImage, apiGetUserSidebarMenu, apiLogin} from '@/api/AuthApi';
import { showErrorNotification } from '@/components/BasicNotifications';
import useAppState from '@/store/app';
import AuthLayout from '../../layouts/authLayout';

function SignInPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [imageSrc, setImageSrc] = useState('');
  const form = useForm({
    initialValues: {
      name: '',
      password: '',
      validateCode: '',
      validateImageSrc: '',
    },

    validate: {
      name: (value) => (value ? null : '用户名不能为空'),
      password: (value) => (value ? null : '密码不能为空'),
      validateCode: (value) => (value ? null : '图片验证码不能为空'),
    },
  });

  const loadUserSidebarMenu = async () => {
    try {
      const res = await apiGetUserSidebarMenu();
      if (res.code === 200) {
        useAppState.setState({ navbarMenu: res.data });
      } else {
        showErrorNotification(res.error!.message);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const loadCurrentUserInfo = async () => {
    try {
      const res = await apiGetCurrentUserInfo();
      if (res.code === 200) {
        useAppState.setState({ userInfo: res.data });
        sessionStorage.setItem('userInfo', JSON.stringify(res.data));
      } else {
        showErrorNotification(res.error!.message);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const doLogin = async () => {
    setLoading(true);
    const res = await apiLogin(form.values);
    if (res.code === 200) {
      const { accessToken } = res.data;
      useAppState.setState({ accessToken });
      sessionStorage.setItem('accessToken', accessToken);
      await loadCurrentUserInfo();
      await loadUserSidebarMenu();
      // await Promise.all([loadCurrentUserInfo(), loadUserSidebarMenu()]);
      router.push('/dashboard');
    } else {
      // 只在返回错误的时候取消loading：因为登录成功后，会跳转到其他页面，不取消loading的影响也不大。后台错误的时候，需要取消loading，让用户重新输入密码等
      setLoading(false);
      showErrorNotification(res.error!.message);
    }
  };

  const getLoginValidateImage = () => {
    apiGetLoginValidateImage().then((res) => {
      if (res.code === 200) {
        setImageSrc(res.data);
        form.setFieldValue('validateImageSrc', res.data);
      } else {
        showErrorNotification(res.error!.message);
      }
    }).catch((error) => {
      console.error(error);
    });
  };

  useEffect(() => {
    getLoginValidateImage();
  }, []); // 空数组表示只在组件挂载时运行

  return (
    <AuthLayout>
      <LoadingOverlay visible={loading} zIndex={1000} />
      <Container mt={0}>
        <Title style={{ fontWeight: 900 }}>
          {process.env.NEXT_PUBLIC_APP_TITLE}{process.env.NEXT_PUBLIC_APP_SUB_TITLE}
        </Title>

        <Paper style={{ minWidth: 420 }} withBorder shadow="md" p={30} mt={30} radius="md">
          <form onSubmit={form.onSubmit(() => doLogin())}>
            <TextInput
              label="用户名"
              placeholder="请输入用户名"
              required
              {...form.getInputProps('name')}
            />
            <PasswordInput
              label="密码"
              placeholder="请输入密码"
              required
              mt="md"
              {...form.getInputProps('password')}
            />
              <Grid grow style={{ marginTop: '16px' }}>
                <Grid.Col span={7}>
                  <TextInput
                    label="图片验证码"
                    placeholder="请输入图片验证码（忽略大小写）"
                    required
                    {...form.getInputProps('validateCode')}
                  />
                </Grid.Col>
                <Grid.Col span={3}>
                  <Tooltip withArrow label="看不清？点击图片换一张">
                    <div style={{ marginTop: '24px' }}>
                      <Image
                        style={{ width: '100%', height: '36px' }}
                        src={imageSrc}
                        onClick={getLoginValidateImage}
                      />
                    </div>
                  </Tooltip>
                </Grid.Col>
              </Grid>
            <Button fullWidth mt="xl" type="submit">
              登录
            </Button>
          </form>
        </Paper>
      </Container>
    </AuthLayout>
  );
}

export default SignInPage;
