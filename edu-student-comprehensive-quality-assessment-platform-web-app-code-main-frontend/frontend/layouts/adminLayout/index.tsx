import { PropsWithChildren, useEffect, useState } from 'react';
import { AppShell } from '@mantine/core';
import { useRouter } from 'next/router';
import { NavbarNested } from '@/layouts/adminLayout/components/Sidebar/NavbarNested/NavbarNested';
import useAppState from '@/store/app';
import AppHeader from './components/AppHeader';
import classes from './AdminLayout.module.css';

type AdminLayoutProps = PropsWithChildren<{}>;

function AdminLayout({ children }: AdminLayoutProps) {
  const router = useRouter();
  const [isReady, setIsReady] = useState(false);
  const { sidebarWidth } = useAppState();

  useEffect(() => {
    const accessToken = sessionStorage.getItem('accessToken');
    if (!accessToken) {
      router.push('/auth/sign-in');
    } else {
      setIsReady(true);
    }
  }, []);

  if (!isReady) {
    return null;
  }

  return (
    <AppShell
      header={{ height: 60 }}
      navbar={{
        width: sidebarWidth,
        breakpoint: 'sm',
      }}
      padding="md"
    >
      <AppShell.Header
        style={{
          width: `calc(100% - ${sidebarWidth})`,
          marginLeft: sidebarWidth,
        }}
      >
        <AppHeader />
      </AppShell.Header>

      <AppShell.Navbar className={classes.navbar}>
        <NavbarNested />
      </AppShell.Navbar>

      <AppShell.Main className={classes.main}>
        {children}
      </AppShell.Main>
    </AppShell>
  );
}

export default AdminLayout;
