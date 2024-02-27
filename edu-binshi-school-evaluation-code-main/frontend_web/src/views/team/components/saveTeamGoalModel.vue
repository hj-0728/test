<template>
  <div class="select-goal-modal" ref="selectGoalModalRef">
    <BasicModal
      @register="registerTeamGoal"
      @cancel="onCloseModal"
      :canFullscreen="false"
      :defaultFullscreen="false"
      :draggable="false"
      :destroyOnClose="true"
      :closable="true"
      :centered="true"
      :maskClosable="false"
      :showCancelBtn="false"
      :showOkBtn="false"
      width="50vw"
      :getContainer="() => $refs.selectGoalModalRef"
    >
      <template #title>
        <div>
          <Icon icon="material-symbols:deployed-code-outline" />
          小组目标选择
        </div>
      </template>
      <template #footer>
        <Button @click="onCloseModal" preIcon="ic:twotone-close" style="top: -1px">关闭</Button>
        <Button
          :type="'primary'"
          color="edit"
          preIcon="ion:paper-airplane"
          :iconSize="16"
          @click="onClickSubmit"
        >
          确认
        </Button>
      </template>
      <div class="outer-goal">
        <GoalTree
          :key="teamId + teamCategoryId"
          ref="goalTreeRef"
          :checkAble="true"
          :checkedGoalKeys="checkedKeys"
          :teamId="teamId"
          :teamCategoryId="teamCategoryId"
          @on-check-goal="onCheckGoalOne"
        />
      </div>
    </BasicModal>
  </div>
</template>
<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Button } from '/@/components/Button';
  import { Icon } from '/@/components/Icon';
  import GoalTree from '/@/views/team/components/GoalTree.vue';
  import { cloneDeep } from 'lodash-es';
  export default defineComponent({
    components: { Icon, Button, BasicModal, GoalTree },
    props: {
      checkedGoalKeys: {
        type: Array,
        default: () => [],
      },
    },
    emit: ['selectGoal'],
    setup() {
      const teamId = ref<string>('');
      const teamCategoryId = ref<string>('');
      const [registerTeamGoal, { closeModal }] = useModalInner((data) => {
        checkedKeys.value = cloneDeep(data.checkedGoalKeys);
        teamId.value = data.teamId;
        teamCategoryId.value = data.teamCategoryId;
      });
      const checkedNodes = ref([]);
      const checkedKeys = ref([]);

      return {
        registerTeamGoal,
        closeModal,
        checkedNodes,
        checkedKeys,
        teamId,
        teamCategoryId,
      };
    },
    mounted() {
      this.checkedKeys = [];
    },
    methods: {
      onCheckGoalOne(checkedNodes) {
        this.checkedNodes = checkedNodes;
      },
      onCloseModal() {
        this.checkedNodes = [];
        this.checkedKeys = [];
        this.closeModal();
      },
      onClickSubmit() {
        let checkedNodes = this.checkedNodes.filter((item) => item.children.length === 0);
        this.$emit('selectGoal', checkedNodes);
        this.onCloseModal();
      },
    },
  });
</script>
<style scoped lang="less">
  .select-goal-modal {
    ::v-deep(.ant-modal) {
      width: 40vw !important;

      .goal-tree {
        .scrollbar__view {
          height: 60vh;
        }
      }
    }
  }
</style>
