<template>
  <div ref="selectPeopleRef" class="select-people-list">
    <BasicModal
      v-bind="$attrs"
      :canFullscreen="false"
      :draggable="false"
      :keyboard="false"
      wrap-class-name="full-modal"
      :maskClosable="false"
      :loading="loadingModal"
      :showOkBtn="false"
      :showCancelBtn="false"
      @register="register"
      @visible-change="handleVisibleChange"
      width="60%"
      :getContainer="() => $refs.selectPeopleRef"
      :footer="null"
    >
      <template #title>
        <span class="inline-flex-center">
          <Icon icon="mdi:checkbox-marked-circle-outline" :size="16" style="margin-right: 5px" />
          选择关联人员
        </span>
      </template>
      <div>
        <BasicTable
          :dataSource="tableData"
          @register="registerTable"
          :showIndexColumn="false"
          :loading="loading"
          bordered
          :canResize="true"
          rowKey="id"
          @change="onChange"
          :pagination="{ total: total, pageSize: params.pageSize, current: params.pageIndex + 1 }"
          :scroll="{ y: 'calc(66vh - 190px)' }"
          :getPopupContainer="(triggerNode) => triggerNode.parentNode"
        >
          <template #tableTitle>
            <InputSearch
              v-model:value="params.searchText"
              placeholder="搜索"
              enter-button
              @search="onSearch"
              style="width: 50%"
            />
          </template>
          <template #bodyCell="{ column, record }">
            <template v-if="column.dataIndex === 'operation'">
              <Button
                type="primary"
                color="edit"
                preIcon="ep:select"
                @click="selectPeople(record)"
                class="select-button"
              >
                选择
              </Button>
            </template>
          </template>
        </BasicTable>
      </div>
    </BasicModal>
  </div>
</template>
<script lang="ts">
  import { defineComponent, ref, reactive } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Icon } from '/@/components/Icon';
  import { useI18n } from '/@/hooks/web/useI18n';
  import { BasicTable, useTable } from '/@/components/Table';
  import { Input } from 'ant-design-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { BasicPageQueryParamsModel } from '/@/api/model/baseModel';
  import { getBasicPeopleColumns } from '/@/views/accountManage/teacherAccount/userTableData';
  import { Button } from '/@/components/Button';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { apiGetPeopleBindUserPage } from '/@/api/people/people';
  export default defineComponent({
    components: {
      BasicModal,
      Icon,
      BasicTable,
      InputSearch: Input.Search,
      Button,
    },
    emits: ['selectedPeople', 'register'],
    setup() {
      const tableHeight = ref(getTableHeight(document));
      const [register, { closeModal }] = useModalInner((data) => {
        onDataReceive(data);
      });

      const total = ref(0);
      const [registerTable, { setPagination, setLoading }] = useTable({
        columns: getBasicPeopleColumns(),
      });
      const loading = ref(false);
      const loadingModal = ref(false);
      const { t } = useI18n();
      const tableData = ref([]);
      const params: BasicPageQueryParamsModel = reactive({
        searchText: '',
        pageSize: 20,
        pageIndex: 0,
        draw: 1,
      });
      const selectedId = ref('');
      function onDataReceive(data) {
        getPeopleList();
        selectedId.value = data;
        console.log('selectId', data);
      }
      const getPeopleList = () => {
        apiGetPeopleBindUserPage(params)
          .then((res) => {
            if (res.code === 200) {
              total.value = res.data.filterCount;
              tableData.value = res.data.data;
              setPaginationInfo();
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
              description: '网络异常',
            });
          })
          .finally(() => {
            setLoading(false);
          });
      };

      const setPaginationInfo = () => {
        setPagination({
          current: params.pageIndex + 1,
          total: total.value,
          pageSize: params.pageSize,
        });
      };
      return {
        register,
        loading,
        t,
        closeModal,
        registerTable,
        tableData,
        params,
        total,
        getPeopleList,
        setLoading,
        tableHeight,
        loadingModal,
        selectedId,
      };
    },
    methods: {
      selectPeople(data) {
        this.selectedId = '';
        this.$nextTick(() => {
          this.selectedId = data.id;
          this.$emit('selectedPeople', data);
          this.init();
          this.params.searchText = '';
          this.closeModal();
        });
      },

      handleVisibleChange(v) {
        if (!v) {
          this.loadingModal = false;
          this.tableData = [];
          this.init();
          this.params.searchText = '';
        } else {
          this.getPeopleList();
        }
      },
      init() {
        this.params.draw += 1;
        this.params.pageIndex = 0;
        this.setLoading(true);
        this.total = 0;
      },
      onChange(pageInfo) {
        this.init();
        this.params.pageSize = pageInfo.pageSize;
        this.params.pageIndex = pageInfo.current - 1;
        this.setLoading(true);
        this.getPeopleList();
      },
      onSearch() {
        this.init();
        this.getPeopleList();
      },
    },
  });
</script>

<style scoped lang="less">
  .select-people-list {
    ::v-deep(.ant-modal-body) {
      .scrollbar {
        height: 66vh;
      }
    }

    ::v-deep(.scroll-container .scrollbar__wrap) {
      margin-bottom: 0 !important;
    }

    ::v-deep(.ant-pagination-options) {
      .ant-select-dropdown {
        position: fixed;
      }
    }
  }
</style>
