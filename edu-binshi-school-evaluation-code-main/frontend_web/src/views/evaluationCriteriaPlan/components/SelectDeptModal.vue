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
        <span> 选择具体部门 </span>
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
      <DeptTree
        ref="deptTreeRef"
        :checkAble="true"
        :checkedKeys="checkedKeys"
        @on-check-dept="onCheckDept"
      />
    </BasicModal>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Icon } from '/@/components/Icon';
  import DeptTree from '/@/views/evaluationCriteriaPlan/components/DeptTree.vue';
  import { Button } from '/@/components/Button';

  export default defineComponent({
    components: { Button, Icon, BasicModal, DeptTree },
    setup() {
      const [register, { closeModal }] = useModalInner((data) => {
        checkedKeys.value = data.checkedDeptKeys;
      });

      const checkedNodes = ref([]);
      const checkedKeys = ref([]);

      return {
        register,
        closeModal,
        checkedNodes,
        checkedKeys,
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
        // 有确认框保证了准确性,但是也增加了操作路径,用户要多点一次确认框,但是对编辑范围的model来说有自己的确认框,这里适当放开是可以的
        const checkedNodes = this.checkedNodes.filter((item) => item.children.length === 0);
        this.$emit('onCheckDept', checkedNodes);
        this.onCloseModal();
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
