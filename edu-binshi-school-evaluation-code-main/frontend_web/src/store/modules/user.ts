import type { UserInfo } from '/#/store';
import type { ErrorMessageMode } from '/#/axios';
import { defineStore } from 'pinia';
import { store } from '/@/store';
import { RoleEnum } from '/@/enums/roleEnum';
import { PageEnum } from '/@/enums/pageEnum';
import { ROLES_KEY, TOKEN_KEY, USER_INFO_KEY, MENU_KEY } from '/@/enums/cacheEnum';
import { getAuthCache, setAuthCache, setStorage } from '/@/utils/auth';
import { LoginParams } from '/@/api/sys/model/userModel';
import { doLogout, apiGetUserInfo, apiLogin } from '/@/api/sys/user';
import { useI18n } from '/@/hooks/web/useI18n';
import { useMessage } from '/@/hooks/web/useMessage';
import { router } from '/@/router';
import { usePermissionStore } from '/@/store/modules/permission';
import { RouteRecordRaw } from 'vue-router';
import { PAGE_NOT_FOUND_ROUTE } from '/@/router/routes/basic';
import { h, ref } from 'vue';
import { useAppStore } from '/@/store/modules/app';
import { isArray } from '/@/utils/is';
import { apiGetDBMenuTree } from '/@/api/menu/menu';

// interface UserState {
//   userInfo: Nullable<UserInfo>;
//   token?: string;
//   roleList: RoleEnum[];
//   sessionTimeout?: boolean;
//   lastUpdateTime: number;
//   lastRoleId: string;
// }

