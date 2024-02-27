import { Group, Stack } from '@mantine/core';
import { useMantineTheme } from '@mantine/styles';
import { IconCompass } from '@tabler/icons-react';
import useAppState from '@/store/app';
import classes from './AuthLogo.module.css';

const LOGO_SIZE = 48;
const LOGO_COLLAPSE_SIZE = 42;
export default () => {
  const { sidebarCollapse, primaryColor } = useAppState();
  const { colorScheme } = useAppState();
  const { colors } = useMantineTheme();
  return (
    <>
      <Group
        justify="center"
        gap={10}
        className={classes.wrapper}
        style={{
          borderBottomWidth: 1,
          borderBottomStyle: 'solid',
          borderBottomColor: colorScheme === 'dark' ? colors.dark[8] : colors.gray[0],
        }}
      >
        <IconCompass
          size={sidebarCollapse === true ? LOGO_COLLAPSE_SIZE : LOGO_SIZE}
          color={colors[primaryColor][9]}
        />

        <Stack
          gap={0}
          style={{
            display: sidebarCollapse === true ? 'none' : 'flex',
            opacity: sidebarCollapse === true ? '0' : '1',
            overflow: 'hidden',
            transition: 'all 0.3s',
          }}
        />
      </Group>
      <div className={classes.placeholder} />
    </>
  );
};
