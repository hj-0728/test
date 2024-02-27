<template>
  <div ref="teamMemberRef" class="team-member-list">
    <BasicModal
      v-bind="$attrs"
      wrap-class-name="full-modal"
      :showOkBtn="false"
      :showCancelBtn="false"
      :canFullscreen="false"
      :draggable="false"
      :keyboard="false"
      :maskClosable="false"
      :loading="loading"
      :destroyOnClose="false"
      @register="register"
      :getContainer="() => $refs.teamMemberRef"
      title="Modal Title"
      width="65%"
      @cancel="close"
    >
      <template #title>
        <span class="inline-flex-center">
          <Icon icon="fluent:people-team-24-regular" :size="16" style="margin-right: 5px" />
          【{{ teamName }}】小组成员
        </span>
      </template>
      <div>
        <BasicTable
          :dataSource="tableData"
          :canResize="true"
          :loading="loading"
          :scroll="{ y: 'calc(66vh - 155px)' }"
          :showIndexColumn="false"
          @register="registerTable"
          @change="onChange"
          :pagination="false"
          :getPopupContainer="(triggerNode) => triggerNode.parentNode"
        >
          <template #tableTitle>
            <InputSearch
              v-model:value="searchText"
              placeholder="搜索"
              enter-button
              @search="onSearch"
              style="padding: 10px 0 10px 0; width: 30%"
            />
          </template>
          <template #toolbar>
            <Button
              type="primary"
              color="edit"
              :iconSize="18"
              preIcon="ant-design:plus-outlined"
              class="ant-btn-left-margin"
              title="选择通讯录人员"
              @click="addTeamMember('ADMINISTRATION')"
              >选择通讯录人员
            </Button>
            <Button
              type="primary"
              :iconSize="18"
              preIcon="ant-design:plus-outlined"
              class="ant-btn-left-margin"
              title="选择家校通讯录人员"
              @click="addTeamMember('EDU')"
              >选择家校通讯录人员
            </Button>
          </template>
          <template #bodyCell="{ column, record }">
            <template v-if="column.dataIndex === 'operation'">
              <Button
                type="primary"
                color="error"
                :iconSize="16"
                style="margin-left: 10px"
                preIcon="material-symbols:delete-outline-rounded"
                @click="deleteTeamMember(record)"
              >
                删除
              </Button>
            </template>
          </template>
        </BasicTable>
      </div>
      <template #footer>
        <Button @click="close" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
      </template>
    </BasicModal>
  </div>
  <PeopleSelectModal
    ref="refPeopleSelectModal"
    @register="registerPeopleSelectModal"
    @update-team-member-list="updateTeamMemberList"
    @save-member-error="saveMemberError"
  />
</template>
<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { BasicTable, useTable } from '/@/components/Table';
  import { BasicModal, useModal, useModalInner } from '/@/components/Modal';
  import { Icon } from '/@/components/Icon';
  import { Button } from '/@/components/Button';
  import { Input } from 'ant-design-vue';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { getTeamMemberColumns } from '/@/views/team/teamMemberComponents/teamMemberTableData';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { apiDeleteTeamMember, apiGetTeamMemberList } from '/@/api/teamMember/teamMember';
  import PeopleSelectModal from '/@/views/team/teamMemberComponents/PeopleSelectModal.vue';
  export default defineComponent({
    components: {
      BasicModal,
      Icon,
      Button,
      BasicTable,
      InputSearch: Input.Search,
      PeopleSelectModal,
    },
    emits: ['register', 'refresh', 'saveError'],
    setup() {
      const total = ref(0);
      const tableData = ref([]);
      const tableHeight = ref<Number>(getTableHeight(document));
      const teamName = ref<string>('');
      const [registerTable, { setPagination, setLoading }] = useTable({
        columns: getTeamMemberColumns(),
        bordered: true,
      });
      const setPaginationInfo = () => {
        setPagination({
          total: total.value,
          pageSize: params.pageSize,
          current: params.pageIndex + 1,
        });
      };
      const teamId = ref<string>('');
      const [register, { closeModal }] = useModalInner((data) => {
        teamId.value = data.teamId;
        teamName.value = data.teamName;
        params.teamId = data.teamId;
        params.searchText = '';
        console.log(teamId.value, 'teamId');
        getTeamMemberList();
      });
      const params = reactive({
        searchText: '',
        pageSize: 20,
        pageIndex: 0,
        draw: 1,
        teamId: teamId.value,
      });
      const [registerPeopleSelectModal, { openModal: openPeopleSelectModal }] = useModal();

      const getTeamMemberList = () => {
        setLoading(true);
        apiGetTeamMemberList(params)
          .then((res) => {
            if (res.code === 200) {
              // total.value = res.data.filterCount;
              tableData.value = res.data;
              // setPaginationInfo();
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
              description: '网络错误',
            });
          })
          .finally(() => {
            setLoading(false);
          });
      };
      const loading = ref<boolean>(false);
      return {
        ...toRefs(params),
        register,
        getTeamMemberList,
        total,
        loading,
        tableData,
        tableHeight,
        registerTable,
        setLoading,
        closeModal,
        setPaginationInfo,
        teamId,
        teamName,
        registerPeopleSelectModal,
        openPeopleSelectModal,
      };
    },
    methods: {
      onSearch() {
        this.pageIndex = 0;
        this.draw++;
        this.getTeamMemberList();
      },
      init() {
        this.setLoading(true);
        this.draw = 1;
        this.total = 0;
      },
      onChange(pageInfo) {
        this.init();
        this.pageSize = pageInfo.pageSize;
        this.pageIndex = pageInfo.current - 1;
        this.getTeamMemberList();
      },
      deleteTeamMember(record) {
        const currentTime = new Date();
        const paramTime = new Date(record.finishAt);
        if (currentTime < paramTime) {
          useMessage().createConfirm({
            iconType: 'info',
            title: '提示',
            content: `确定要删除该小组成员吗？`,
            onOk: () => {
              apiDeleteTeamMember(record.id)
                .then((res) => {
                  if (res.code === 200) {
                    useMessage().createSuccessNotification({
                      message: '成功',
                      description: '删除成功',
                    });
                    this.getTeamMemberList();
                  } else {
                    useMessage().createErrorNotification({
                      message: '错误',
                      description: res.error.message,
                    });
                    this.$emit('saveError');
                  }
                })
                .catch(() => {
                  useMessage().createErrorNotification({
                    message: '错误',
                    description: '网络错误',
                  });
                })
                .finally(() => {
                  // this.loading = false;
                });
            },
            onCancel() {},
          });
        } else {
          useMessage().createErrorNotification({
            message: '错误',
            description: '此小组成员已删除',
          });
        }
      },
      close() {
        this.$emit('refresh');
        this.closeModal();
      },
      addTeamMember(dimensionCategory) {
        this.openPeopleSelectModal(true, {
          dimensionCategory: dimensionCategory,
          teamId: this.teamId,
        });
      },
      updateTeamMemberList() {
        this.getTeamMemberList();
      },
      saveMemberError() {
        this.$emit('saveError');
      },
      onCloseModal() {
        this.$refs.refPeopleSelectModal?.closeModal();
        this.closeModal();
      },
    },
  });
</script>
<style lang="less" scoped>
  .team-member-list {
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
