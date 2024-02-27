<template>
  <div v-if="currentRoleCode !== 'STUDENT'">
    <Popover
      title=""
      trigger="click"
      v-model:visible="visible"
      :overlayClassName="`${prefixCls}__overlay`"
      @visible-change="visibleChange"
    >
      <Badge
        :count="existUnreadMessageCount"
        :numberStyle="numberStyle"
        class="unread-message-count"
      >
        <!--        <BellOutlined />-->
        <Tag :class="getIsHorizontal ? 'custom-tag-style' : 'custom-tag-style'">
          <template #icon>
            <BellOutlined
              :size="18"
              :style="{ color: getIsHorizontal ? '#ffffff' : '#0960bd', padding: 0 }"
              :class="getIsHorizontal ? 'custom-icon-style' : 'custom-icon-style'"
            />
          </template>
          <text>消息</text>
        </Tag>
      </Badge>
      <template #content>
        <Tabs>
          <template v-for="(item, index) in [listData]" :key="index">
            <TabPane>
              <template #tab>
                <div style="width: 280px">
                  <MailTwoTone />
                  未读通知
                  <span v-if="item.length !== 0">({{ totalCount }})</span>
                </div>
              </template>
              <!-- 绑定title-click事件的通知列表中标题是“可点击”的-->
              <NoticeList
                :list="item"
                :total-count="totalCount"
                @title-click="onNoticeClick"
                @get-message="getMessage"
                @update-exist-unread-message="updateExistUnreadMessage"
              />
            </TabPane>
          </template>
        </Tabs>
      </template>
    </Popover>
  </div>
</template>
<script lang="ts">
  import {
    defineComponent,
    ref,
    reactive,
    toRefs,
    onMounted,
    provide,
    computed,
    watch,
    unref,
  } from 'vue';
  import { Popover, Tabs, Badge, Tag } from 'ant-design-vue';
  import { BellOutlined, MailTwoTone } from '@ant-design/icons-vue';
  import NoticeList from './NoticeList.vue';
  import { useDesign } from '/@/hooks/web/useDesign';
  import { MessagePageQueryResponseModel } from '/@/api/siteMessage/siteMessageModel';
  import { apiJudgeUnreadMessageExist, apiSiteMessageList } from '/@/api/siteMessage/siteMessage';
  import { getToken } from '/@/utils/auth';
  import { useAppStore } from '/@/store/modules/app';
  import { MenuModeEnum } from '/@/enums/menuEnum';
  import { getAuthCache } from '/@/utils/auth';
  import { USER_INFO_KEY } from '/@/enums/cacheEnum';
  import { UserInfo } from '/#/store';
  export default defineComponent({
    components: {
      Popover,
      BellOutlined,
      Tabs,
      TabPane: Tabs.TabPane,
      Badge,
      NoticeList,
      MailTwoTone,
      Tag,
    },
    setup() {
      const { prefixCls } = useDesign('header-notify');
      const listData = ref([]);
      const visible = ref(false);
      const existUnreadMessage = ref<boolean>(false);
      const existUnreadMessageCount = ref<any>(null);
      const searchText = ref('');
      const pageSize = ref(1000);
      const pageIndex = ref(0);
      const draw = ref(1);
      const totalCount = ref(0);
      const count = ref(1);
      const compState = reactive({
        absolute: true,
        loading: false,
        tip: '加载中...',
      });
      const currentUserInfo: UserInfo = getAuthCache(USER_INFO_KEY);
      const currentRoleCode: string = currentUserInfo.currentRole.code;

      let interval;
      function polling() {
        loadUnreadMessageCount();
        if (interval) {
          clearInterval(interval);
        }
        interval = setInterval(async () => {
          await loadUnreadMessageCount();
        }, 30000);
      }

      async function loadUnreadMessageCount() {
        const token = getToken();
        if (token) {
          let res = await apiJudgeUnreadMessageExist();
          handleUnreadMessageCountDisplay(res);
        }
      }

      function handleUnreadMessageCountDisplay(res) {
        existUnreadMessage.value = res.data > 0;
        if (res.data > 0) {
          existUnreadMessageCount.value = res.data;
        } else {
          existUnreadMessageCount.value = null;
        }
      }

      onMounted(async () => {
        polling();
      });

      function updateExistUnreadMessage(status) {
        existUnreadMessage.value = status;
      }

      provide('noticeVisible', visible);
      window.onresize = function () {
        visible.value = false;
      };

      const appStore = useAppStore();
      const updateUnreadStatusFlag = computed(() => {
        return appStore.getUpdateUnreadStatusFlag;
      });
      watch(updateUnreadStatusFlag, () => {
        if (updateUnreadStatusFlag.value) {
          apiJudgeUnreadMessageExist()
            .then((res) => {
              handleUnreadMessageCountDisplay(res);
            })
            .finally(() => {
              appStore.setUpdateUnreadStatusFlag('');
            });
        }
      });

      const getMenuMode = computed(() => {
        return appStore.getMenuSetting.mode;
      });

      const getIsHorizontal = computed(() => {
        return unref(getMenuMode) === MenuModeEnum.HORIZONTAL;
      });

      return {
        getIsHorizontal,
        prefixCls,
        listData,
        count,
        numberStyle: {},
        searchText,
        pageSize,
        pageIndex,
        draw,
        totalCount,
        ...toRefs(compState),
        visible,
        existUnreadMessage,
        updateExistUnreadMessage,
        existUnreadMessageCount,
        currentRoleCode,
      };
    },

    methods: {
      async getUserNotReadMessage() {
        this.loading = true;
        const data: MessagePageQueryResponseModel = {
          searchText: this.searchText,
          pageSize: this.pageSize,
          pageIndex: this.pageIndex,
          draw: this.draw,
          isRead: 'unread',
        };
        const res = await apiSiteMessageList(data);
        if (res.code === 200) {
          this.listData = res.data.data;
          this.totalCount = res.data.totalCount;
          this.draw += 1;
        }
        this.loading = false;
      },
      getMessage(page) {
        if ((page - 1) * this.pageSize > this.pageIndex) {
          this.pageIndex = (page - 1) * this.pageSize;
          this.getUserNotReadMessage();
        }
      },
      visibleChange(visible) {
        this.visible = visible;
        if (visible) {
          this.getUserNotReadMessage();
        }
      },
      onNoticeClick(record) {
        this.visible = false;
        this.$.emit('viewMessage', record.id);
      },
    },
  });
</script>
<style lang="less">
  @prefix-cls: ~'@{namespace}-header-notify';

  .@{prefix-cls} {
    padding-top: 2px;

    &__overlay {
      max-width: 360px;
    }

    .ant-tabs-content {
      width: 300px;
    }

    .ant-badge {
      font-size: 18px;

      .ant-badge-multiple-words {
        padding: 0 4px;
      }

      svg {
        width: 0.9em;
      }
    }
  }

  .unread-message-count {
    .ant-badge-count {
      font-size: 10px !important;
      top: 13px !important;
    }

    .ant-badge-multiple-words {
      padding: 0 5px;
    }
  }
</style>
