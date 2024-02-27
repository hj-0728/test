import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';

const stateCouncilIndex: AppRouteModule = {
  path: '/template',
  name: 'Template',
  component: LAYOUT,
  redirect: '/template/basic-table',
  meta: {
    // hideChildrenInMenu: true,
    icon: 'simple-icons:about-dot-me',
    title: '模板路由',
    orderNo: 1,
    hideMenu: true,
  },
  children: [
    {
      path: '/basic-table',
      name: 'BasicTable',
      component: () => import('/@/views/template/table/TemplateList.vue'),
      meta: {
        title: '基础Table',
        ignoreAuth: true,
      },
    },
    {
      path: '/basic-tree',
      name: 'BasicTreeFromVben',
      component: () => import('/@/views/template/tree/BasicTreeFromVben.vue'),
      meta: {
        title: 'Vben基础Tree',
        ignoreAuth: true,
      },
    },
  ],
};
export default stateCouncilIndex;
