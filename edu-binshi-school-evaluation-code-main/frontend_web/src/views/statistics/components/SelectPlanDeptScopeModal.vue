<template>
  <div class="select-dept-modal" ref="selectDeptModalRef">
    <BasicModal
      @register="register"
      :canFullscreen="false"
      :defaultFullscreen="false"
      :draggable="false"
      :destroyOnClose="true"
      :closable="true"
      :centered="true"
      :maskClosable="false"
      :getContainer="() => $refs.selectDeptModalRef"
      width="50vw"
    >
      <template #title>
        <Icon icon="material-symbols:deployed-code-outline" />
        <span> 筛选部门 </span>
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
          提交
        </Button>
      </template>
      <plan-dept-scope-tree
        v-if="planId"
        ref="planDeptTreeRef"
        :checkAble="true"
        :checkedKeys="checkedKeys"
        :plan-id="planId"
        @on-check-dept="onCheckDept"
      />
    </BasicModal>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Icon } from '/@/components/Icon';
  import PlanDeptScopeTree from '/src/views/statistics/components/PlanDeptScopeTree.vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';

  export default defineComponent({
    components: { Button, Icon, BasicModal, PlanDeptScopeTree },
    setup() {
      const planId = ref('');
      const [register, { closeModal }] = useModalInner((data) => {
        checkedKeys.value = data.checkedDeptKeys;
        planId.value = data.planId;
        console.log(planId.value);
      });

      const checkedNodes = ref([]);
      const checkedKeys = ref([]);

      return {
        register,
        closeModal,
        checkedNodes,
        checkedKeys,
        planId,
      };
    },
    methods: {
      onCheckDept(checkedNodes) {
        this.checkedNodes = checkedNodes;
      },
      onCloseModal() {
        this.closeModal();
      },
      onClickSubmit() {
        console.log(this.checkedNodes);
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: '确定要提交吗？',
          onOk: () => {
            const checkedNodes = this.checkedNodes.filter((item) => item?.children.length === 0);
            this.$emit('onCheckDept', checkedNodes);
            this.onCloseModal();
          },
          onCancel() {},
        });
      },
    },
  });
</script>

<style scoped lang="less">
  .select-dept-modal {
    ::v-deep(.ant-modal) {
      width: 40vw !important;

      .dept-tree {
        .scrollbar__view {
          height: 60vh;
        }
      }
    }
  }
</style>
