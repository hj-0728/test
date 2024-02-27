<template>
  <div ref="planScopeModalRef">
    <BasicModal
      @register="register"
      @cancel="onCloseModal"
      :canFullscreen="false"
      :defaultFullscreen="false"
      :draggable="false"
      :destroyOnClose="true"
      :closable="true"
      :centered="true"
      :maskClosable="false"
      :loading="loading"
      wrap-class-name="full-modal"
      :getContainer="() => $refs.planScopeModalRef"
      width="50vw"
    >
      <template #title>
        <Icon icon="material-symbols:deployed-code-outline" />
        <span> 评价计划适用范围 </span>
      </template>
      <SelectScopeFrom
        ref="selectScopeFromRef"
        v-if="formState.planId"
        :plan-id="formState.planId"
        :disabled="disabled"
        :required="required"
        @save-success="onCloseModal"
      />
      <template #footer>
        <Button v-if="!disabled" @click="onCloseModal" preIcon="ic:twotone-close">关闭</Button>
        <Button
          :type="'primary'"
          color="edit"
          preIcon="ion:paper-airplane"
          :iconSize="16"
          v-if="!disabled"
          @click="onClickSubmit"
        >
          提交
        </Button>
      </template>
    </BasicModal>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref } from 'vue';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Icon } from '/@/components/Icon';
  import { Button } from '/@/components/Button';
  import { useStudentSelectStore } from '/src/store/modules/peopleSelect';
  import SelectScopeFrom from '/src/views/evaluationCriteriaPlan/components/SelectScopeForm.vue';

  export default defineComponent({
    components: {
      SelectScopeFrom,
      Button,
      BasicModal,
      Icon,
    },
    emits: ['register', 'saveSuccess'],
    setup(_props, { emit }) {
      const loading = ref(false);
      const pStore = useStudentSelectStore();
      const disabled = ref(false);
      const required = ref(true);
      const [register, { closeModal }] = useModalInner((data) => {
        formState.planId = data.plan_id;
        disabled.value = data.disabled;
        required.value = data.required;
      });

      const formState = reactive<{
        planId: null | string;
        scopeCategory: string[];
        dept: null | string[];
        people: null | string[];
      }>({
        planId: null,
        scopeCategory: [],
        dept: null,
        people: null,
      });

      const onCloseModal = () => {
        closeModal();
        selectScopeFromRef.value.formState.scopeCategory = [];
        selectScopeFromRef.value.selectPeopleList = '';
        selectScopeFromRef.value.selectDeptList = '';
        selectScopeFromRef.value.showSelectPeople = false;
        selectScopeFromRef.value.showSelectDept = false;
        selectScopeFromRef.value.formState.deptIdList = [];
        selectScopeFromRef.value.formState.peopleIdList = [];
        selectScopeFromRef.value.formState.planId = '';
        formState.planId = '';
        emit('saveSuccess');
        pStore.initPeopleSelectStore([]);
      };

      const selectScopeFromRef = ref();

      const onClickSubmit = () => {
        selectScopeFromRef.value.onClickSubmit();
      };

      return {
        register,
        closeModal,
        formState,
        onCloseModal,
        onClickSubmit,
        loading,
        selectScopeFromRef,
        disabled,
        required
      };
    },
  });
</script>
