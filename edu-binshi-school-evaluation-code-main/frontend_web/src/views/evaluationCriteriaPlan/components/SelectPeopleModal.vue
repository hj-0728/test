<template>
  <BasicModal
    @register="register"
    :canFullscreen="false"
    :defaultFullscreen="false"
    :draggable="false"
    :destroyOnClose="true"
    :closable="true"
    :centered="true"
    :maskClosable="false"
    wrap-class-name="full-modal"
    width="90vw"
    :showOkBtn="false"
    :showCancelBtn="false"
    @cancel="onCloseModal"
  >
    <template #title>
      <Icon icon="material-symbols:deployed-code-outline" />
      <span> 选择具体人员 </span>
    </template>
    <div
      class="md:flex p-3"
      style="height: calc(100vh - 300px); position: relative; overflow: hidden"
    >
      <div
        class="md:w-1/3 w-full"
        style="background: white; padding: 10px; margin-right: 10px; position: relative"
      >
        <DeptTree ref="deptTreeRef" @on-select-dept="onSelectDept" />
      </div>
      <div class="md:w-2/3 w-full" style="background: white">
        <PeopleTable
          :key="dimensionDeptTreeId"
          :dimension-dept-tree-id="dimensionDeptTreeId"
          @confirm-select="confirmSelectPeople"
        />
      </div>
    </div>
  </BasicModal>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import DeptTree from '/@/views/evaluationCriteriaPlan/components/DeptTree.vue';
  import PeopleTable from '/@/views/evaluationCriteriaPlan/components/PeopleTable.vue';
  import { Icon } from '/@/components/Icon';
  import { useStudentSelectStore } from '/src/store/modules/peopleSelect';

  export default defineComponent({
    components: {
      DeptTree,
      PeopleTable,
      BasicModal,
      Icon,
    },
    setup() {
      const dimensionDeptTreeId = ref();
      const selectPeopleId = ref([]);
      const pStore = useStudentSelectStore();

      const [register, { closeModal }] = useModalInner((data) => {
        pStore.initPeopleSelectStore(data.selectedPeopleIdList);
      });

      return {
        register,
        closeModal,
        dimensionDeptTreeId,
        pStore,
        selectPeopleId,
      };
    },
    methods: {
      confirmSelectPeople(data) {
        this.onCloseModal();
        this.$emit('confirmSelect', data);
      },
      onCloseModal() {
        this.pStore.$state.selectedRowKeys = [];
        this.dimensionDeptTreeId = '';
        this.closeModal();
      },
      onSelectDept(data) {
        const node = data.node;
        this.dimensionDeptTreeId = node.dimensionDeptTreeId;
      },
    },
  });
</script>

<style scoped></style>
