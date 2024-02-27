import { forwardRef } from 'react';
import Router from 'next/router';
import { IconChevronRight, IconLogout } from '@tabler/icons-react';
import { Avatar, Group, Menu, Text, UnstyledButton } from '@mantine/core';
import useAppState from '@/store/app';
import { Role } from 'MyApp';
import { useMounted } from '@/utils';

interface UserButtonProps extends React.ComponentPropsWithoutRef<'button'> {
  image: string;
  name: string;
  email?: string;
  icon?: React.ReactNode;
}

const UserButton = forwardRef<HTMLButtonElement, UserButtonProps>(
  ({ image, name, email, icon, ...others }: UserButtonProps, ref) => (
    <UnstyledButton
      ref={ref}
      {...others}
    >
      <Group>
        <Avatar src={image} radius="xl" />

        <div style={{ flex: 1 }}>
          <Text size="sm" fw={500}>
            {name}
          </Text>

          <Text color="dimmed" size="xs">
            {email}
          </Text>
        </div>

        {icon || <IconChevronRight size="1rem" />}
      </Group>
    </UnstyledButton>
  )
);

function UserInfo() {
  const isMounted = useMounted();
  const { userInfo, logout } = useAppState();
  return (
    <>
      { isMounted && userInfo && (
        <Group justify="center">
          <Menu withArrow>
            <Menu.Target>
              <UserButton
                image="https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=255&q=80"
                name={userInfo.name}
              />
            </Menu.Target>
            <Menu.Dropdown>
              {userInfo.roleList.map((item: Role) => (
                <Menu.Item key={item.id}>
                  {item.name}{item.id === userInfo.currentRole.id ? '（√）' : ''}
                </Menu.Item>
              ))}

              <Menu.Divider />
              <Menu.Item
                onClick={() => {
                  sessionStorage.clear();
                  logout();
                  Router.push('/auth/sign-in');
                }}
                leftSection={<IconLogout size={24}/>}
              >
                退出登录
              </Menu.Item>
            </Menu.Dropdown>
          </Menu>
        </Group>
      )}
    </>
  );
}

export default UserInfo;
