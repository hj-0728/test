import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';

const home: AppRouteModule = {
  path: '/',
  name: 'Home',
  component: LAYOUT,
  redirect: '/home',
  meta: {
    icon: 'material-symbols:home-outline-rounded',
    title: '首页',
    orderNo: 1,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'home',
      name: 'HomeIndex',
      component: () => import('/src/views/home/Home.vue'),
      meta: {
        title: '首页',
        icon: 'material-symbols:home-outline-rounded',
        hideMenu: true,
      },
    },
  ],
};

export default home;
