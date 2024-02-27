<template>
  <div ref="modal">
    <BasicModal
      v-bind="$attrs"
      :canFullscreen="false"
      @register="register"
      width="60%"
      :showOkBtn="false"
      :showCancelBtn="false"
      :destroyOnClose="true"
      :closeFunc="closeModalFunc"
      :getContainer="() => $refs.modal"
    >
      <template #title>
        <Icon icon="ant-design:edit-twotone" :size="16" style="margin-right: 5px" /> 编辑路径
      </template>
      <template #footer>
        <div style="padding: 10px 0">
          <Button
            type="primary"
            color="blue"
            :iconSize="16"
            preIcon="ion:paper-airplane"
            class="ant-btn-left-margin"
            title="保存"
            @click="saveRoute"
            style="top: 1px"
          >
            提交
          </Button>
        </div>
      </template>
      <Form
        :model="inputValue"
        ref="formRef"
        name="basic"
        autocomplete="off"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 14 }"
        layout="horizontal"
        :rules="formRules"
      >
        <FormItem label="路径" name="path">
          <span>{{ inputValue.path }}</span>
        </FormItem>
        <FormItem label="编码" name="entryCode">
          <Input v-model:value="inputValue.entryCode" placeholder="请输入编码" />
        </FormItem>
        <FormItem label="身份验证" name="accessStrategy">
          <Select v-model:value="inputValue.accessStrategy" ref="select">
            <SelectOption
              v-for="[id, item] of accessStrategyList.entries()"
              :value="item.name"
              :key="'select' + id"
            >
              {{ item.value }}
            </SelectOption>
          </Select>
        </FormItem>
        <FormItem label="角色名称" name="roleId" v-if="inputValue.accessStrategy === 'CONTROLLED'">
          <Select
            mode="multiple"
            placeholder="请选择角色名称"
            ref="select"
            v-model:value="inputValue.roleId"
          >
            <SelectOption
              v-for="[id, item] of roleList.entries()"
              :value="item.value"
              :key="'select' + id"
            >
              {{ item.name }}
            </SelectOption>
          </Select>
        </FormItem>
        <FormItem
          label="功能权限"
          name="abilityPermission"
          v-if="inputValue.accessStrategy === 'CONTROLLED'"
        >
          <Button
            type="primary"
            color="orange"
            :iconSize="16"
            preIcon="ion:settings-outline"
            class="ant-btn-left-margin"
            title="功能权限"
            @click="functionPermission"
          >
            功能权限
          </Button>
        </FormItem>
      </Form>
      <AbilityPermissionAssign @register="registerGranted" @save-granted="saveGranted" />
    </BasicModal>
  </div>
</template>

