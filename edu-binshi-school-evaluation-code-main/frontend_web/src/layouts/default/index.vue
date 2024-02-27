<template>
  <Loading :loading="loading" />
  <ResetPasswordModalForLoginCheck
    v-if="resetPassword && !loading"
    @reset-password-success="resetPasswordSuccess"
  />
  <Loading :loading="loadingChild" />
  <Layout :class="prefixCls" v-bind="lockEvents" v-if="!resetPassword && !loading">
    <LayoutFeatures />
    <LayoutHeader fixed v-if="getShowFullHeaderRef" />
    <Layout :class="[layoutClass]">
      <LayoutSideBar v-if="getShowSidebar || getIsMobile" :key="'sideBar' + sideBarKey" />
      <Layout :class="`${prefixCls}-main`">
        <LayoutMultipleHeader />
        <LayoutContent />
        <LayoutFooter />
      </Layout>
    </Layout>
  </Layout>
</template>

<script lang="ts">
  import { defineComponent, computed, unref, ref, provide } from 'vue';
  import { Layout } from 'ant-design-vue';
  import { createAsyncComponent } from '/@/utils/factory/createAsyncComponent';

  import LayoutHeader from './header/index.vue';
  import LayoutContent from './content/index.vue';
  import LayoutSideBar from './sider/index.vue';
  import LayoutMultipleHeader from './header/MultipleHeader.vue';

  import { useHeaderSetting } from '/@/hooks/setting/useHeaderSetting';
  import { useMenuSetting } from '/@/hooks/setting/useMenuSetting';
  import { useDesign } from '/@/hooks/web/useDesign';
  import { useLockPage } from '/@/hooks/web/useLockPage';

  import { useAppInject } from '/@/hooks/web/useAppInject';
  import ResetPasswordModalForLoginCheck from '/@/layouts/default/resetPasswordForLogin/resetPasswordModalForLoginCheck.vue';
  import { apiGetUserInfo } from '/@/api/sys/user';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { Loading } from '/@/components/Loading';
  import { useChangeRoleStore } from '/@/store/modules/changeRole';

  export default defineComponent({
    name: 'DefaultLayout',
    components: {
      LayoutFeatures: createAsyncComponent(() => import('/@/layouts/default/feature/index.vue')),
      LayoutFooter: createAsyncComponent(() => import('/@/layouts/default/footer/index.vue')),
      LayoutHeader,
      LayoutContent,
      LayoutSideBar,
      LayoutMultipleHeader,
      Layout,
      ResetPasswordModalForLoginCheck,
      Loading,
    },
    setup() {
      const loading = ref(true);
      const loadingChild = ref(false);
      const { prefixCls } = useDesign('default-layout');
      const { getIsMobile } = useAppInject();
      const { getShowFullHeaderRef } = useHeaderSetting();
      const { getShowSidebar, getIsMixSidebar, getShowMenu } = useMenuSetting();
      const changeLoading = (loadingValue) => {
        loadingChild.value = loadingValue;
      };
      provide('changeLoading', changeLoading);
      // Create a lock screen monitor
      const lockEvents = useLockPage();

      const layoutClass = computed(() => {
        let cls: string[] = ['ant-layout'];
        if (unref(getIsMixSidebar) || unref(getShowMenu)) {
          cls.push('ant-layout-has-sider');
        }
        return cls;
      });
      const resetPassword = ref();
      const getUserInfo = () => {
        apiGetUserInfo()
          .then((res) => {
            if (res.code === 200) {
              resetPassword.value = res.data.passwordReset;
            } else {
              useMessage().createErrorNotification(
                {
                  message: '错误',
                  description: res.error.message,
                },
                'pre-wrap',
              );
            }
          })
          .catch(() => {
            useMessage().notification.destroy();
            useMessage().createErrorModal({
              title: '操作失败',
              content: '网络异常，请检查您的网络连接是否正常!',
              closable: true,
              maskClosable: false,
              showOkBtn: true,
              showCancelBtn: false,
            });
          })
          .finally(() => {
            loading.value = false;
          });
      };
      getUserInfo();
      const changeRoleStore = useChangeRoleStore();
      const sideBarKey = ref(new Date().getTime());
      return {
        changeLoading,
        getShowFullHeaderRef,
        getShowSidebar,
        prefixCls,
        getIsMobile,
        getIsMixSidebar,
        layoutClass,
        lockEvents,
        resetPassword,
        loading,
        changeRoleStore,
        sideBarKey,
        loadingChild,
      };
    },
    watch: {
      'changeRoleStore.$state.refreshSideBarKey': {
        deep: true,
        handler(newVal, _oldVal) {
          this.sideBarKey = newVal;
        },
      },
    },
    methods: {
      resetPasswordSuccess() {
        this.resetPassword = false;
      },
    },
  });
</script>
<style lang="less">
  @prefix-cls: ~'@{namespace}-default-layout';

  .@{prefix-cls} {
    display: flex;
    width: 100%;
    min-height: 100%;
    background-color: @content-bg;
    flex-direction: column;

    > .ant-layout {
      min-height: 100%;
    }

    &-main {
      width: 100%;
      margin-left: 1px;
    }
  }
</style>
