import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const teacherManage: AppRouteModule = {
  path: '/teacher-manage',
  name: 'TeacherManage',
  component: LAYOUT,
  redirect: '/teacher-manage/tree',
  meta: {
    icon: 'ph:chalkboard-teacher-fill',
    title: t('教师管理'),
    orderNo: 1,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'tree',
      name: 'TeacherManageTree',
      component: () => import('/@/views/teacherManage/deptTeacher/Index.vue'),
      meta: {
        title: t('教师管理'),
        icon: 'ph:chalkboard-teacher-fill',
        hideMenu: true,
      },
    },
  ],
};

export default teacherManage;
