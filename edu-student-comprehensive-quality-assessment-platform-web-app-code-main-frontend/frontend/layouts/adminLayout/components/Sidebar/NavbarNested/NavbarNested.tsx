import { Group, ScrollArea } from '@mantine/core';
import { useEffect, useState } from 'react';
import useAppState from '@/store/app';
import { NavbarMenu } from '@/model/Menu.model';
import { LinksGroup } from '../NavbarLinksGroup/NavbarLinksGroup';
import Logo from './Logo';
import classes from './NavbarNested.module.css';

export function NavbarNested() {
  const [menuList, setMenuList] = useState<NavbarMenu[]>([]);
  const { navbarMenu, sidebarWidth } = useAppState();
  useEffect(() => {
    if (navbarMenu && navbarMenu.length > 0) {
      setMenuList(navbarMenu);
    }
  }, [navbarMenu]);
  const links = menuList.map((item) => <LinksGroup {...item} key={item.id} />);

  return (
    <nav className={classes.navbar} style={{ width: sidebarWidth }}>
      <div className={classes.header}>
        <Group>
          <Logo />
        </Group>
      </div>

      <ScrollArea className={classes.links}>
        <div className={classes.linksInner}>{links}</div>
      </ScrollArea>
    </nav>
  );
}
