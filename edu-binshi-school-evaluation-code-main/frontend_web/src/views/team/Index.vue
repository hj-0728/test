<template>
  <div style="background: #ececec; height: 88vh">
    <PageWrapper>
      <div class="content">
        <Card class="card">
          <template #title>
            <div style="display: flex; align-items: center">
              <Tag color="green" v-if="teamCategory && teamCategory.isActivated"> 已启用 </Tag>
              <Tag color="red" v-else> 已禁用 </Tag>
              <span style="font-size: 16px; font-weight: bold; line-height: 16px">{{
                teamCategoryName
              }}</span>
            </div>
          </template>
          <template #extra>
            <InputSearch
              v-model:value="searchText"
              placeholder="搜索"
              enter-button
              @search="onSearch"
              style="padding: 10px 0 10px 0; width: 20vw"
            />
            <Button
              v-if="teamCategory && teamCategory.isActivated"
              type="primary"
              color="success"
              :iconSize="18"
              preIcon="ant-design:plus-outlined"
              class="ant-btn-left-margin mg-top"
              title="添加"
              @click="addTeam()"
              >添加
            </Button>
          </template>
          <BasicTable
            :dataSource="tableData"
            :canResize="true"
            :loading="loading"
            :scroll="{ x: 0 | false, y: 'calc(89vh - 175px)' }"
            :showIndexColumn="false"
            @register="registerTable"
            @change="onChange"
          >
            <template #bodyCell="{ column, record }">
              <template v-if="column.dataIndex === 'memberList'">
                <div
                  v-for="(memberCount, index) in record['memberList']"
                  :key="index"
                  :style="{ color: colorList[index] }"
                  class="member"
                >
                  <span>{{ memberCount }}</span>
                  <span v-if="index < record['memberList'].length - 1"> /&nbsp;</span>
                </div>
              </template>
              <template v-if="column.dataIndex === 'operation'">
                <div v-if="record.isSelfCreate && teamCategory.isActivated">
                  <Button
                    type="primary"
                    color="edit"
                    :iconSize="16"
                    preIcon="ant-design:edit-twotone"
                    @click="editTeam(record)"
                  >
                    编辑
                  </Button>
                  <Button
                    type="primary"
                    class="ant-btn-left-margin"
                    :iconSize="16"
                    preIcon="ant-design:team-outlined"
                    @click="setTeamMember(record)"
                  >
                    小组成员
                  </Button>
                  <Button
                    type="primary"
                    color="error"
                    :iconSize="16"
                    class="ant-btn-left-margin"
                    preIcon="material-symbols:delete-outline-rounded"
                    @click="deleteTeam(record)"
                  >
                    删除
                  </Button>
                </div>
                <Button
                  v-else
                  type="primary"
                  color="info"
                  :iconSize="16"
                  preIcon="ant-design:eye-outlined"
                  @click="viewTeam(record)"
                >
                  查看
                </Button>
              </template>
            </template>
          </BasicTable>
        </Card>
        <Edit
          @register="register"
          ref="refTeamEditor"
          @save-success="saveSuccess"
          @save-error="saveError"
        />
        <View @register="registerViewTeamModal" ref="refTeamViewer" />
        <TeamMemberListModal
          @register="registerTeamMemberModal"
          ref="refSetTeamMember"
          @refresh="saveSuccess"
          @save-error="saveError"
        />
      </div>
    </PageWrapper>
  </div>
