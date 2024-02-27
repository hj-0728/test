import { PropsWithChildren } from 'react';
import dayjs from 'dayjs';
import { Stack, Text, useMantineTheme } from '@mantine/core';
import AuthLogo from './components/AuthLogo';
import classes from './AuthLayout.module.css';

type AuthLayoutProps = PropsWithChildren<{}>;

const AuthLayout = ({ children }: AuthLayoutProps) => {
  const { colors, fontFamily } = useMantineTheme();
  return (
    <Stack justify="center" gap={20} align="center" className={classes.wrapper}>
      <AuthLogo />
      {children}
      <Text
        style={{ fontFamily: `Greycliff CF, ${fontFamily}`, color: colors.gray[5] }}
        fw={14}
      >
        &copy; {dayjs().year()} {process.env.NEXT_PUBLIC_APP_TITLE}{process.env.NEXT_PUBLIC_APP_SUB_TITLE}
      </Text>
    </Stack>
  );
};

export default AuthLayout;
