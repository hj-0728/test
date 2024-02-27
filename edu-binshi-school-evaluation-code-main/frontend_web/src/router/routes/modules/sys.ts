import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const system: AppRouteModule = {
  path: '/',
  name: 'System',
  component: LAYOUT,
  redirect: '/role/list',
  meta: {
    icon: 'mdi:file-tree-outline',
    title: t('系统管理'),
  },
  children: [
    {
      path: '/role/list',
      name: 'Role',
      component: () => import('/@/views/role/index.vue'),
      meta: {
        title: t('角色管理'),
        icon: 'ph:chalkboard-teacher-fill',
      },
    },
    {
      path: '/ability-permission/tree',
      name: 'AbilityPermissionTree',
      component: () => import('/@/views/abilityPermission/Tree.vue'),
      meta: {
        title: t('功能权限'),
        icon: 'icon-park-outline:permissions',
      },
    },
    {
      path: '/menu/tree',
      name: 'MenuTree',
      component: () => import('/@/views/menu/Tree.vue'),
      meta: {
        title: t('菜单管理'),
        icon: 'ant-design:menu-outlined',
      },
    },
    {
      path: '/route/list',
      name: 'Route',
      component: () => import('/@/views/route/List.vue'),
      meta: {
        title: t('路径列表'),
        icon: 'ion:git-compare',
      },
    },
  ],
};

export default system;
