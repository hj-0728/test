import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const honorConfiguration: AppRouteModule = {
  path: '/honor-configuration',
  name: 'HonourConfiguration',
  component: LAYOUT,
  redirect: '/honor-configuration/tree',
  meta: {
    icon: 'ph:chalkboard-teacher-fill',
    title: t('荣誉配置'),
    orderNo: 1,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'tree',
      name: 'HonorConfigurationTree',
      component: () => import('/@/views/honorConfiguration/Index.vue'),
      meta: {
        title: t('荣誉配置'),
        icon: 'ph:chalkboard-teacher-fill',
        hideMenu: true,
      },
    },
  ],
};

export default honorConfiguration;
