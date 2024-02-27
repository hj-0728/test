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
          <Icon icon="ant-design:eye-outlined" />
          查看小组
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
            <span>{{ name }}</span>
          </FormItem>
          <FormItem
            name="selectedGoalName"
            label="小组目标："
            :colon="false"
            :rules="[{ required: true, message: '请选择小组目标' }]"
          >
            <span v-if="selectedGoalName">{{ selectedGoalName }}</span>
            <span v-else>暂无小组目标</span>
          </FormItem>
          <FormItem
            name="memberName"
            label="小组成员："
            :colon="false"
            :rules="[{ required: true, message: '请选择小组目标' }]"
          >
            <span v-if="memberName">{{ memberName }}</span>
            <span v-else>暂无小组成员</span>
          </FormItem>
        </Form>
      </div>
      <template #footer>
        <Button @click="onCloseModal" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
      </template>
    </BasicModal>
  </div>
</template>
<script lang="ts">
  import { defineComponent, reactive, Ref, ref, toRefs } from 'vue';
  import BasicModal from '/@/components/Modal/src/BasicModal.vue';
  import { Icon } from '/@/components/Icon';
  import { Form } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { useModalInner } from '/@/components/Modal';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import { apiGetTeamDetail } from '/@/api/team/team';
  import { Loading } from '/@/components/Loading';

  export default defineComponent({
    components: {
      Loading,
      Button,
      Icon,
      BasicModal,
      Form,
      FormItem: Form.Item,
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
      const goalId = ref();
      const teamGoalList: Ref<object[]> = ref([]);
      const goalIdList = ref<string[]>([]);
      const fullScreenLoading = ref(false);
      const [register, { closeModal }] = useModalInner((data) => {
        teamId.value = data.teamId;
        getTeamDetail();
      });
      const formState = reactive({
        name: '',
        selectedGoalName: '',
        memberName: '',
      });
      const clearParams = () => {
        formState.name = '';
        formState.selectedGoalName = '';
        teamId.value = '';
        formState.memberName = '';
      };
      const getTeamDetail = () => {
        apiGetTeamDetail(teamId.value)
          .then((res) => {
            if (res.code === 200) {
              formState.name = res.data.name;
              formState.selectedGoalName = res.data.teamGoalList
                .map((obj) => obj.goalName)
                .join('；');
              formState.memberName = res.data.memberList.join('；');
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
        teamGoal,
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
        inputText,
      };
    },
    methods: {
      onCloseModal() {
        this.clearParams();
        this.closeModal();
      },
    },
  });
</script>
