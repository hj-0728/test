<template>
  <Header :class="getHeaderClass">
    <!-- left start -->
    <div :class="`${prefixCls}-left`">
      <!-- logo -->
      <AppLogo
        v-if="getShowHeaderLogo || getIsMobile"
        :class="`${prefixCls}-logo`"
        :theme="getHeaderTheme"
        :style="getLogoWidth"
      />
      <LayoutTrigger
        v-if="
          (getShowContent && getShowHeaderTrigger && !getSplit && !getIsMixSidebar) || getIsMobile
        "
        :theme="getHeaderTheme"
        :sider="false"
      />
      <LayoutBreadcrumb v-if="getShowContent && getShowBread" :theme="getHeaderTheme" />
    </div>
    <!-- left end -->

    <!-- menu start -->
    <div :class="`${prefixCls}-menu`" v-if="getShowTopMenu && !getIsMobile">
      <LayoutMenu
        :isHorizontal="true"
        :theme="getHeaderTheme"
        :splitType="getSplitType"
        :menuMode="getMenuMode"
      />
    </div>
    <!-- menu-end -->

    <!-- action  -->
    <div :class="`${prefixCls}-action`" style="flex: 1; justify-content: flex-end">
      <Notify
        v-if="getShowNotice"
        @view-message="viewMessage"
        :class="`${prefixCls}-action__item notify-item`"
        title="消息"
        style="margin-right: 10px; margin-left: 15px"
      />
      <UserDropDown :theme="getHeaderTheme" />
    </div>
  </Header>
  <div ref="modal">
    <BasicModal
      @register="register"
      title="消息详情"
      width="50%"
      :canFullscreen="false"
      :draggable="false"
      :showOkBtn="false"
      :getContainer="() => $refs.modal"
    >
      <template #title>
        <div>
          <ContainerOutlined />
          消息详情
        </div>
      </template>
      <View :message-id="messageId" />
    </BasicModal>
  </div>
</template>
<script lang="ts">
  import { defineComponent, unref, computed, ref } from 'vue';

  import { propTypes } from '/@/utils/propTypes';

  import { Layout } from 'ant-design-vue';
  import { AppLogo } from '/@/components/Application';
  import LayoutMenu from '../menu/index.vue';
  import LayoutTrigger from '../trigger/index.vue';

  import { useHeaderSetting } from '/@/hooks/setting/useHeaderSetting';
  import { useMenuSetting } from '/@/hooks/setting/useMenuSetting';

  import { MenuModeEnum, MenuSplitTyeEnum } from '/@/enums/menuEnum';

  import { Notify, UserDropDown, LayoutBreadcrumb } from './components';
  import { useAppInject } from '/@/hooks/web/useAppInject';
  import { useDesign } from '/@/hooks/web/useDesign';
  import { useModal, BasicModal } from '/@/components/Modal';
  import { ContainerOutlined } from '@ant-design/icons-vue';
  import View from '/@/views/siteMessage/View.vue';

  export default defineComponent({
    name: 'LayoutHeader',
    components: {
      Header: Layout.Header,
      AppLogo,
      LayoutTrigger,
      LayoutBreadcrumb,
      LayoutMenu,
      UserDropDown,
      ContainerOutlined,
      BasicModal,
      View,
      Notify,
    },
    props: {
      fixed: propTypes.bool,
    },
    setup(props) {
      const { prefixCls } = useDesign('layout-header');
      const {
        getShowTopMenu,
        getShowHeaderTrigger,
        getSplit,
        getIsMixMode,
        getMenuWidth,
        getIsMixSidebar,
      } = useMenuSetting();

      const { getHeaderTheme, getShowNotice, getShowContent, getShowBread, getShowHeaderLogo } =
        useHeaderSetting();

      const { getIsMobile } = useAppInject();

      const getHeaderClass = computed(() => {
        const theme = unref(getHeaderTheme);
        return [
          prefixCls,
          {
            [`${prefixCls}--fixed`]: props.fixed,
            [`${prefixCls}--mobile`]: unref(getIsMobile),
            [`${prefixCls}--${theme}`]: theme,
          },
        ];
      });

      const getLogoWidth = computed(() => {
        if (!unref(getIsMixMode) || unref(getIsMobile)) {
          return {};
        }
        const width = unref(getMenuWidth) < 180 ? 180 : unref(getMenuWidth);
        return { width: `${width}px` };
      });

      const getSplitType = computed(() => {
        return unref(getSplit) ? MenuSplitTyeEnum.TOP : MenuSplitTyeEnum.NONE;
      });

      const getMenuMode = computed(() => {
        return unref(getSplit) ? MenuModeEnum.HORIZONTAL : null;
      });

      const messageId = ref('');
      const [register, { openModal }] = useModal();

      return {
        prefixCls,
        getHeaderClass,
        getShowHeaderLogo,
        getHeaderTheme,
        getShowHeaderTrigger,
        getIsMobile,
        getShowBread,
        getShowContent,
        getSplitType,
        getSplit,
        getMenuMode,
        getShowTopMenu,
        getShowNotice,
        getLogoWidth,
        getIsMixSidebar,
        messageId,
        register,
        openModal,
      };
    },
    methods: {
      viewMessage(messageId) {
        this.messageId = messageId;
        this.openModal();
      },
    },
  });
</script>
<style lang="less">
  @import './index.less';

  .custom-tag-style {
    background-color: #ffffff !important;
    color: #0960bd !important;
    border: 2px solid #0960bd !important;
    font-weight: 600 !important;
    border-radius: 4px !important;
    font-size: 14px !important;
    margin: 0 auto !important;
  }

  .custom-icon-style {
    color: #0960bd !important;
    padding: 0 !important;
  }
</style>
