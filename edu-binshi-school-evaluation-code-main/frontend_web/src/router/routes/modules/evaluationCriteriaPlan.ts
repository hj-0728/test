import { AppRouteModule } from '/@/router/types';
import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const evaluationCriteriaPlan: AppRouteModule = {
  path: '/evaluation-criteria-plan',
  name: 'EvaluationCriteriaPlan',
  component: LAYOUT,
  redirect: '/evaluation-criteria-plan/list',
  meta: {
    icon: 'ci:folder-edit',
    title: t('评价计划'),
    orderNo: 1,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'list',
      name: 'EvaluationCriteriaPlan',
      component: () => import('/@/views/evaluationCriteriaPlan/Index.vue'),
      meta: {
        title: t('评价计划'),
        icon: 'ci:folder-edit',
        hideMenu: true,
      },
    },
  ],
};

export default evaluationCriteriaPlan;
