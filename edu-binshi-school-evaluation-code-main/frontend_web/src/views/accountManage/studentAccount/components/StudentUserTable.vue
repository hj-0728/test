<template>
  <div>
    <BasicTable
      :dataSource="tableData"
      :canResize="true"
      :loading="loading"
      :scroll="{ y: tableHeight }"
      :showIndexColumn="false"
      @register="registerTable"
      @change="onChange"
      :pagination="{ total: total, pageSize: pageSize, current: pageIndex + 1 }"
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
          preIcon="ant-design:align-left-outlined"
          class="ant-btn-left-margin"
          title="批量创建账号"
          @click="batchCreateStudentUser()"
          >批量创建账号
        </Button>
        <Button
          type="primary"
          color="purple"
          :iconSize="18"
          preIcon="ph:download-simple"
          class="ant-btn-left-margin"
          title="导出学生账号"
          @click="exportStudentUser()"
          >导出学生账号
        </Button>
      </template>
      <template #bodyCell="{ column, record }">
        <template v-if="column.dataIndex === 'dept'">
          <span>{{ record.schoolClass }}</span>
        </template>
        <template v-if="column.dataIndex === 'userName'">
          <span>{{ record.user?.name }}</span>
        </template>
        <template v-if="column.dataIndex === 'isInitPassword'">
          <span v-if="record.user">{{ record.user.passwordReset ? '是' : '否' }}</span>
        </template>
        <template v-if="column.dataIndex === 'isActivated'">
          <Switch
            v-if="record.user"
            v-model:checked="record.user.isActivated"
            checked-children="启用"
            un-checked-children="禁用"
            @change="onChangeUserActivated(record)"
            v-model:disabled="switchDisabled"
          />
        </template>
        <template v-if="column.dataIndex === 'operation'">
          <Button
            v-if="record.user"
            type="primary"
            :iconSize="16"
            preIcon="mdi:lock-reset"
            class="reset-password-button-style"
            @click="resetPassword(record)"
          >
            重置密码
          </Button>
          <Button
            v-else
            type="primary"
            color="edit"
            :iconSize="16"
            preIcon="ant-design:plus-outlined"
            @click="createStudentUser(record)"
          >
            创建账号
          </Button>
        </template>
      </template>
    </BasicTable>
  </div>
</template>

