import { Flex, Group, Stack } from '@mantine/core';
import MenuBtn from './MenuBtn';
import UserButton from './UserButton';

export default () => (
  <Stack justify="center" style={{ height: '100%' }}>
    <Group justify="left" grow align="apart">
      <Flex align="center">
        <MenuBtn />
      </Flex>
      <Flex justify="flex-end" align="center">
        <Group justify="right">
          <UserButton />
        </Group>
      </Flex>
    </Group>
  </Stack>
);