<script>
  import { createVNode, defineComponent, reactive, ref } from 'vue';
  import { BasicModal, useModal, useModalInner } from '/@/components/Modal';
  import { Button } from '/@/components/Button';
  import { Form, Select, Input, Modal } from 'ant-design-vue';
  import { apiEditPath, apiGetRouteAccessStrategy } from '/@/api/route/route';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { useTabs } from '/@/hooks/web/useTabs';
  import { apiGetRolePageList } from '/@/api/role/role';
  import { Icon } from '/@/components/Icon';
  import AbilityPermissionAssign from '/@/components/AbilityPermissionAssign/index.vue';
  import { ExclamationCircleOutlined } from '@ant-design/icons-vue';

  export default defineComponent({
    components: {
      BasicModal,
      Button,
      Form,
      FormItem: Form.Item,
      Select,
      Input,
      Icon,
      SelectOption: Select.Option,
      AbilityPermissionAssign,
    },
    emits: ['register'],
    setup() {
      const { refreshPage } = useTabs();
      const inputValue = reactive({
        path: '',
        entryCode: '',
        accessStrategy: '',
        version: 1,
        roleId: [],
      });
      const accessStrategyList = ref([]);
      const getRouteCategoryList = () => {
        apiGetRouteAccessStrategy().then((res) => {
          accessStrategyList.value = res.data;
        });
      };
      getRouteCategoryList();
      const roleList = reactive([]);
      const getRoleNameList = () => {
        apiGetRolePageList().then((res) => {
          roleList.splice(0);
          res.data.data.forEach((role) => {
            roleList.push({
              name: role.name,
              value: role.id,
            });
          });
        });
      };
      getRoleNameList();
      const [register, { closeModal }] = useModalInner((data) => {
        editRouteInfo.value = data;
        inputValue.path = data.path;
        inputValue.entryCode = data.entryCode;
        inputValue.accessStrategy = data.accessStrategy;
        inputValue.roleId = [];
        routeId.value = data.id;
        roleList.forEach((role) => {
          if (data.roleNameList && data.roleNameList.includes(role.name)) {
            inputValue.roleId.push(role.value);
          }
        });
      });
      let editRouteInfo = ref({});
      const routeId = ref('');
      const [registerGranted, { openModal: openGrantedModal }] = useModal();
      const permittedResourceCategory = ref('');
      const permittedResourceIds = ref([]);

      const formRef = ref();
      const formRules = {
        accessStrategy: [{ required: true, message: '请选择身份验证方式' }],
        roleId: [{ required: true, message: '请选择角色' }],
      };

      return {
        inputValue,
        accessStrategyList,
        register,
        closeModal,
        editRouteInfo,
        refreshPage,
        getRoleNameList,
        roleList,
        getRouteCategoryList,
        registerGranted,
        openGrantedModal,
        permittedResourceIds,
        permittedResourceCategory,
        routeId,
        formRef,
        formRules,
      };
    },
    methods: {
      saveRoute() {
        this.formRef.validateFields().then(() => {
          this.onSaveRoute();
        });
      },
      onSaveRoute() {
        Modal.confirm({
          title: () => '确定要提交吗？',
          centered: true,
          icon: () => createVNode(ExclamationCircleOutlined),
          onOk: () => {
            if (this.inputValue.accessStrategy !== 'CONTROLLED') {
              this.inputValue.roleId = [];
              this.permittedResourceIds = [];
            }
            let params = {
              path: this.inputValue.path.trim(),
              entryCode: this.inputValue.entryCode?.trim(),
              accessStrategy: this.inputValue.accessStrategy,
              version: this.inputValue.version,
              role_id_list: this.inputValue.roleId,
              permitList: [
                {
                  permittedResourceCategory: this.permittedResourceCategory,
                  permittedResourceIds: this.permittedResourceIds,
                },
              ],
            };
            if (this.editRouteInfo.id) {
              params.id = this.editRouteInfo.id;
              params.version = this.editRouteInfo.version;
              params.accessStrategy = this.inputValue.accessStrategy;
            }
            apiEditPath(params)
              .then((res) => {
                if (res.code === 200) {
                  useMessage().createSuccessNotification({
                    message: '保存成功',
                    description: res.messages.join('\n'),
                  });
                  setTimeout(() => {
                    this.refreshPage();
                  }, 1000);
                } else {
                  useMessage().createErrorNotification({
                    message: '保存失败',
                    description: res.error.message,
                  });
                }
              })
              .catch(() => {
                useMessage().createErrorNotification({
                  message: '错误',
                  description: '网络异常',
                });
              });
          },
        });
      },
      functionPermission() {
        this.openGrantedModal(true, { category: 'route', routeId: this.routeId });
        this.openGrantedModal(true, {
          category: 'route',
          routeId: this.routeId,
          permittedResourceIds: this.permittedResourceIds,
        });
      },
      saveGranted(data) {
        this.permittedResourceCategory = data.permittedResourceCategory;
        this.permittedResourceIds = data.permittedResourceIds;
      },
      closeModalFunc() {
        this.permittedResourceIds = [];
        this.permittedResourceCategory = '';
        return true;
      },
    },
  });
</script>
