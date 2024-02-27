<template>
  <div ref="modal" class="edit-user-modal">
    <BasicModal
      v-bind="$attrs"
      :canFullscreen="false"
      @register="register"
      wrap-class-name="full-modal"
      width="65%"
      :showOkBtn="false"
      :showCancelBtn="false"
      :destroyOnClose="true"
      :draggable="false"
      :keyboard="false"
      :maskClosable="false"
      :getContainer="() => $refs.modal"
      @cancel="onCancelModal"
    >
      <template #title>
        <div>
          <Icon icon="ant-design:plus-outlined" v-if="category === 'add'" />
          <Icon icon="ant-design:edit-twotone" v-if="category === 'edit'" />
          {{ category === 'add' ? '添加用户' : '修改角色' }}
        </div>
      </template>
      <template #footer>
        <Button @click="closeModal" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
        <Button
          type="primary"
          color="edit"
          :iconSize="16"
          preIcon="ion:paper-airplane"
          class="ant-btn-left-margin"
          title="保存"
          @click="saveUser"
          style="top: 1px"
        >
          保存
        </Button>
      </template>
      <Loading :loading="fullScreenLoading" />
      <Loading :loading="loading" :absolute="true" />
      <div class="content">
        <Form
          :model="inputValue"
          ref="formRef"
          name="basic"
          autocomplete="off"
          layout="horizontal"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          :rules="formRules"
        >
          <FormItem name="name" label="用户名">
            <span v-if="category === 'edit'">{{ inputValue.name }}</span>
            <Input
              v-if="category === 'add'"
              :maxlength="255"
              v-model:value="inputValue.name"
              @change="inputChange('name')"
            />
          </FormItem>
          <FormItem name="password" v-if="category === 'add'" label="密码">
            <InputPassword
              :maxlength="30"
              autocomplete="new-password"
              v-model:value="inputValue.password"
              @change="inputChange('password')"
              showCount
            />
          </FormItem>
          <FormItem name="verifyPassword" v-if="category === 'add'" label="确认密码">
            <InputPassword
              :maxlength="30"
              v-model:value="inputValue.verifyPassword"
              @change="inputChange('verifyPassword')"
              showCount
            />
          </FormItem>
          <!--        添加用户弹出框-->
          <div v-if="category === 'add'">
            <FormItem name="role" label="选择角色">
              <div>
                <Select
                  v-model:value="inputValue.roleIdList"
                  :fieldNames="{ label: 'name', value: 'id' }"
                  :filterOption="false"
                  :options="roleOptions"
                  mode="multiple"
                  show-search
                  @search="searchRole"
                  @focus="focusSelectRole"
                  :autoClearSearchValue="true"
                />
              </div>
            </FormItem>
            <People
              :state="category"
              @get-selected-people-id="getSelectedPeopleId"
              :selectedPeopleId="selectedPeopleId"
              :people-name="peopleName"
              @validate-people="validatePeople"
              :key="'addPeople' + refreshKey"
            />
          </div>
          <!--        编辑用户弹出框-->
          <div v-if="category === 'edit'">
            <FormItem name="role" label="选择角色">
              <div>
                <Select
                  v-model:value="inputValue.roleIdList"
                  :fieldNames="{ label: 'name', value: 'id' }"
                  :filterOption="false"
                  :options="roleOptions"
                  mode="multiple"
                  show-search
                  @search="searchRole"
                  @focus="focusSelectRole"
                  :autoClearSearchValue="true"
                  readonly
                />
              </div>
            </FormItem>
          </div>
        </Form>
      </div>
    </BasicModal>
  </div>
</template>

