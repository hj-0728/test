<template>
  <div>
    <PageWrapper title="角色管理">
      <div class="md:flex" style="height: calc(100vh - 200px); position: relative">
        <div class="md:w-full w-full h-full" style="background: #ffffff">
          <BasicTable
            titleHelpMessage="温馨提醒"
            :dataSource="tableData"
            :canResize="true"
            :loading="loading"
            :bordered="true"
            :scroll="{ x: 0 | false, y: tableHeight }"
            :showIndexColumn="false"
            @register="registerTable"
          >
            <template #tableTitle>
              <a-input-search
                v-model:value="searchValue"
                placeholder="搜索"
                enter-button
                @search="onSearch"
                style="padding: 10px 0 10px 0; width: 30%"
              />
            </template>
            <template #toolbar>
              <a-button
                type="primary"
                :iconSize="18"
                preIcon="ant-design:plus-outlined"
                class="add-button"
                title="添加角色"
                @click="addRole"
                >添加</a-button
              >
            </template>
            <template #bodyCell="{ column, record }">
              <template v-if="column.dataIndex === 'isActivated'">
                <Switch
                  v-model:checked="record.isActivated"
                  @change="handleChange(record)"
                  checked-children="已启用"
                  un-checked-children="已禁用"
                />
              </template>
              <template v-if="column.dataIndex === 'operation'">
                <a-button
                  type="primary"
                  preIcon="ant-design:edit-twotone"
                  :iconSize="16"
                  @click="editRole(record)"
                  class="edit-button"
                >
                  编辑
                </a-button>
                <a-button
                  type="primary"
                  :iconSize="16"
                  preIcon="ant-design:setting-filled"
                  class="ability-permission-button"
                  @click="openGrantedModalFun(record)"
                >
                  功能权限
                </a-button>
              </template>
            </template>
          </BasicTable>
        </div>
      </div>
      <SaveModel @register="register" />
      <AbilityPermissionAssign @register="registerGranted" />
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { PageWrapper } from '/@/components/Page';
  import { defineComponent, onMounted, ref } from 'vue';
  import { getBasicColumns } from './roleTableData';
  import { useModal } from '/@/components/Modal';
  import { BasicTable, useTable } from '/@/components/Table';
  import { apiGetRolePageList, changeIsActivatedApi } from '/@/api/role/role';
  import { Switch } from 'ant-design-vue';
  import { getAuthCache } from '/@/utils/auth/index';
  import { USER_INFO_KEY } from '/@/enums/cacheEnum';
  import { useMessage } from '/@/hooks/web/useMessage';
  import SaveModel from './saveRoleModel.vue';
  import AbilityPermissionAssign from '/@/components/AbilityPermissionAssign/index.vue';
  import { TRANSITION_NAME, MASK_TRANSITION_NAME } from '/@/settings/transitionSetting';
  import { changeIsActivatedResponseModel, RoleListResponseModel } from '/@/api/model/roleModel';

  export default defineComponent({
    components: {
      PageWrapper,
      BasicTable,
      Switch,
      SaveModel,
      AbilityPermissionAssign,
    },
    setup() {
      // 表格的标题
      const [registerTable] = useTable({
        columns: getBasicColumns(),
        bordered: true,
      });
      const [register, { openModal: openSaveModal }] = useModal();
      const [registerGranted, { openModal: openGrantedModal }] = useModal();
      const tableData = ref<any>([]);
      const searchValue = ref<string>('');
      const loading = ref<boolean>(false);
      const currentOrganization = ref<any>({});
      const tableHeight = ref<Number>(0);
      tableHeight.value = document.body.clientHeight - 400;
      // 获取信息
      const getRoleList = () => {
        const params: RoleListResponseModel = {
          searchText: searchValue.value,
        };
        apiGetRolePageList(params).then((res) => {
          if (res.code === 200) {
            tableData.value = res.data.data;
            loading.value = false;
          }
        });
      };
      onMounted(async () => {
        // @ts-ignore
        currentOrganization.value = getAuthCache(USER_INFO_KEY).currentOrganization;
        await getRoleList();
      });
      return {
        currentOrganization,
        register,
        registerTable,
        registerGranted,
        openGrantedModal,
        openSaveModal,
        tableHeight,
        tableData,
        getRoleList,
        loading,
        TRANSITION_NAME,
        MASK_TRANSITION_NAME,
        searchValue,
      };
    },
    methods: {
      onSearch() {
        this.getRoleList();
      },
      handleChange(record) {
        const params: changeIsActivatedResponseModel = {
          id: record.id,
          version: record.version,
          isActivated: record.isActivated,
        };
        changeIsActivatedApi(params)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '修改成功',
              });
            } else {
              useMessage().createErrorNotification({
                message: '修改失败',
              });
            }
          })
          .finally(() => {
            this.getRoleList();
          });
      },
      addRole() {
        const data = {
          event: 'add',
          title: '添加角色',
        };
        this.openSaveModal(true, data);
      },
      editRole(record) {
        const data = {
          id: record.id,
          event: 'save',
          title: '编辑角色',
          roleId: record.id,
        };
        this.openSaveModal(true, data);
      },
      openGrantedModalFun(record) {
        record['assignResourceCategory'] = 'ROLE';
        this.openGrantedModal(true, record);
      },
    },
  });
</script>
<style scoped>
  .add-button {
    background: rgb(82, 196, 26);
    border-color: rgb(82, 196, 26);
    padding: 0 10px;
  }

  .add-button:hover {
    background: rgb(128, 196, 26);
    border-color: rgb(128, 196, 26);
    padding: 0 10px;
  }

  .ability-permission-button {
    background: #4bc0c0;
    border-color: #4bc0c0;
    margin: 0 10px;
  }

  .ability-permission-button:hover {
    background: #4bc08f;
    border-color: #4bc08f;
    margin: 0 10px;
  }

  .edit-button {
    background: #1890ff;
    border-color: #1890ff;
    margin: 0 10px;
  }

  .edit-button:hover {
    background: #18c9ff;
    border-color: #18c9ff;
    margin: 0 10px;
  }
</style>
