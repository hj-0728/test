<template>
  <MenuItem v-if="itemKey !== 'changeRole'" :key="itemKey">
    <span class="flex items-center">
      <Icon :icon="icon" class="mr-1" />
      <span>{{ text }}</span>
    </span>
  </MenuItem>
  <div v-if="itemKey === 'changeRole'">
    <MenuItem
      v-for="role in roles"
      @click="showConfirm(role['id'], role['code'], role['name'])"
      :key="role['id']"
      :subMenuOpenDelay="0.1"
    >
      <Icon icon="la:user-cog" size="18" style="vertical-align: middle; margin-left: -2px" />
      <span style="margin-left: 5px; vertical-align: middle">{{ role['name'] }}</span>
      <CheckOutlined style="color: #0b0; margin-left: 2px" v-if="currentRoleId === role['id']" />
    </MenuItem>
  </div>
  <MenuDivider v-if="itemKey === 'changeRole'" />
</template>
<script lang="ts">
  import { Menu, Modal } from 'ant-design-vue';
  import { computed, createVNode, defineComponent, getCurrentInstance, inject, ref } from 'vue';
  import Icon from '/@/components/Icon/index';
  import { propTypes } from '/@/utils/propTypes';
  import { CheckOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue';
  import { useChangeRoleStore, useFillInStoreWithOut } from '/@/store/modules/changeRole';
  import { useUserStore } from '/@/store/modules/user';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { apiUpdateUserCurrentRole } from '/@/api/role/role';
  import { useAppStore } from '/@/store/modules/app';
  import { useTabs } from '/@/hooks/web/useTabs';
  import headerImg from '/@/assets/images/header.jpg';
  import { useGo } from '/@/hooks/web/usePage';
  import { getStorage } from '/@/utils/auth';
  import { MENU_KEY, USER_INFO_KEY } from '/@/enums/cacheEnum';

  export default defineComponent({
    name: 'DropdownMenuItem',
    components: { MenuItem: Menu.Item, Icon, CheckOutlined, MenuDivider: Menu.Divider },
    props: {
      // eslint-disable-next-line
      key: propTypes.string,
      text: propTypes.string,
      icon: propTypes.string,
    },
    setup(props) {
      const changeLoading = inject('changeLoading') as Function;
      const messageKey = ref('updatable');
      const appStore = useAppStore();
      const userStore = useUserStore();
      const instance = getCurrentInstance();
      const itemKey = computed(() => props.key || instance?.vnode?.props?.key);
      let userInfo = userStore.getUserInfo;
      const getUserInfo = computed(() => {
        const { name = '', avatar, desc } = userStore.getUserInfo || {};
        return { name, avatar: avatar || headerImg, desc };
      });
      const roles = userInfo.roleList;
      const currentRoleCode = ref<string>(userInfo.currentRole.code);
      const currentRoleName = ref<string>(userInfo.currentRole.name);
      const currentRoleId = computed(() => {
        if (userInfo.currentRole) {
          return userInfo.currentRole.id;
        } else {
          return null;
        }
      });
      const switchRoleHandler = async (roleId: string, roleCode: string, role_name: string) => {
        if (roleId !== currentRoleId.value) {
          const changeRoleStore = useFillInStoreWithOut();
          changeRoleStore.setNeedClearTabs(true);
          userStore.setLastRoleId(roleId);
          userInfo.currentRole.id = roleId;
          currentRoleCode.value = roleCode;
          currentRoleName.value = role_name;
          const updateRoleResult = await updateCurrentRole(roleId);
          if (updateRoleResult) {
            await toPath();
            appStore.setUpdateUnreadStatusFlag(true);
          } else {
            changeLoading(false);
            useMessage().createErrorNotification({
              message: '操作失败',
              description: '切换角色失败',
            });
          }
        }
      };
      const updateCurrentRole = async function (roleId) {
        let params: any = { roleId: roleId };
        let flag = false;
        await apiUpdateUserCurrentRole(params)
          .then((res) => {
            if (res.code === 200) {
              flag = res.data;
              useMessage().createSuccessNotification({
                message: '切换成功',
              });
            } else {
              changeLoading(false);
              useMessage().createErrorNotification({
                message: '操作失败',
                description: res.error.message,
              });
            }
          })
          .catch(() => {
            changeLoading(false);
            useMessage().createErrorModal({
              title: '操作失败',
              content: '网络异常，请检查您的网络连接是否正常!',
              closable: true,
              maskClosable: false,
            });
          });
        const userStore = useUserStore();
        await userStore.updateUserInfo();
        await userStore.getDbMenuTree();
        const changeRoleStore = useChangeRoleStore();
        changeRoleStore.setRefreshSideBarKey(new Date().getTime());
        return flag;
      };
      const { refreshPage } = useTabs();
      const go = useGo();
      const toPath = async function () {
        const menuList = getStorage(MENU_KEY);
        const storageUserInfo = getStorage(USER_INFO_KEY);
        const windowsPath = window.location.hash;
        // 因为目前就两级菜单，不考虑更多级的情况了，正常应该写个递归的
        const sameMenu = [];
        menuList.map((m) => {
          if (windowsPath.includes(m.path)) {
            sameMenu.push(m);
          } else {
            if (m.children && m.children.length > 0) {
              m.children.map((c) => {
                if (windowsPath.includes(c.path)) {
                  sameMenu.push(c);
                }
              });
            }
          }
        });
        // 因为计划把整个tab隐藏起来
        // await closeAll();
        if (sameMenu && sameMenu.length > 0) {
          await refreshPage();
        } else {
          go(storageUserInfo.homePath);
        }
        changeLoading(false);
      };
      return {
        changeLoading,
        messageKey,
        itemKey,
        roles,
        switchRoleHandler,
        currentRoleId,
        userInfo,
        currentRoleCode,
        currentRoleName,
        appStore,
        getUserInfo,
      };
    },
    methods: {
      showConfirm(role_id, role_code, role_name) {
        // this.changeLoading();
        if (role_id != this.userInfo.currentRole.id) {
          Modal.confirm({
            title: '您确定要切换当前身份吗?',
            icon: createVNode(ExclamationCircleOutlined),
            content: '您当前身份为' + this.currentRoleName + '，切换后的身份为' + role_name,
            mask: true,
            onOk: () => {
              this.changeLoading(true);
              this.switchRoleHandler(role_id, role_code, role_name);
            },
            // eslint-disable-next-line @typescript-eslint/no-empty-function
            onCancel() {},
          });
        }
      },
    },
  });
</script>