export const useUserStore = defineStore({
  id: 'app-user',
  state: (): {
    userInfo: null;
    lastRoleCode: string;
    lastRoleId: string;
    sessionTimeout: boolean;
    roleList: any[];
    token: undefined;
    lastUpdateTime: number;
  } => ({
    // user info
    userInfo: null,
    // token
    token: undefined,
    // roleList
    roleList: [],
    // Whether the login expired
    sessionTimeout: false,
    // Last fetch time
    lastUpdateTime: 0,
    lastRoleId: '',
    lastRoleCode: '',
  }),
  getters: {
    getUserInfo(): UserInfo {
      return this.userInfo || getAuthCache<UserInfo>(USER_INFO_KEY) || {};
    },
    getToken(): string {
      return this.token || getAuthCache<string>(TOKEN_KEY);
    },
    getRoleList(): RoleEnum[] {
      return this.roleList.length > 0 ? this.roleList : getAuthCache<RoleEnum[]>(ROLES_KEY);
    },
    getSessionTimeout(): boolean {
      return !!this.sessionTimeout;
    },
    getLastUpdateTime(): number {
      return this.lastUpdateTime;
    },
    getLastRoleCode(): string {
      return this.lastRoleCode;
    },
  },
  actions: {
    setToken(info: string | undefined) {
      this.token = info ? info : ''; // for null or undefined value
      setAuthCache(TOKEN_KEY, info);
    },
    setRoleList(roleList: RoleEnum[]) {
      this.roleList = roleList;
      setAuthCache(ROLES_KEY, roleList);
    },
    setUserInfo(info: UserInfo | null) {
      this.userInfo = info;
      this.lastUpdateTime = new Date().getTime();
      setAuthCache(USER_INFO_KEY, info);
    },
    setSessionTimeout(flag: boolean) {
      this.sessionTimeout = flag;
    },
    setLastRoleId(roleId: string) {
      this.lastRoleId = roleId;
    },
    setLastRoleCode(roleCode: string) {
      this.lastRoleCode = roleCode;
    },
    resetState() {
      this.userInfo = null;
      this.token = '';
      this.roleList = [];
      this.sessionTimeout = false;
    },

    /**
     * @description: 获取用户菜单
     */
    async getDbMenuTree() {
      const { t } = useI18n();
      const basicMenuTree = ref([]);
      await apiGetDBMenuTree().then((res) => {
        if (res.code === 200) {
          function rebuildMenuItem(dataList) {
            dataList.map((data) => {
              data.title = data.name;
              data.orderNo = data.seq;
              data.childrenList = data.children;
              if (data.children && data.children.length) {
                rebuildMenuItem(data.childrenList);
              }
            });
          }

          rebuildMenuItem(res.data);
          basicMenuTree.value = res.data;
        } else {
          useMessage().createErrorNotification({
            message: t('sys.api.errorTip'),
            description: res.error.message,
            class: 'network-error',
          });
        }
      });
      setStorage(MENU_KEY, basicMenuTree.value);
      return basicMenuTree;
    },

    /**
     * @description: login
     */
    async login(
      params: LoginParams & {
        goHome?: boolean;
        mode?: ErrorMessageMode;
      },
    ): Promise<UserInfo | null | boolean> {
      const { t } = useI18n();
      try {
        const { goHome = true, mode, ...loginParams } = params;
        const data = await apiLogin(loginParams, mode);
        if (data.code !== 200) {
          useMessage().createConfirm({
            iconType: 'error',
            title: () => h('span', t('sys.login.loginFailedTitle')),
            content: () => h('span', data.error.message),
            okCancel: false,
            onOk: async () => {
              await this.logout(true);
            },
          });
          return false;
        } else {
          const token = data.data;
          this.setToken(token);
          // @ts-ignore
          return this.afterLoginAction(goHome);
        }
      } catch (error) {
        return Promise.reject(t('sys.api.networkExceptionMsg'));
      }
    },

    /**
     * @description: 登录后的动作
     */
    async afterLoginAction(goHome?: boolean): Promise<UserInfo | null> {
      if (!this.getToken) return null;
      // get user info
      const userInfo = await this.getUserInfoAction();
      await this.getDbMenuTree();

      const sessionTimeout = this.sessionTimeout;
      if (sessionTimeout) {
        this.setSessionTimeout(false);
      } else {
        const permissionStore = usePermissionStore();
        if (!permissionStore.isDynamicAddedRoute) {
          const routes = await permissionStore.buildRoutesAction();
          routes.forEach((route) => {
            router.addRoute(route as unknown as RouteRecordRaw);
          });
          router.addRoute(PAGE_NOT_FOUND_ROUTE as unknown as RouteRecordRaw);
          permissionStore.setDynamicAddedRoute(true);
        }
        goHome && (await router.replace(userInfo?.homePath || PageEnum.BASE_HOME));
      }
      return userInfo;
    },

    /**
     * @description: 获取当前用户信息动作
     */
    async getUserInfoAction(): Promise<UserInfo | null> {
      const userInfo = await this.getCurrentUserInfo();
      if (userInfo) {
        const roles = userInfo.roleList;
        if (isArray(roles)) {
          const roleList = roles.map((item) => item.code) as RoleEnum[];
          this.setRoleList(roleList);
        } else {
          this.setRoleList([]);
        }
        // @ts-ignore
        this.setUserInfo(userInfo);
        const currentRole = userInfo.currentRole;
        this.setLastRoleId(currentRole.id);
        this.setLastRoleCode(currentRole.code);
        return userInfo;
      }
      return null;
    },

    /**
     * @description: 获取当前用户信息
     */
    async getCurrentUserInfo(): Promise<UserInfo | null> {
      const { t } = useI18n();
      try {
        const data = await apiGetUserInfo();
        if (data.code !== 200) {
          useMessage().createConfirm({
            iconType: 'error',
            title: () => h('span', t('sys.user.getUserInfoFailed')),
            content: () => h('span', data.error.message),
            okCancel: false,
            onOk: async () => {
              await this.doLogout();
            },
          });
          return null;
        } else {
          return data.data;
        }
      } catch (error) {
        return Promise.reject(t('sys.api.networkExceptionMsg'));
      }
    },

    /**
     * @description: 更新用户信息
     */
    async updateUserInfo() {
      if (!this.getToken) return null;
      const userInfo = await this.getCurrentUserInfo();
      this.setUserInfo(userInfo);
      // @ts-ignore
      const currentRole = userInfo.currentRole;
      this.setLastRoleId(currentRole.id);
      this.setLastRoleCode(currentRole.code);
    },

    /**
     * @description: logout
     */
    async logout(goLogin = false) {
      this.setToken(undefined);
      this.setSessionTimeout(false);
      this.setUserInfo(null);
      goLogin && (await router.push(PageEnum.BASE_LOGIN));
    },

    /**
     * @description: Confirm before logging out
     */
    confirmLoginOut(needConfirm = true) {
      if (!needConfirm) {
        this.doLogout();
        return;
      }
      const { t } = useI18n();
      useMessage().createConfirm({
        iconType: 'warning',
        title: () => h('span', t('sys.app.logoutTip')),
        content: () => h('span', t('sys.app.logoutMessage')),
        onOk: async () => {
          await this.doLogout();
        },
        onCancel: () => {
          useAppStore().setLogoutStatus('');
        },
      });
    },

    /**
     * @description: 向后台请求退出登录
     */
    async doLogout() {
      doLogout().then(async (res) => {
        // 如果一个用户在两个浏览器登录，其中一台退出登录之后，已经没有这个身份了，此时后台返回的是500，如果只200的时候才处理，后面登出的就出错了
        console.log(res);
        await this.logout(true);
      });
    },
  },
});

// Need to be used outside the setup
export function useUserStoreWithOut() {
  return useUserStore(store);
}
