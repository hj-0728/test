import { useState } from 'react';
import { Group, Box, Collapse, ThemeIcon, UnstyledButton, rem } from '@mantine/core';
import { IconChevronRight } from '@tabler/icons-react';
import * as Icons from '@tabler/icons-react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import useAppState from '@/store/app';
import { NavbarMenu } from '@/model/Menu.model';
import classes from './NavbarLinksGroup.module.css';
import { SidebarCollapseButton } from './CollapseNavButton';

export function LinksGroup({ icon: iconName, name, opened: initOpened, childList, path, id }: NavbarMenu) {
  const hasLinks = Array.isArray(childList) && childList.length > 0;
  const [opened, setOpened] = useState(initOpened);
  const { updateNavbarMenuOpened, sidebarCollapse } = useAppState();
  // @ts-ignore
  const Icon = Icons[iconName] || Icons.IconAlignLeft;
  const router = useRouter();
  const curPath = router.pathname;

  const items = (hasLinks ? childList : []).map((lk) => {
    let LinksIcon;
    if (lk.icon) {
      // @ts-ignore
      LinksIcon = Icons[lk.icon];
    }
    return (
      <Link
        href={lk.path}
        passHref
        key={lk.id}
        className={`${classes.link} ${curPath === lk.path ? classes.active : ''}`}
      >
        <Box className={classes.linksBox}>
          {
            LinksIcon && (
              <ThemeIcon variant="light" size={25}>
                <LinksIcon size="1.1rem" />
              </ThemeIcon>
            )
          }
          <Box ml="md">{lk.name}</Box>
        </Box>
      </Link>
    );
  });

  const onClickLinksGroup = () => {
    updateNavbarMenuOpened(id);
    setOpened(!opened);
  };

  return (
    <>
      {
        !sidebarCollapse && (
          <UnstyledButton
            onClick={() => onClickLinksGroup()}
            className={`${classes.control} ${curPath === path ? classes.active : ''}`}
          >
            <Link
              href={hasLinks ? '' : path}
              className={classes.singleLink}
              passHref
              key={id}
            >
              <Group justify="space-between" gap={0}>
                <Box style={{ display: 'flex', alignItems: 'center' }}>
                  <ThemeIcon variant="light" size={30}>
                    <Icon style={{ width: rem(18), height: rem(18) }} />
                  </ThemeIcon>
                  <Box ml="md">{name}</Box>
                </Box>
                {hasLinks && (
                  <IconChevronRight
                    className={classes.chevron}
                    stroke={1.5}
                    style={{
                      width: rem(16),
                      height: rem(16),
                      transform: opened ? 'rotate(-90deg)' : 'none',
                    }}
                  />
                )}
              </Group>
            </Link>
          </UnstyledButton>
        )
      }
      {hasLinks && !sidebarCollapse ? <Collapse in={opened}>{items}</Collapse> : null}
      {sidebarCollapse && <SidebarCollapseButton name={name} icon={Icon} path={path} childList={childList || []} />}
    </>
  );
}
