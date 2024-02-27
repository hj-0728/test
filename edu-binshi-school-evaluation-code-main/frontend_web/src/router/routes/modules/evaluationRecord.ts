import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const evaluationRecord: AppRouteModule = {
  path: '/evaluation-record',
  name: 'EvaluationRecord',
  component: LAYOUT,
  redirect: '/evaluation-record/todo-list',
  meta: {
    icon: 'fluent:slide-record-24-regular',
    title: t('评价记录'),
  },
  children: [
    {
      path: '/evaluation-record/todo-list',
      name: 'EvaluationList',
      component: () => import('/@/views/evaluationRecord/Index.vue'),
      meta: {
        title: t('评价列表'),
        icon: 'material-symbols:approval-delegation-outline',
      },
    },
    {
      path: '/evaluation-record/about-me',
      name: 'evaluationRecordAboutMe',
      component: () => import('/@/views/evaluationRecord/aboutMe/Index.vue'),
      meta: {
        title: t('自我评价'),
        icon: 'material-symbols:ar-on-you-outline',
      },
    },
    {
      path: '/evaluation-assignment/todo-list/:evaluationCriteriaPlanId',
      name: 'evaluationAssignmentTodoList',
      component: () => import('/@/views/evaluationRecord/evaluationAssignment/Index.vue'),
      meta: {
        title: t('评价分配'),
        icon: 'solar:branching-paths-up-broken',
        currentActiveMenu: '/evaluation-record/todo-list',
        hideMenu: true,
      },
    },
    {
      path: '/evaluation-record/evaluation-report/overview/:id',
      name: 'evaluationRecordReportOverview',
      component: () => import('/@/views/evaluationReport/Index.vue'),
      meta: {
        title: t('评价报告'),
        icon: 'carbon:report',
        currentActiveMenu: '/evaluation-record/todo-list',
        hideMenu: true,
      },
    },
  ],
};

export default evaluationRecord;
