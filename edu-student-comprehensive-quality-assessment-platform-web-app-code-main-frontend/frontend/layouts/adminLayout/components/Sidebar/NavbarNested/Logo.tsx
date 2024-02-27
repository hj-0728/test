import { Image } from '@mantine/core';
import useAppState from '@/store/app';
import classes from './Logo.module.css';

const Logo = () => {
  const { sidebarCollapse } = useAppState();
  return (
    <>
      <Image
        h={40}
        w={40}
        radius="40"
        src="/logo.png"
      />
      {
        !sidebarCollapse && (
          <div>
            <div className={classes.title}>{process.env.NEXT_PUBLIC_APP_TITLE}</div>
            <div className={classes.subTitle}>{process.env.NEXT_PUBLIC_APP_SUB_TITLE}</div>
          </div>
        )
      }
    </>
  );
};
export default Logo;
