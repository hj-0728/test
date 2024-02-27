<template>
  <div>
    <LoadingCom :loading="loadingDownload" tip="加载中..." />
    <div ref="modal">
      <BasicModal
        @register="register"
        width="60%"
        :showOkBtn="false"
        :canFullscreen="false"
        :draggable="false"
        :getContainer="() => $refs.modal"
        @visible-change="visibleChange"
      >
        <template #title>
          <div>
            <ContainerOutlined />
            消息详情
          </div>
        </template>
        <View :message-id="messageId" />
        <template #footer>
          <Button @click="closeModal" preIcon="ic:twotone-close" style="top: -1px">取消</Button>
        </template>
      </BasicModal>
    </div>
    <PageWrapper :content-style="{ height: 'calc(100vh - 80px)' }">
      <div style="height: 100%; background: white">
        <BasicTable
          :dataSource="tableData"
          bordered
          :loading="loading"
          :scroll="{ y: tableHeight }"
          :showIndexColumn="false"
          @register="registerTable"
          @change="onChange"
        >
          <template #tableTitle>
            <a-input-search
              v-model:value="searchText"
              placeholder="搜索"
              enter-button
              @search="onSearch"
              style="padding: 10px 0 10px 0; width: 30%"
            />
          </template>
          <template #bodyCell="{ record, column }">
            <template v-if="column.dataIndex === 'readAt'">
              <Tag v-if="!record.readAt" color="error">未读</Tag>
              <Tag v-else color="success">已读</Tag>
            </template>
            <template v-if="column.dataIndex === 'operation'">
              <Button
                type="primary"
                preIcon="ant-design:eye-outlined"
                :iconSize="16"
                @click="viewMessage(record)"
                color="info"
                title="查看"
              >
                查看
              </Button>
              <Button
                class="ant-btn-left-margin"
                type="primary"
                color="green"
                preIcon="ph:download-simple"
                :iconSize="16"
                @click="downloadFile(record)"
                v-if="record.fileId"
              >
                下载
              </Button>
            </template>
          </template>
        </BasicTable>
      </div>
    </PageWrapper>
  </div>
