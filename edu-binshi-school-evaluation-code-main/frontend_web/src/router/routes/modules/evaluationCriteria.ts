import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const evaluationCriteria: AppRouteModule = {
  path: '/evaluation-criteria',
  name: 'EvaluationCriteria',
  component: LAYOUT,
  redirect: '/evaluation-criteria/list',
  meta: {
    icon: 'ri:file-list-2-line',
    title: t('评价标准'),
    orderNo: 1,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'list',
      name: 'EvaluationCriteriaList',
      component: () => import('/@/views/evaluationCriteria/Index.vue'),
      meta: {
        title: t('评价标准'),
        icon: 'ri:file-list-2-line',
        hideMenu: true,
      },
    },
    {
      path: 'tree/:evaluationCriteriaId',
      name: 'EvaluationCriteriaTree',
      component: () => import('/@/views/evaluationCriteriaTree/Index.vue'),
      meta: {
        title: t('评价项'),
        icon: 'ant-design:setting-filled',
        currentActiveMenu: '/evaluation-criteria/list',
        hideMenu: true,
      },
    },
  ],
};

export default evaluationCriteria;
