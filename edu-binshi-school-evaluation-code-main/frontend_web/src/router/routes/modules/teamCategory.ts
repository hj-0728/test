import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const teamCategory: AppRouteModule = {
  path: '/team-category',
  name: 'TeamCategory',
  component: LAYOUT,
  redirect: '/team-category/list',
  meta: {
    icon: 'fluent:people-team-16-regular',
    title: t('小组类型'),
    orderNo: 1,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'list',
      name: 'TeamCategoryList',
      component: () => import('/@/views/teamCategory/TeamCategoryTable.vue'),
      meta: {
        title: t('小组类型'),
        icon: 'fluent:people-team-16-regular',
        hideMenu: true,
      },
    },
    {
      path: 'team/:teamCategoryId',
      name: 'Team',
      component: () => import('/@/views/team/Index.vue'),
      meta: {
        title: t('小组管理'),
        icon: 'bi:microsoft-teams',
        currentActiveMenu: '/team-category/list',
        hideMenu: true,
      },
    },
  ],
};

export default teamCategory;
