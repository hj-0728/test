<template>
  <div>
    <PageWrapper>
      <div style="height: calc(100vh - 85px); background: white">
        <BasicTable
          :dataSource="tableData"
          :canResize="true"
          :loading="loading"
          :scroll="{ x: 0 | false, y: tableHeight }"
          :showIndexColumn="false"
          @register="registerTable"
          @change="onChange"
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
              color="success"
              :iconSize="18"
              preIcon="ant-design:plus-outlined"
              class="ant-btn-left-margin"
              title="添加"
              @click="addTeamCategory()"
              >添加
            </Button>
          </template>
          <template #bodyCell="{ column, record }">
            <template v-if="column.dataIndex === 'isActivated'">
              <Switch
                v-model:checked="record.isActivated"
                checked-children="启用"
                un-checked-children="禁用"
                @change="onChangeTeamCategoryActivated(record)"
              />
            </template>
            <template v-if="column.dataIndex === 'operation'">
              <Button
                type="primary"
                color="edit"
                :iconSize="16"
                preIcon="ant-design:edit-twotone"
                @click="editTeamCategory(record)"
              >
                编辑
              </Button>
              <Button
                type="primary"
                class="team-button-style"
                :iconSize="16"
                preIcon="bi:microsoft-teams"
                style="margin-left: 10px"
                @click="toTeam(record)"
              >
                小组
              </Button>
            </template>
          </template>
        </BasicTable>
        <Edit @register="register" ref="refTeamCategoryEditor" @save-success="saveSuccess" />
      </div>
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { getBasicColumns } from './teamCategoryTableData';
  import { apiGetTeamCategoryList, apiChangeActivated } from '/@/api/teamCategory/teamCategory';
  import { PageWrapper } from '/@/components/Page';
  import { BasicTable, useTable } from '/@/components/Table';
  import { Input, Switch } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import Edit from './components/Edit.vue';
  import { useModal } from '/@/components/Modal';
  import { getTableHeight } from '/@/utils/helper/tableHelper';

  export default defineComponent({
    components: {
      PageWrapper,
      BasicTable,
      InputSearch: Input.Search,
      Button,
      Switch,
      Edit,
    },
    emits: ['register'],
    setup() {
      const refTeamCategoryEditor = ref();
      const total = ref(0);
      const loading = ref(false);
      const tableData = ref([]);
      const tableHeight = ref<Number>(getTableHeight(document));
      const [registerTable, { setPagination, setLoading }] = useTable({
        columns: getBasicColumns(),
        bordered: true,
      });
      const [register, { openModal }] = useModal();
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
        isActivated: '',
      });
      const getTeamCategoryList = () => {
        apiGetTeamCategoryList(params)
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
      getTeamCategoryList();
      return {
        loading,
        total,
        tableData,
        tableHeight,
        registerTable,
        setLoading,
        setPaginationInfo,
        ...toRefs(params),
        getTeamCategoryList,
        register,
        openModal,
        refTeamCategoryEditor,
      };
    },
    mounted() {
      this.getTeamCategoryList();
    },
    methods: {
      onSearch() {
        this.init();
        this.pageIndex = 0;
        this.getTeamCategoryList();
      },
      init() {
        this.setLoading(true);
        this.draw = 1;
        this.total = 0;
      },
      onChange(pageInfo, filters) {
        this.init();
        this.isActivated = '';
        if (filters['isActivated'] && filters['isActivated'].length > 0) {
          this.isActivated = filters['isActivated'][0];
        }
        this.pageSize = pageInfo.pageSize;
        this.pageIndex = pageInfo.current - 1;
        this.getTeamCategoryList();
      },
      addTeamCategory() {
        this.openModal(true, { teamCategory: null, category: 'add' });
      },
      editTeamCategory(teamCategory) {
        this.openModal(true, { teamCategory: teamCategory, category: 'edit' });
      },
      saveSuccess() {
        this.getTeamCategoryList();
      },
      toTeam(data) {
        this.$router.push({
          path: `/team-category/team/${data.id}`,
        });
      },
      onChangeTeamCategoryActivated(teamCategory) {
        this.setLoading(true);
        apiChangeActivated(teamCategory)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '修改成功',
              });
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
              this.setLoading(false);
            }
          })
          .catch(() => {
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络错误',
            });
            this.setLoading(false);
          })
          .finally(() => {
            this.getTeamCategoryList();
          });
      },
    },
  });
</script>

<style lang="less" scoped>
  ::v-deep(.zebra-highlight) {
    background: #fafafa;
  }

  .team-button-style {
    background: #4bc0c0;
    border-color: #4bc0c0;
    margin: 0 5px;
  }

  .team-button-style:hover {
    background: #4bc08f;
    border-color: #4bc08f;
  }
</style>
