import { AppRouteModule } from '/@/router/types';
import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const evaluationReport: AppRouteModule = {
  path: '/evaluation-report',
  name: 'EvaluationReport',
  component: LAYOUT,
  redirect: '/evaluation-report/overview',
  meta: {
    icon: 'ant-design:delivered-procedure-outlined',
    title: t('评价报告'),
    orderNo: 1,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: '/evaluation-report/overview',
      name: 'EvaluationReportOverview',
      component: () => import('/@/views/evaluationReport/Index.vue'),
      meta: {
        title: t('评价报告'),
        icon: 'carbon:report',
        hideMenu: true,
        hideBreadcrumb: true,
      },
    },
  ],
};

export default evaluationReport;