</template>
<script lang="ts">
  import { BasicTable, useTable } from '/@/components/Table';
  import { PageWrapper } from '/@/components/Page';
  import { Button } from '/@/components/Button';
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { Card, Input, Tag } from 'ant-design-vue';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { getBasicColumns } from '/@/views/team/teamTableData';
  import { useModal } from '/@/components/Modal';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { apiDeleteTeam, apiGetTeamList } from '/@/api/team/team';
  import Edit from '/@/views/team/components/Edit.vue';
  import TeamMemberListModal from '/@/views/team/teamMemberComponents/TeamMemberListModal.vue';
  import { apiGetTeamCategoryDetail } from '/@/api/teamCategory/teamCategory';
  import View from '/@/views/team/components/View.vue';

  export default defineComponent({
    components: {
      Tag,
      Edit,
      TeamMemberListModal,
      PageWrapper,
      BasicTable,
      InputSearch: Input.Search,
      Button,
      Card,
      View,
    },
    emits: ['register'],
    setup() {
      const colorList = ref<string[]>([]);
      colorList.value = ['#63b2ee', '#76da91', '#f8cb7f', '#f89588', '#7cd6cf'];
      const state = window.history.state.current;
      const teamCategoryId = state.split('/')[3];
      const teamCategory = ref<object>({});
      const teamCategoryName = ref('');
      const total = ref(0);
      const loading = ref(true);
      const tableData = ref([]);
      const tableHeight = ref<Number>(getTableHeight(document));
      const [registerTable, { setPagination, setLoading }] = useTable({
        columns: getBasicColumns(),
        bordered: true,
      });
      const [register, { openModal }] = useModal();
      const [registerViewTeamModal, { openModal: openViewTeamModal }] = useModal();
      const [registerTeamMemberModal, { openModal: openTeamMemberModal }] = useModal();
      const setPaginationInfo = () => {
        setPagination({
          total: total.value,
          pageSize: params.pageSize,
          current: params.pageIndex + 1,
        });
      };
      const params = reactive({
        searchText: '',
        pageSize: 20,
        pageIndex: 0,
        draw: 1,
        teamCategoryId: teamCategoryId,
      });
      const getTeamList = () => {
        apiGetTeamList(params)
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
              description: '网络错误',
            });
          })
          .finally(() => {
            setLoading(false);
          });
      };
      return {
        colorList,
        total,
        loading,
        tableData,
        tableHeight,
        teamCategory,
        registerTable,
        setLoading,
        setPaginationInfo,
        getTeamList,
        ...toRefs(params),
        register,
        openModal,
        registerTeamMemberModal,
        openTeamMemberModal,
        teamCategoryName,
        registerViewTeamModal,
        openViewTeamModal,
      };
    },
    mounted() {
      this.getTeamList();
      this.getTeamCategory();
    },
    methods: {
      getTeamCategory() {
        apiGetTeamCategoryDetail(this.teamCategoryId)
          .then((res) => {
            if (res.code === 200) {
              console.log(res.data, 'res.data');
              this.teamCategory = res.data;
              if (!res.data.isActivated) {
                this.$refs.refTeamEditor.close();
                this.$refs.refSetTeamMember.onCloseModal();
              }
              this.teamCategoryName = '小组类型: ' + res.data.name;
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
              description: '1',
            });
          })
          .finally(() => {
            this.setLoading(false);
          });
      },
      onSearch() {
        this.init();
        this.pageIndex = 0;
        this.getTeamList();
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
        this.getTeamList();
      },
      saveSuccess() {
        this.getTeamList();
      },
      deleteTeam(data) {
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: `确定要删除【<text style="color: #00acc1">${data.name}</text>】吗？`,
          onOk: () => {
            this.doDeleteTeam(data.id);
          },
          onCancel() {},
        });
      },
      doDeleteTeam(teamId) {
        apiDeleteTeam(teamId)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '成功',
                description: '删除成功',
              });
              this.getTeamList();
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
              this.saveError();
            }
          })
          .catch(() => {
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络错误',
            });
          })
          .finally(() => {
            this.loading = false;
          });
      },
      addTeam() {
        this.openModal(true, { teamCategoryId: this.teamCategoryId, category: 'add' });
      },
      editTeam(team) {
        this.openModal(true, {
          teamId: team.id,
          teamCategoryId: this.teamCategoryId,
          category: 'edit',
        });
      },
      viewTeam(team) {
        this.openViewTeamModal(true, {
          teamId: team.id,
        });
      },
      setTeamMember(data) {
        console.log(data);
        this.openTeamMemberModal(true, { teamId: data.id, teamName: data.name });
      },
      saveError() {
        this.getTeamList();
        this.getTeamCategory();
      },
    },
  });
</script>

<style lang="less" scoped>
  ::v-deep(.zebra-highlight) {
    background: #fafafa;
  }

  ::v-deep(.ant-card-extra) {
    width: 27vw;
    padding: 6px 0;
  }

  //::v-deep(.ant-card-body) {
  //  padding: 15px 0 15px 0;
  //}

  .mg-top {
    margin-top: 10px;
  }

  .member {
    display: inline-block;
  }
</style>
