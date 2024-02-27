import { Box, Group, Menu, ThemeIcon, UnstyledButton } from '@mantine/core';
import { forwardRef } from 'react';
import Link from 'next/link';
import * as Icons from '@tabler/icons-react';

import classes from './CollapseNavButton.module.css';

export interface CollapseNavItemProps extends React.ComponentPropsWithoutRef<'button'> {
  icon: any;
}

export interface SidebarCollapseButtonProps {
  name: string;
  icon: string;
  childList: {
    name: string;
    path: string,
    icon: string
  }[];
  path: string
}

export const SidebarCollapseIcon = forwardRef<HTMLButtonElement, CollapseNavItemProps>(
  ({ icon: Icon }: CollapseNavItemProps, ref) => (
    <UnstyledButton ref={ref}>
      <Group justify="center" gap={0}>
        <Box>
          <ThemeIcon variant="light" size={30}>
            <Icon size="1.1rem" />
          </ThemeIcon>
        </Box>
      </Group>
    </UnstyledButton>
  )
);

export const SidebarCollapseButton = ({ childList, icon, name, path }: SidebarCollapseButtonProps) => {
  const menuItems = (Array.isArray(childList) ? childList : []).map((ls) => {
    let LinkIcon;
    if (ls.icon) {
      // @ts-ignore
      LinkIcon = Icons[ls.icon];
    }
    return (
      <Menu.Item key={ls.name} onClick={(event: any) => event.preventDefault()}>
        <Link href={ls.path} passHref className={classes.menuItemLink}>
          <Box className={classes.menuItemBox}>
            {
              LinkIcon && (
                <LinkIcon size="1.1rem" />
              )
            }
            <Box ml="md">{ls.name}</Box>
          </Box>
        </Link>
      </Menu.Item>
    );
  });
  return (
    <div className={classes.menu}>
      <Menu position="right-start" shadow="md" trigger="hover">
        <Menu.Target>
          <Link href={childList.length === 0 ? path : ''} passHref>
            <SidebarCollapseIcon icon={icon} />
          </Link>
        </Menu.Target>
        {
          childList.length > 0 && (
            <Menu.Dropdown>
              <Menu.Label>{name}</Menu.Label>
              {menuItems}
            </Menu.Dropdown>
          )
        }
      </Menu>
    </div>
  );
};
