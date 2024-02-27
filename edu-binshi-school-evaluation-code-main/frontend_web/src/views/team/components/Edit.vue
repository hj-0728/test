<template>
  <div class="edit-team-model" ref="editTeamModalRef">
    <BasicModal
      @register="register"
      :getContainer="() => $refs.editTeamModalRef"
      :destoryOnclose="true"
      width="60vw"
      :canFullscreen="false"
      :defaultFullscreen="false"
      :draggable="false"
      :destroyOnClose="true"
      :closable="true"
      :centered="true"
      :maskClosable="false"
      :showCancelBtn="false"
      :showOkBtn="false"
      @cancel="onCloseModal"
      wrap-class-name="full-modal"
    >
      <template #title>
        <div>
          <Icon icon="ant-design:edit-twotone" v-if="category === 'edit'" />
          <Icon icon="ant-design:plus-outlined" v-if="category === 'add'" />
          {{ category === 'add' ? '添加小组' : '编辑小组' }}
        </div>
      </template>
      <Loading :loading="fullScreenLoading" :absolute="true" />
      <div class="content">
        <Form
          :model="formState"
          autocomplete="off"
          name="form"
          ref="formRef"
          layout="horizontal"
          :rules="formRules"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          style="margin-top: 20px"
        >
          <FormItem name="name" label="名称：" :colon="false">
            <TextArea
              v-model:value="name"
              show-count
              :maxlength="255"
              :autoSize="{ minRows: 2, maxRows: 4 }"
            />
          </FormItem>
          <FormItem
            name="selectedGoalName"
            label="小组目标："
            :colon="false"
            :rules="[{ required: true, message: '请选择小组目标' }]"
          >
            <TextArea
              v-model:value="selectedGoalName"
              placeholder="请点击选择"
              readOnly
              @click="openTeamGoalFun"
            />
          </FormItem>
        </Form>
      </div>
      <template #footer>
        <Button @click="onCloseModal" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
        <Button
          :type="'primary'"
          color="edit"
          preIcon="ion:paper-airplane"
          :iconSize="16"
          @click="onClickSubmit"
        >
          提交
        </Button>
      </template>
      <SaveTeamGoalModel
        :key="teamCategoryId + teamId"
        :teamId="teamId"
        :teamCategoryId="teamCategoryId"
        ref="refTeamGoal"
        @register="registerTeamGoal"
        @select-goal="selectGoal"
      />
    </BasicModal>
  </div>
