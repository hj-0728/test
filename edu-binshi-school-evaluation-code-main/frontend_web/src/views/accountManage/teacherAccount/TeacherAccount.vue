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
              @click="addUser()"
              >添加
            </Button>
          </template>
          <template #bodyCell="{ column, record }">
            <template v-if="column.dataIndex === 'roleNameList'">
              {{ record['roleNameList'].join('、') }}
            </template>
            <template v-if="column.dataIndex === 'isActivated'">
              <Switch
                v-model:checked="record.isActivated"
                :disabled="record.id === currentUserId"
                checked-children="启用"
                un-checked-children="禁用"
                @change="onChangeUserActivated(record)"
                v-model:disabled="switchDisabled"
              />
            </template>
            <template v-if="column.dataIndex === 'operation'">
              <Button
                type="primary"
                color="edit"
                :iconSize="16"
                preIcon="ant-design:edit-twotone"
                @click="edit(record)"
              >
                修改角色
              </Button>
              <Button
                type="primary"
                :iconSize="16"
                preIcon="mdi:lock-reset"
                class="reset-password-button-style"
                @click="resetPassword(record)"
              >
                重置密码
              </Button>
            </template>
          </template>
        </BasicTable>
        <Edit
          @register="register"
          ref="refUserEditor"
          :currentUserRoleCode="currentUserRole.code"
        />
      </div>
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { getBasicColumns } from './userTableData';
  import { apiGetUserTeacherList } from '/@/api/user/user';
  import { PageWrapper } from '/@/components/Page';
  import { BasicTable, useTable } from '/@/components/Table';
  import { Input, Switch } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import Edit from '/@/views/accountManage/teacherAccount/components/Edit.vue';
  import { useModal } from '/@/components/Modal';
  import { getAuthCache } from '/@/utils/auth';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { UserInfo } from '/#/store';
  import { USER_INFO_KEY } from '/@/enums/cacheEnum';
  import { changeUserActivated, resetUserPassword } from '/@/views/accountManage/userFunc';
  import { cloneDeep } from 'lodash-es';

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
      const refUserEditor = ref();
      const total = ref(0);
      const loading = ref(false);
      const tableData = ref([]);
      const tableHeight = ref<Number>(getTableHeight(document));
      const currentUserInfo: UserInfo = getAuthCache(USER_INFO_KEY);
      const currentUserId = currentUserInfo.id;
      const currentUserRole = currentUserInfo.currentRole;
      const switchDisabled = ref(false);
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
        currentUserRoleCode: currentUserRole.code,
      });
      const getUserList = () => {
        apiGetUserTeacherList(params)
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
      getUserList();
      return {
        loading,
        total,
        tableData,
        tableHeight,
        switchDisabled,
        currentUserId,
        registerTable,
        setLoading,
        setPaginationInfo,
        ...toRefs(params),
        getUserList,
        register,
        openModal,
        currentUserRole,
        refUserEditor,
      };
    },
    methods: {
      onSearch() {
        this.init();
        this.pageIndex = 0;
        this.getUserList();
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
        this.getUserList();
      },
      addUser() {
        this.openModal(true, { user: null, category: 'add' });
      },
      edit(user) {
        this.openModal(true, { user: user, category: 'edit' });
      },
      onChangeUserActivated(user) {
        changeUserActivated(user, this);
      },
      resetPassword(user) {
        let teacherUser = cloneDeep(user);
        teacherUser['userType'] = 'TEACHER';
        resetUserPassword(teacherUser, this);
      },
    },
  });
</script>

<style lang="less" scoped>
  ::v-deep(.zebra-highlight) {
    background: #fafafa;
  }

  .reset-password-button-style {
    background: #4bc0c0;
    border-color: #4bc0c0;
    margin: 0 5px;
  }

  .reset-password-button-style:hover {
    background: #4bc08f;
    border-color: #4bc08f;
  }
</style>
