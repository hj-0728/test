import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const honorConfiguration: AppRouteModule = {
  path: '/report-manage',
  name: 'ReportManage',
  component: LAYOUT,
  redirect: '/report-manage/tree',
  meta: {
    icon: 'ph:chalkboard-teacher-fill',
    title: t('报告单模板'),
    orderNo: 1,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'tree',
      name: 'ReportManageTree',
      component: () => import('/@/views/reportManage/Index.vue'),
      meta: {
        title: t('荣誉配置'),
        icon: 'ph:chalkboard-teacher-fill',
        hideMenu: true,
      },
    },
  ],
};

export default honorConfiguration;