<script lang="ts">
  import { createVNode, defineComponent, reactive, ref, toRefs } from 'vue';
  import { BasicTable, useTable } from '/@/components/Table';
  import { getBasicColumns } from '/@/views/accountManage/studentAccount/components/studentUserTableData';
  import { Input, Switch } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { getTableHeight } from '/@/utils/helper/tableHelper';
  import { UserInfo } from '/#/store';
  import { useModal } from '/@/components/Modal';
  import {
    apiStudentUserPage,
    apiCreateStudentUser,
    apiExportStudentUser,
    apiBatchCreateStudentUser,
  } from '/@/api/student/student';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { getAuthCache } from '/@/utils/auth';
  import { USER_INFO_KEY } from '/@/enums/cacheEnum';
  import { changeUserActivated, resetUserPassword } from '/@/views/accountManage/userFunc';
  import { ExclamationCircleOutlined } from '@ant-design/icons-vue';
  import { cloneDeep } from 'lodash-es';

  export default defineComponent({
    components: {
      Switch,
      BasicTable,
      InputSearch: Input.Search,
      Button,
    },
    props: {
      dimensionDeptTreeId: {
        type: String,
        default: '',
      },
      deptName: {
        type: String,
        default: '',
      },
    },
    setup(props) {
      const currentUserInfo: UserInfo = getAuthCache(USER_INFO_KEY);
      const currentRoleCode = currentUserInfo.currentRole?.code;

      const [register, { openModal }] = useModal();
      const total = ref(0);
      const tableHeight = ref(getTableHeight(document));
      const loading = ref(false);
      const switchDisabled = ref(false);
      const tableData = ref([]);
      const params = reactive({
        pageSize: 20,
        pageIndex: 0,
        searchText: '',
        draw: 1,
        getDutyTeacherDept: currentRoleCode === 'TEACHER',
        dimensionDeptTreeId: props.dimensionDeptTreeId,
      });
      const columns = ref();
      columns.value = getBasicColumns();
      const [registerTable, { setPagination, setLoading }] = useTable({
        columns: columns.value,
        bordered: true,
      });
      const getStudentUserPage = () => {
        loading.value = true;
        apiStudentUserPage(params)
          .then((res) => {
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
      getStudentUserPage();
      return {
        loading,
        registerTable,
        ...toRefs(params),
        params,
        tableData,
        tableHeight,
        total,
        currentRoleCode,
        getStudentUserPage,
        register,
        openModal,
        setPagination,
        setLoading,
        switchDisabled,
      };
    },
    methods: {
      onSearch() {
        this.pageIndex = 0;
        this.getStudentUserPage();
      },
      onChange(pageInfo, _filters) {
        this.pageSize = pageInfo.pageSize;
        this.pageIndex = pageInfo.current - 1;
        this.getStudentUserPage();
      },
      init() {
        this.pageSize = 20;
        this.pageIndex = 0;
        this.searchText = '';
        this.draw = 1;
      },
      resetPassword(student) {
        console.log('reset password');
        console.log(student);
        let user = cloneDeep(student.user);
        user['userType'] = 'STUDENT';
        resetUserPassword(user, this);
      },
      createStudentUser(student) {
        console.log('created student user');
        console.log(student);
        useMessage().createConfirm({
          iconType: 'info',
          title: () => '您确定为该学生创建账号吗？',
          centered: true,
          icon: () => createVNode(ExclamationCircleOutlined),
          onOk: () => {
            this.setLoading(true);
            apiCreateStudentUser(student)
              .then((res) => {
                if (res.code === 200) {
                  useMessage().createSuccessNotification({
                    message: '创建成功',
                  });
                  this.getStudentUserPage();
                } else {
                  useMessage().createErrorNotification({
                    message: '操作失败',
                    description: res.error.message,
                  });
                  this.setLoading(false);
                }
              })
              .catch(() => {
                useMessage().createErrorNotification({
                  message: '保存失败',
                  description: '网络错误',
                });
                this.setLoading(false);
              });
          },
        });
      },
      exportStudentUser() {
        console.log('export student user');
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: '确定要导出学生账号吗？',
          onOk: () => {
            this.setLoading(true);
            apiExportStudentUser(this.params)
              .then((res) => {
                console.log(res);
                if (res.code === 200) {
                  console.log(res);
                  let anchor = document.createElement('a');
                  anchor.href = res.data.url;
                  anchor.download = res.data.originalName;
                  anchor.click();
                  anchor.remove();
                  useMessage().createSuccessNotification({
                    message: '生成成功',
                    description: `${res.data.originalName} 导出完成！`,
                  });
                } else {
                  useMessage().createErrorNotification({
                    message: '错误提示',
                    description: res.messages.join(';'),
                  });
                }
              })
              .catch(() => {
                useMessage().createErrorModal({
                  title: '提示',
                  content: '网络异常，请检查您的网络连接是否正常!',
                  closable: true,
                  maskClosable: false,
                });
              })
              .finally(() => {
                this.setLoading(false);
              });
          },
          onCancel() {
            console.log('Cancel');
          },
        });
      },
      getUserList() {
        this.getStudentUserPage();
      },
      onChangeUserActivated(student) {
        changeUserActivated(student.user, this);
      },
      batchCreateStudentUser() {
        console.log('batch create student user');
        console.log(this.params);
        let deptNameContent = '【全校】';
        let searchTextContent = '';
        if (this.deptName) {
          deptNameContent = `【${this.deptName}】`;
        }
        if (this.searchText) {
          searchTextContent = `检索条件为：【${this.searchText}】的`;
        }
        let content = `您确定要为${searchTextContent}${deptNameContent}学生创建账号吗？`;
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: content,
          onOk: () => {
            this.setLoading(true);
            apiBatchCreateStudentUser(this.params)
              .then((res) => {
                if (res.code === 200) {
                  useMessage().createSuccessNotification({
                    message: '创建成功',
                  });
                  this.getStudentUserPage();
                } else {
                  useMessage().createErrorNotification({
                    message: '操作失败',
                    description: res.error.message,
                  });
                  this.setLoading(false);
                }
              })
              .catch(() => {
                useMessage().createErrorNotification({
                  message: '保存失败',
                  description: '网络错误',
                });
                this.setLoading(false);
              });
          },
          onCancel() {
            console.log('Cancel');
          },
        });
      },
    },
  });
</script>

<style scoped lang="less">
  ::v-deep(.vben-basic-table-header__toolbar) {
    margin-right: 0;
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
