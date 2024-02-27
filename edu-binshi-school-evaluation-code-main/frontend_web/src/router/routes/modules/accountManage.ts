import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';

const accountManage: AppRouteModule = {
  path: '/account-manage',
  name: 'AccountManage',
  component: LAYOUT,
  redirect: '/account-manage/student-list',
  meta: {
    icon: 'material-symbols:manage-accounts-outline',
    title: '账号管理',
  },
  children: [
    {
      path: 'student-list',
      name: 'StudentList',
      component: () => import('/@/views/accountManage/studentAccount/StudentAccount.vue'),
      meta: {
        title: '学生账号',
        icon: 'material-symbols:person-outline-rounded',
      },
    },
    {
      path: 'teacher-list',
      name: 'TeacherList',
      component: () => import('/@/views/accountManage/teacherAccount/TeacherAccount.vue'),
      meta: {
        title: '教师账号',
        icon: 'material-symbols:person-4-outline',
      },
    },
  ],
};

export default accountManage;
