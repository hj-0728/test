import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';

const statistics: AppRouteModule = {
  path: '/',
  name: 'Statistics',
  component: LAYOUT,
  redirect: '/statistics',
  meta: {
    icon: 'material-symbols:bar-chart-4-bars-rounded',
    title: '统计',
    orderNo: 1,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'statistics',
      name: 'StatisticsIndex',
      component: () => import('/src/views/statistics/Index.vue'),
      meta: {
        title: '统计',
        icon: 'material-symbols:bar-chart-4-bars-rounded',
        hideMenu: true,
        carryParam: true,
      },
    },
  ],
};

export default statistics;