</template>
<script lang="ts">
  import { PageWrapper } from '/@/components/Page';
  import { BasicTable, useTable } from '/@/components/Table';
  import { useModal, BasicModal } from '/@/components/Modal';
  import { Loading } from '/@/components/Loading';
  import { computed, defineComponent, ref } from 'vue';
  import { Tag } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { getBasicColumns } from '/@/views/siteMessage/messageTableData';
  import { MessagePageQueryResponseModel } from '/@/api/siteMessage/siteMessageModel';
  import { apiReadSiteMessage, apiSiteMessageList } from '/@/api/siteMessage/siteMessage';
  import View from './View.vue';
  import dayjs from 'dayjs';
  import { ContainerOutlined } from '@ant-design/icons-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { getAuthCache } from '/@/utils/auth';
  import { USER_INFO_KEY } from '/@/enums/cacheEnum';
  import { UserInfo } from '/#/store';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { apiGetFileDownloadUrl } from '/@/api/storage/storage';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import { useAppStore } from '/@/store/modules/app';

  export default defineComponent({
    components: {
      PageWrapper,
      BasicTable,
      BasicModal,
      View,
      Tag,
      ContainerOutlined,
      LoadingCom: Loading,
      Button,
    },
    $refs: { PeopleInDeptTableRef: HTMLFormElement, Loading },
    setup() {
      const tableData = ref([]);
      const showIcon = ref<boolean>(true);
      const loading = ref<boolean>(true);
      const loadingDownload = ref<boolean>(false);

      const messageCategoryFilters = ref<object[] | undefined>(undefined);
      const currentUserInfo: UserInfo = getAuthCache(USER_INFO_KEY);
      const currentRoleCode: string = currentUserInfo.currentRole.code;
      const [registerTable, { setPagination }] = useTable({
        columns: getBasicColumns(messageCategoryFilters),
        bordered: true,
      });
      const searchText = ref<string>('');
      const page = ref<number>(1);
      const pageSize = ref<number>(20);
      const pageIndex = ref<number>(0);
      const draw = ref<number>(1);
      const currentPage = ref<number>(1);
      const total = ref<number>(0);
      const pagination = ref({});

      function setPaginationInfo() {
        setPagination({
          current: currentPage.value,
          total: total.value,
          pageSize: pageSize.value,
        });
      }

      const appStore = useAppStore();
      const updateUnreadStatusFlag = computed(() => {
        return appStore.getUpdateUnreadStatusFlag;
      });

      const tableHeight = ref<Number>(getTableHeight(document));

      const messageId = ref('');

      const [register, { openModal, closeModal }] = useModal();

      const sortName = ref();
      const orderBy = ref();
      const category = ref([]);
      const isRead = ref('');

      return {
        showIcon,
        loading,
        tableData,
        registerTable,
        searchText,
        page,
        pageSize,
        pageIndex,
        draw,
        currentPage,
        total,
        pagination,
        setPaginationInfo,
        tableHeight,
        messageId,
        register,
        openModal,
        closeModal,
        orderBy,
        sortName,
        category,
        isRead,
        loadingDownload,
        currentRoleCode,
        updateUnreadStatusFlag,
      };
    },
    watch: {
      updateUnreadStatusFlag(value) {
        if (value) {
          this.onLoadList();
        }
      },
    },
    created() {
      this.onLoadList();
    },
    methods: {
      init() {
        this.pageSize = 20;
        this.pageIndex = 0;
        this.draw = 1;
        this.currentPage = 1;
        this.total = 0;
        this.loading = true;
      },
      onChange(pageInfo, filters, sorter) {
        this.category = [];
        this.isRead = '';
        this.sortName = '';
        this.orderBy = '';
        if (sorter.order === 'ascend') {
          this.sortName = sorter.columnKey;
          this.orderBy = 'asc';
        } else if (sorter.order === 'descend') {
          this.sortName = sorter.columnKey;
          this.orderBy = 'desc';
        }
        this.pageSize = pageInfo.pageSize;
        this.currentPage = pageInfo.current;
        this.pageIndex = this.currentPage - 1;
        if (filters['category'] && filters['category'].length > 0) {
          for (let i = 0; i < filters['category'].length; i++) {
            this.category.push(filters['category'][i]);
          }
        }
        if (filters['readAt'] && filters['readAt'].length > 0) {
          this.isRead = filters['readAt'][0];
        }
        this.onLoadList();
      },
      onSearch() {
        this.init();
        this.onLoadList();
      },
      async onLoadList() {
        this.loading = true;
        const messageSearchData: MessagePageQueryResponseModel = {
          searchText: this.searchText,
          pageSize: this.pageSize,
          pageIndex: this.pageIndex,
          draw: this.draw,
          sortName: this.sortName,
          orderBy: this.orderBy,
          category: this.category,
          isRead: this.isRead,
        };
        const res = await apiSiteMessageList(messageSearchData);
        if (res.code === 200) {
          this.tableData = res.data.data;
          this.tableData.map((item) => {
            item.createdAt = dayjs(item.createdAt).format('YYYY-MM-DD HH:mm');
          });
          this.total = res.data.filterCount;
          this.setPaginationInfo();
          // this.draw += 1;
        }
        if (res.code !== 200) {
          useMessage().createErrorNotification({
            message: '操作失败',
            description: `获取消息失败${res.error.message}`,
          });
        }
        this.loading = false;
      },
      viewMessage(record) {
        this.messageId = record.id;
        this.openModal();
      },
      visibleChange(visible) {
        if (!visible) {
          this.onLoadList();
        }
      },
      downloadFile(record) {
        this.loadingDownload = true;
        apiGetFileDownloadUrl(record.fileId)
          .then((res) => {
            if (res.code === 200) {
              window.location.href = res.data;
              useMessage().createSuccessNotification({
                message: '操作成功',
                description: '文件下载完成',
              });
              this.readSiteMessage(record.id);
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .finally(() => {
            this.loadingDownload = false;
          });
      },
      getFilenameFromHeader(res) {
        let fileName = res.headers['content-disposition'].split('filename*=')[1].split(';')[0];
        fileName = decodeURIComponent(fileName).replace(/UTF-8''/g, '');
        fileName = decodeURIComponent(fileName).replaceAll('"', '');
        return fileName;
      },
      readSiteMessage(messageId) {
        this.loadingDownload = true;
        apiReadSiteMessage(messageId)
          .then((res) => {
            if (res.code === 200) {
              this.init();
              this.onLoadList();
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch(() => {
            useMessage().createErrorNotification({
              message: '错误',
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
          })
          .finally(() => {
            this.loadingDownload = false;
          });
      },
    },
  });
</script>

<style scoped>
  :deep(.basic-tree-header) {
    border-bottom: 0;
  }
</style>
