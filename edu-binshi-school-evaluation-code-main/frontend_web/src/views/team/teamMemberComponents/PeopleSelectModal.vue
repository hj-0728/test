<template>
  <div ref="selectPeopleRef" class="select-people-list">
    <BasicModal
      v-bind="$attrs"
      :canFullscreen="false"
      :draggable="false"
      :keyboard="false"
      :maskClosable="false"
      :loading="loading"
      @register="register"
      title="Modal Title"
      wrap-class-name="full-modal"
      width="80%"
      :showOkBtn="false"
      :showCancelBtn="false"
      :destroyOnClose="true"
      :getContainer="() => $refs.selectPeopleRef"
    >
      <template #title>
        <span class="inline-flex-center">
          <Icon icon="ion:settings-outline" :size="16" style="margin-right: 5px" /> 选择人员
        </span>
      </template>
      <div class="pt-3px pr-3px" style="height: calc(100vh - 140px)">
        <Row :gutter="[16, 0]" style="height: 100%">
          <Col :span="7" style="height: 100%">
            <div style="background-color: #fff; margin-top: -16px">
              <DeptTree
                @on-select-dept="onSelectDept"
                :dimension-category="dimensionCategory"
                :key="dimensionCategory"
              />
            </div>
          </Col>
          <Col :span="17">
            <div style="height: 100%; width: 100%; background-color: #fff">
              <PeopleTable
                :key="dimensionDeptTreeId + teamId + dimensionCategory"
                :teamId="teamId"
                :dimension-category="dimensionCategory"
                :dimension-dept-tree-id="dimensionDeptTreeId"
                @confirm-select-people="confirmSelectPeople"
                @save-team-member-error="saveTeamMemberError"
              />
            </div>
          </Col>
        </Row>
      </div>
    </BasicModal>
  </div>
</template>
<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Icon } from '/@/components/Icon';
  import DeptTree from '/@/views/team/teamMemberComponents/DeptTree.vue';
  import PeopleTable from '/src/views/team/teamMemberComponents/PeopleTable.vue';
  import { Col, Row } from 'ant-design-vue';

  export default defineComponent({
    components: {
      Row,
      Col,
      PeopleTable,
      DeptTree,
      BasicModal,
      Icon,
    },
    props: {
      isAdd: {
        type: Boolean,
      },
    },
    emits: ['register', 'updateTeamMemberList', 'saveMemberError'],
    setup() {
      const teamId = ref('');
      const dimensionDeptTreeId = ref('');
      const dimensionCategory = ref('');
      const [register, { closeModal }] = useModalInner((data) => {
        console.log(data);
        teamId.value = data.teamId;
        dimensionCategory.value = data.dimensionCategory;
        dimensionDeptTreeId.value = '';
        loading.value = false;
      });
      const loading = ref(true);
      return {
        register,
        loading,
        closeModal,
        dimensionDeptTreeId,
        teamId,
        dimensionCategory,
      };
    },
    methods: {
      onSelectDept(data) {
        const node = data.node;
        this.dimensionDeptTreeId = node.dimensionDeptTreeId;
      },
      confirmSelectPeople() {
        console.log('confirmSelectPeople');
        this.$emit('updateTeamMemberList');
        this.closeModal();
      },
      close() {
        this.closeModal();
      },
      saveTeamMemberError() {
        this.$emit('saveMemberError');
      },
    },
  });
</script>
<style scoped lang="less">
  .select-people-list {
    ::v-deep(.scroll-container .scrollbar__wrap) {
      margin-bottom: 0 !important;
    }

    ::v-deep(.ant-pagination-options) {
      .ant-select-dropdown {
        position: fixed;
      }
    }

    ::v-deep(.ant-modal) {
      height: 68vh;
    }
    // 控制只在modal内滚动，而不需要model的滚动，否则会出现两个滚动条
    // 注：严格按照下面的路径做才不会影响到DeptTree等子组件的滚动，所以轻易不要改动，除非你有充分的理由
    ::v-deep(.ant-modal-body > .scrollbar > .scrollbar__wrap > .scrollbar__view) {
      height: 66vh;
      overflow: hidden;
    }
  }
</style>
