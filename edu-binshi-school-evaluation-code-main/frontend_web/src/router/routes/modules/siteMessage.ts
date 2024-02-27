import type { AppRouteModule } from '/@/router/types';

import { LAYOUT } from '/@/router/constant';
import { t } from '/@/hooks/web/useI18n';

const message: AppRouteModule = {
  path: '/site-message',
  name: 'SiteMessage',
  component: LAYOUT,
  redirect: '/site-message/list',
  meta: {
    icon: 'ant-design:mail-outlined',
    title: t('消息'),
    orderNo: 100000,
    hideChildrenInMenu: true,
  },
  children: [
    {
      path: 'list',
      name: 'MessageList',
      component: () => import('/@/views/siteMessage/List.vue'),
      meta: {
        title: '消息',
        icon: 'clarity:note-edit-line',
        hideMenu: true,
      },
    },
  ],
};

export default message;