<script>
  import { defineComponent, reactive, ref } from 'vue';
  import { BasicModal, useModalInner } from '/src/components/Modal';
  import { Icon } from '/src/components/Icon';
  import { Button } from '/src/components/Button';
  import { Form, Input, Select } from 'ant-design-vue';
  import { apiGetTeacherRoleList } from '/src/api/role/role';
  import { useMessage } from '/src/hooks/web/useMessage';
  import { apiAddUser, apiEditUser } from '/src/api/user/user';
  import { useTabs } from '/src/hooks/web/useTabs';
  import { Loading } from '/src/components/Loading';
  import { PageEnum } from '/src/enums/pageEnum';
  import { clearAuthCache } from '/src/utils/auth';
  import { useUserStore } from '/src/store/modules/user';
  import People from './People.vue';

  export default defineComponent({
    components: {
      BasicModal,
      Icon,
      Button,
      Form,
      FormItem: Form.Item,
      Input,
      InputPassword: Input.Password,
      Select,
      Loading,
      People,
    },
    emits: ['register'],
    setup() {
      const roleOptions = ref([]);
      const loading = ref(false);
      const refreshKey = ref(new Date().getTime());
      const fullScreenLoading = ref(false);
      const icon = ref('ant-design:plus-outlined');
      const inputValue = reactive({
        name: '',
        password: '',
        verifyPassword: '',
        roleId: '',
        roleIdList: [],
        version: 1,
      });
      const inputCount = reactive({
        password: 0,
        verifyPassword: 0,
      });
      const formRef = ref();
      const category = ref('add');
      const selectedPeopleId = ref('');
      const peopleName = ref('');
      const { refreshPage } = useTabs();
      const [register, { closeModal }] = useModalInner((data) => {
        inputValue.name = '';
        inputValue.password = '';
        inputValue.verifyPassword = '';
        inputValue.roleIdList = [];
        selectedPeopleId.value = '';
        peopleName.value = '';
        category.value = data.category;
        refreshKey.value = new Date().getTime();
        roleOptions.value = [];
        getRoleList(data);
      });
      const initData = (data) => {
        if (data.category === 'edit') {
          editUserInfo.value = data.user;
          inputValue.name = data.user.name;
          inputValue.roleIdList = data.user.roleIdList;
          selectedPeopleId.value = data.user.peopleId;
          peopleName.value = data.user.peopleName;
        }
        refreshKey.value = new Date().getTime();
      };
      const validateName = async (rule, value) => {
        if (value === '' || value === undefined || value === null) {
          return Promise.reject('用户名不能为空');
        } else if (value?.trim() === '') {
          return Promise.reject('用户名不能为空');
        } else if (value.length > 255) {
          return Promise.reject('用户名最大长度不可超过255个字段，请重新输入');
        }
        return Promise.resolve();
      };

      const pwdRegex = new RegExp('(?=.*?\\d)(?=.*?[a-zA-Z])(?=.*?[^\\w\\s]|.*?[_]).{8,30}');
      const validatePassword = async (rule, value) => {
        if (value === '') {
          return Promise.reject('请输入密码');
        } else if (value.length < 8 || value.length > 30) {
          return Promise.reject('密码至少8个字符，最多不超过30个字符，请重新输入');
        } else if (/.*[\u4e00-\u9fa5]+.*$/.test(value)) {
          return Promise.reject('密码不能包含中文');
        } else if (!pwdRegex.test(value)) {
          return Promise.reject('您的密码复杂度太低，需包含数字、字母、特殊字符');
        } else {
          if (inputValue.verifyPassword !== '') {
            formRef.value.validateFields('verifyPassword');
          }
          return Promise.resolve();
        }
      };
      const validateVerifyPassword = async (rule, value) => {
        if (value === '') {
          return Promise.reject('请确认您的密码');
        } else if (value !== inputValue.password) {
          return Promise.reject('俩次输入密码不一致，重新输入');
        } else {
          return Promise.resolve();
        }
      };
      const validateRole = async () => {
        if (inputValue.roleIdList.length <= 0) {
          return Promise.reject('请确认选择角色');
        } else {
          return Promise.resolve();
        }
      };
      const validatePeople = async () => {
        if (!selectedPeopleId.value || selectedPeopleId.value?.trim() === '') {
          return Promise.reject('请确认选择人员');
        } else {
          return Promise.resolve();
        }
      };
      const formRules = {
        name: [{ required: true, validator: validateName, trigger: 'blur' }],
        password: [{ required: true, validator: validatePassword, trigger: 'blur' }],
        verifyPassword: [{ required: true, validator: validateVerifyPassword, trigger: 'blur' }],
        role: [{ required: true, validator: validateRole, trigger: ['blur', 'change'] }],
        people: [{ required: true, validator: validatePeople, trigger: ['blur', 'change'] }],
      };
      const roleList = ref([]);
      const roleListId = ref([]);
      const editUserInfo = ref({});
      const userRoleId = ref('');
      const userStore = useUserStore();
      const getRoleList = (data) => {
        loading.value = true;
        apiGetTeacherRoleList()
          .then((res) => {
            if (res.code === 200) {
              roleList.value = [];
              roleList.value = res.data;
              roleOptions.value = res.data;
              if (userStore.getUserInfo.currentRole.code !== 'SYSTEM_ADMIN') {
                if (category.value === 'add') {
                  roleList.value = res.data.filter((o) => o.code !== 'SYSTEM_ADMIN');
                } else {
                  roleList.value.forEach((item) => {
                    if (item.code === 'SYSTEM_ADMIN') {
                      item.disabled = true;
                    }
                  });
                }
              }
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
            initData(data);
            loading.value = false;
          });
      };
      return {
        icon,
        inputValue,
        inputCount,
        formRef,
        formRules,
        roleOptions,
        getRoleList,
        roleList,
        roleListId,
        editUserInfo,
        refreshPage,
        register,
        closeModal,
        userRoleId,
        category,
        fullScreenLoading,
        refreshKey,
        loading,
        validateName,
        selectedPeopleId,
        peopleName,
        validatePeople,
      };
    },
    methods: {
      searchRole(searchValue) {
        const newRoleOptions = [];
        const originalRoleIdList = [];
        this.roleList.forEach((item) => {
          originalRoleIdList.push(item['id']);
          if (item['name'].indexOf(searchValue) >= 0) {
            newRoleOptions.push(item);
          }
        });
        this.inputValue.roleIdList.forEach((item) => {
          if (originalRoleIdList.indexOf(item) < 0) {
            newRoleOptions.unshift({
              id: item,
              name: item,
            });
          }
        });
        this.roleOptions = newRoleOptions;
      },
      focusSelectRole() {
        this.searchRole('');
      },
      display() {
        console.log('当前的this是:' + this);
      },
      inputChange(input) {
        this.inputCount[input] = this.inputValue[input].length;
      },
      onCancelModal() {
        this.inputValue.name = '';
        this.inputValue.password = '';
        this.inputValue.verifyPassword = '';
        this.inputValue.roleId = this.roleList[0].id;
        this.inputValue.version = 1;
        this.roleList = [];
        this.selectedPeopleId = '';
      },
      saveUser() {
        this.fullScreenLoading = true;
        this.formRef
          .validateFields()
          .then(() => {
            this.onSaveUser();
          })
          .catch(() => {
            this.fullScreenLoading = false;
          });
      },
      saveUserRole() {
        this.fullScreenLoading = true;
        this.formRef
          .validateFields('role')
          .then(() => {
            this.onSaveUser();
          })
          .catch(() => {
            this.fullScreenLoading = false;
          });
      },
      onSaveUser() {
        let params = {
          name: this.inputValue.name.trim(),
          password: this.inputValue.password.trim(),
          verifyPassword: this.inputValue.verifyPassword.trim(),
          roleIdList: this.inputValue.roleIdList,
          version: this.inputValue.version,
          peopleId: this.selectedPeopleId,
        };
        // @ts-ignore
        if (this.editUserInfo.id && this.category === 'edit') {
          params.id = this.editUserInfo.id;
          params.version = this.editUserInfo.version;
        }
        const api = this.category === 'edit' ? apiEditUser : apiAddUser;
        api(params)
          .then((res) => {
            if (res.code === 200) {
              const message = res.data && res.data.logout ? '修改成功，请重新登录' : '保存成功';
              useMessage().createSuccessNotification({
                message: message,
              });
              setTimeout(() => {
                if (res.data && res.data.logout) {
                  clearAuthCache();
                  this.$router.push(PageEnum.BASE_LOGIN);
                } else {
                  this.refreshPage();
                  this.fullScreenLoading = false;
                }
              }, 1000);
            } else {
              useMessage().createErrorNotification({
                message: '保存失败',
                description: res.error.message,
              });
              this.fullScreenLoading = false;
            }
          })
          .catch(() => {
            useMessage().createErrorNotification({
              message: '保存失败',
              description: '网络错误',
            });
            this.fullScreenLoading = false;
          });
      },
      getSelectedPeopleId(data) {
        console.log('选择了', data);
        // console.log('category是:' + this.category);
        this.selectedPeopleId = data;
      },
    },
  });
</script>

<style scoped lang="less">
  .edit-user-modal {
    .form-mark {
      color: red;
      margin: 0 4px 0 4px;
      top: 3px;
      position: relative;
    }

    ::v-deep(.scrollbar__view) {
      //height: calc(100% - 50px);
      height: 60vh;
      overflow: hidden;
    }

    ::v-deep(.ant-modal-body) {
      height: 100%;
      //background-color: #f0f2f5;
      .scrollbar {
        padding: 0 !important;
        overflow: hidden;
      }
    }

    .content {
      //height: 100%;
      height: 60vh;
      //background-color: #00acc1;
      overflow-y: auto;
      padding: 16px;
    }
  }
</style>