</template>
<script lang="ts">
  import { defineComponent, reactive, Ref, ref, toRefs } from 'vue';
  import BasicModal from '/@/components/Modal/src/BasicModal.vue';
  import { Icon } from '/@/components/Icon';
  import { Form, Input } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { useModal, useModalInner } from '/@/components/Modal';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import { apiGetTeamDetail, apiSaveTeam } from '/@/api/team/team';
  import { Loading } from '/@/components/Loading';
  import SaveTeamGoalModel from './saveTeamGoalModel.vue';

  export default defineComponent({
    components: {
      Loading,
      Button,
      Icon,
      BasicModal,
      Form,
      FormItem: Form.Item,
      TextArea: Input.TextArea,
      SaveTeamGoalModel,
    },
    setup() {
      const inputText = ref('');
      const goalCategory = ref();
      const teamCategoryId = ref('');
      const category = ref('add');
      const formRef = ref();
      const formRules = {
        name: [
          {
            required: true,
            trigger: ['blur', 'change'],
            message: '请输入名称',
            whitespace: true,
          },
        ],
      };
      const paramsList: Ref<object[]> = ref([]);
      const team = ref();
      const teamGoal = ref();
      const teamId = ref();
      const copyTeamId = ref();
      const copyTeamName = ref('');
      const copyTeamGoal = ref('');
      const goalId = ref();
      const teamGoalList: Ref<object[]> = ref([]);
      const goalIdList = ref<string[]>([]);
      const fullScreenLoading = ref(false);
      const [registerTeamGoal, { openModal: openTeamGoalSelectModal }] = useModal();
      const [register, { closeModal }] = useModalInner((data) => {
        category.value = data.category;
        teamCategoryId.value = data.teamCategoryId;
        if (data.category === 'edit') {
          teamId.value = data.teamId;
          getTeamDetail();
        } else {
          clearParams();
        }
      });
      const formState = reactive({
        name: '',
        version: 1,
        selectedGoalName: '',
      });
      const clearParams = () => {
        formState.name = '';
        formState.selectedGoalName = '';
        teamId.value = '';
      };
      const getTeamDetail = () => {
        apiGetTeamDetail(teamId.value)
          .then((res) => {
            if (res.code === 200) {
              formState.name = res.data.name;
              formState.version = res.data.version;
              formState.selectedGoalName = res.data.teamGoalList
                .map((obj) => obj.goalName)
                .join('；');
              goalIdList.value = res.data.teamGoalList.map((obj) => obj.goalId);
              teamGoalList.value = res.data.teamGoalList;
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
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
          });
      };
      return {
        teamGoalList,
        paramsList,
        teamId,
        goalIdList,
        copyTeamGoal,
        copyTeamName,
        teamGoal,
        copyTeamId,
        goalId,
        formRules,
        formRef,
        closeModal,
        register,
        clearParams,
        fullScreenLoading,
        team,
        formState,
        ...toRefs(formState),
        category,
        teamCategoryId,
        goalCategory,
        registerTeamGoal,
        openTeamGoalSelectModal,
        inputText,
      };
    },
    mounted() {
      this.goalIdList = [];
      this.paramsList = [];
    },
    methods: {
      selectGoal(goalList) {
        const teamGoalList: object[] = [];
        let selectedGoalNameList: string[] = [];
        let goalIdList: string[] = [];
        goalList.forEach((item) => {
          if (item.deptCategory === 'CLASS' && !item.disableCheckbox) {
            const goal = {
              goalId: item.key,
              goalCategory: 'DIMENSION_DEPT_TREE',
              activity: 'EVALUATION',
            };
            teamGoalList.push(goal);
            if (item.parentName) {
              selectedGoalNameList.push(`${item.parentName}/${item.name}`);
            } else {
              selectedGoalNameList.push(item.name);
            }
            goalIdList.push(item.key);
          }
        });
        this.teamGoalList = teamGoalList;
        this.formState.selectedGoalName = selectedGoalNameList.join('；');
        this.goalIdList = goalIdList;
      },
      onCloseModal() {
        this.goalIdList = [];
        this.formState.selectedGoalName = '';
        this.closeModal();
      },
      close() {
        this.$refs.refTeamGoal?.closeModal();
        this.closeModal();
      },
      onClickSubmit() {
        this.formRef.validate().then(() => {
          useMessage().createConfirm({
            iconType: 'info',
            title: '提示',
            content: '确定要提交吗？',
            onOk: () => {
              this.saveTeam();
            },
            onCancel: () => {},
          });
        });
      },
      saveTeam() {
        const team = {
          id: this.teamId,
          name: this.name,
          version: this.version,
          teamCategoryId: this.teamCategoryId,
          teamGoalList: this.teamGoalList,
        };
        this.fullScreenLoading = true;
        apiSaveTeam(team)
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '保存成功',
              });
              this.$emit('saveSuccess');
              this.clearParams();
              this.onCloseModal();
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
              description: ErrorNotificationEnum.networkExceptionMsg,
            });
          })
          .finally(() => {
            this.fullScreenLoading = false;
          });
        this.clearParams();
      },
      openTeamGoalFun() {
        console.log(this.goalIdList);
        if (this.category === 'edit') {
          this.openTeamGoalSelectModal(true, {
            category: this.category,
            checkedGoalKeys: this.goalIdList,
            teamId: this.teamId,
            teamCategoryId: this.teamCategoryId,
          });
        } else {
          this.openTeamGoalSelectModal(true, {
            category: this.category,
            checkedGoalKeys: this.goalIdList,
            teamId: '',
            teamCategoryId: this.teamCategoryId,
          });
        }
      },
    },
  });
</script>
