<template>
  <div style="height: calc(100vh - 185px); background: white">
    <BasicTable
      :dataSource="tableData"
      :canResize="true"
      :loading="loading"
      :scroll="{ y: 'calc(66vh - 175px)' }"
      :showIndexColumn="false"
      row-key="id"
      @register="registerTable"
      @change="onChange"
      :rowSelection="{
        type: selectType,
        selectedRowKeys: selectedPeopleKeys,
        onSelectAll: onSelectAll,
        onSelect: onSelect,
      }"
      @row-click="onRowClick"
      :pagination="{
        total: total,
        pageSize: pageSize,
        current: pageIndex + 1,
        showQuickJumper: false,
      }"
      :getPopupContainer="(triggerNode) => triggerNode.parentNode"
    >
      <template #tableTitle>
        <InputSearch
          v-model:value="searchText"
          placeholder="搜索"
          enter-button
          @search="onSearch"
          style="padding: 5px 0; width: 30%"
        />
      </template>
      <template #toolbar>
        <Button
          type="primary"
          color="success"
          :iconSize="18"
          preIcon="ant-design:check-outlined"
          class="ant-btn-left-margin"
          title="确认"
          @click="confirmSelect()"
          >确认
        </Button>
      </template>
    </BasicTable>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { BasicTable, useTable } from '/@/components/Table';
  import { getBasicColumns } from '/@/views/team/teamMemberComponents/PeopleTableData';
  import { Input } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { useModal } from '/@/components/Modal';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { apiGetTeamCanSelectPeopleList, apiSaveTeamMember } from '/@/api/teamMember/teamMember';

  export default defineComponent({
    components: {
      BasicTable,
      InputSearch: Input.Search,
      Button,
    },
    props: {
      dimensionDeptTreeId: {
        type: String,
        default: '',
      },
      dimensionCategory: {
        type: String,
        default: '',
      },
      teamId: {
        type: String,
        default: '',
      },
    },
    emits: ['confirmSelectPeople', 'saveTeamMemberError'],
    setup(props) {
      const [registerSetSubjectModal, { openModal: openSetSubjectModal }] = useModal();
      const total = ref(0);
      const tableHeight = ref(getTableHeight(document));
      const loading = ref(false);
      const tableData = ref([]);
      const params = reactive({
        pageSize: 20,
        pageIndex: 0,
        searchText: '',
        draw: 1,
        dimensionDeptTreeId: props.dimensionDeptTreeId,
        dimensionCategory: props.dimensionCategory,
        teamId: props.teamId,
      });
      const selectType = ref('checkbox');
      const selectedPeopleKeys = ref<string[]>([]);
      const columns = ref();
      columns.value = getBasicColumns();
      const [registerTable, { setSelectedRowKeys }] = useTable({
        columns: columns.value,
        bordered: true,
      });
      const getTeamCanSelectPeoplePage = () => {
        loading.value = true;
        apiGetTeamCanSelectPeopleList(params)
          .then((res) => {
            console.log(res);
            if (res.code === 200) {
              total.value = res.data.filterCount;
              tableData.value = res.data.data;
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
            loading.value = false;
          });
      };
      getTeamCanSelectPeoplePage();

      const onSelectChange = (selectedRowKeys) => {
        selectedPeopleKeys.value = selectedRowKeys;
      };
      return {
        loading,
        selectType,
        selectedPeopleKeys,
        registerTable,
        ...toRefs(params),
        params,
        tableData,
        tableHeight,
        total,
        getTeamCanSelectPeoplePage,
        registerSetSubjectModal,
        openSetSubjectModal,
        setSelectedRowKeys,
        onSelectChange,
      };
    },
    methods: {
      onRowClick(record, _index, _event) {
        this.onSelect(record);
      },
      onSearch() {
        this.pageIndex = 0;
        this.getTeamCanSelectPeoplePage();
      },
      onChange(pageInfo, _filters) {
        this.pageSize = pageInfo.pageSize;
        this.pageIndex = pageInfo.current - 1;
        this.getTeamCanSelectPeoplePage();
      },
      init() {
        this.pageSize = 20;
        this.pageIndex = 0;
        this.searchText = '';
        this.draw = 1;
      },
      onSelectAll(_selected, _selectedRows, changeRows) {
        for (const row of changeRows) {
          this.selectPeople(row);
        }
      },
      onSelect(record) {
        this.selectPeople(record);
      },
      selectPeople(row) {
        const idx = this.selectedPeopleKeys.indexOf(row.id);
        if (idx < 0) {
          if (this.selectType === 'radio') {
            this.selectedPeopleKeys = [row.id];
          } else {
            this.selectedPeopleKeys.push(row.id);
          }
        } else {
          this.selectedPeopleKeys.splice(idx, 1);
        }
      },
      confirmSelect() {
        this.loading = true;
        let memberGroupByCapacityCode = [
          {
            capacityCode: 'LEADER',
            memberList: [],
          },
          {
            capacityCode: 'MEMBER',
            memberList: [],
          },
          {
            capacityCode: 'HEAD_TEACHER',
            memberList: [],
          },
          {
            capacityCode: 'TEACHER',
            memberList: [],
          },
          {
            capacityCode: 'STUDENT',
            memberList: [],
          },
        ];
        this.selectedPeopleKeys.forEach((val) => {
          const valList = val.split('&&');
          memberGroupByCapacityCode.forEach((item) => {
            if (valList[2] === item.capacityCode) {
              item.memberList.push({
                peopleId: valList[0],
                capacityId: valList[1],
              });
            }
          });
        });
        apiSaveTeamMember({
          teamId: this.teamId,
          memberGroupByCapacityList: memberGroupByCapacityCode,
        })
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '成功',
                description: '保存成功',
              });
              this.$emit('confirmSelectPeople');
              this.init();
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
              this.$emit('saveTeamMemberError');
            }
          })
          .catch(() => {
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络异常',
            });
          })
          .finally(() => {
            this.loading = false;
          });
      },
    },
  });
</script>

<style scoped lang="less">
  ::v-deep(.vben-basic-table-header__toolbar) {
    margin-right: 0;
  }
</style>
