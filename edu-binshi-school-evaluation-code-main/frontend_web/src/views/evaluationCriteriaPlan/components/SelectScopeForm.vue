<template>
  <div>
    <Form
      :model="formState"
      name="basic"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 14 }"
      autocomplete="off"
      ref="formRef"
    >
      <FormItem
        label="部门"
        name="deptIdList"
        :rules="[{ required: false, message: '请选择部门' }]"
      >
        <span v-if="disabled">
          <span v-if="selectDeptList">{{ selectDeptList }}</span>
          <span v-else>未选择部门</span>
        </span>
        <TextArea
          v-else
          v-model:value="selectDeptList"
          placeholder="请点击选择部门"
          readOnly
          :disabled="disabled"
          @click="toSelectDeptModal"
        />
      </FormItem>
      <FormItem
        label="人员"
        name="peopleIdList"
        :rules="[{ required: false, message: '请选择人员' }]"
      >
        <span v-if="disabled">
          <span v-if="selectPeopleList">{{ selectPeopleList }}</span>
          <span v-else>未选择人员</span>
        </span>
        <TextArea
          v-else
          v-model:value="selectPeopleList"
          placeholder="请点击选择人员"
          readOnly
          :disabled="disabled"
          @click="toSelectPeopleModal"
        />
      </FormItem>
    </Form>
    <SelectPeopleModal
      @register="registerSelectPeopleModal"
      @confirm-select="confirmSelectPeople"
    />
    <SelectDeptModal @register="registerSelectDeptModal" @on-check-dept="onCheckDept" />
    <Loading :loading="loading" />
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref } from 'vue';
  import { Form, Input, SelectProps } from 'ant-design-vue';
  import SelectPeopleModal from '/@/views/evaluationCriteriaPlan/components/SelectPeopleModal.vue';
  import SelectDeptModal from '/@/views/evaluationCriteriaPlan/components/SelectDeptModal.vue';
  import { useModal } from '/@/components/Modal';
  import { apiGetPlanScopeByPlanId } from '/@/api/evaluationCriteriaPlanScope/evaluationCriteriaPlanScope';
  import { useStudentSelectStore } from '/src/store/modules/peopleSelect';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { apiSaveEvaluationCriteriaPlanAndScope } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlan';
  import { Loading } from '/@/components/Loading';

  export default defineComponent({
    components: {
      Loading,
      Form,
      FormItem: Form.Item,
      TextArea: Input.TextArea,
      SelectPeopleModal,
      SelectDeptModal,
    },
    props: {
      planId: {
        type: String,
        default: null,
      },
      disabled: {
        type: Boolean,
        default: false,
      },
      required: {
        type: Boolean,
        default: true,
      },
    },
    emits: ['saveSuccess'],
    setup(props, { emit }) {
      const loading = ref(false);
      const pStore = useStudentSelectStore();
      const formState = reactive<{
        evaluationCriteriaPlanId: null | string;
        scopeCategory: string[];
        deptIdList: null | string[];
        peopleIdList: null | string[];
      }>({
        evaluationCriteriaPlanId: props.planId,
        scopeCategory: [],
        deptIdList: null,
        peopleIdList: null,
      });
      const getPlanScope = () => {
        apiGetPlanScopeByPlanId(formState.evaluationCriteriaPlanId)
          .then((res) => {
            if (res.data) {
              res.data.forEach((item) => {
                if (item.scopeCategory === 'PERSONAL') {
                  selectPeopleList.value = item.scopeInfo
                    .map((people) =>
                      people.isDeleted ? people.name + '（已从钉钉移除）' : people.name,
                    )
                    .join('；');
                  formState.scopeCategory.push(item.scopeCategory);
                  formState.peopleIdList = [];
                  item.scopeInfo.forEach((people) => {
                    if (!people.isDeleted) {
                      formState.peopleIdList.push(people.id);
                    }
                  });
                  pStore.initPeopleSelectStore(formState.peopleIdList);
                } else if (item.scopeCategory === 'DEPT') {
                  selectDeptList.value = item.scopeInfo
                    .map((dept) => (dept.isDeleted ? dept.name + '（已从钉钉移除）' : dept.name))
                    .join('；');
                  formState.deptIdList = [];
                  item.scopeInfo.forEach((dept) => {
                    if (!dept.isDeleted) {
                      formState.deptIdList.push(dept.id);
                    }
                  });
                  console.log(formState.peopleIdList);
                  console.log(formState.deptIdList);
                  formState.scopeCategory.push(item.scopeCategory);
                }
              });
            }
          })
          .finally(() => {
            loading.value = false;
          });
      };
      getPlanScope();

      const scopeCategoryOptions = ref<SelectProps['options']>([
        {
          label: '部门',
          value: 'DEPT',
        },
        {
          label: '个人',
          value: 'PERSONAL',
        },
      ]);

      const [registerSelectPeopleModal, { openModal: openSelectPeopleModal }] = useModal();

      const toSelectPeopleModal = () => {
        openSelectPeopleModal(true, {
          selectedPeopleIdList: formState.peopleIdList,
        });
      };

      const [registerSelectDeptModal, { openModal: openSelectDeptModal }] = useModal();

      const toSelectDeptModal = () => {
        openSelectDeptModal(true, {
          checkedDeptKeys: formState.deptIdList,
        });
      };

      const selectDeptList = ref('');

      const onCheckDept = (checkDept) => {
        const deptIdList: string[] = [];
        const deptNameList: string[] = [];
        checkDept.forEach((dept) => {
          deptIdList.push(dept.key);
          if (dept.parentName) {
            deptNameList.push(dept.parentName + '/' + dept.name);
          } else {
            deptNameList.push(dept.name);
          }
        });
        formState.deptIdList = deptIdList;
        selectDeptList.value = deptNameList.join('；');
        if (
          selectDeptList.value.length &&
          !formState.scopeCategory.some((item) => item === 'DEPT')
        ) {
          formState.scopeCategory.push('DEPT');
        }
      };

      const selectPeopleList = ref('');

      const confirmSelectPeople = (data) => {
        formState.peopleIdList = data.selectedRowKeys;
        selectPeopleList.value = data.peopleList.map((people) => people.studentName).join('；');
        if (
          selectPeopleList.value.length &&
          !formState.scopeCategory.some((item) => item === 'PERSONAL')
        ) {
          formState.scopeCategory.push('PERSONAL');
        }
      };

      const formRef = ref();

      const onClickSubmit = () => {
        if (props.required) {
          const hasPeople = formState.peopleIdList && formState.peopleIdList.length > 0;
          const hasDept = formState.deptIdList && formState.deptIdList.length > 0;
          if (!hasPeople && !hasDept) {
            useMessage().createErrorNotification({
              message: '错误',
              description: '请选择部门或人员',
            });
            return;
          }
        }
        formRef.value.validateFields().then(() => {
          useMessage().createConfirm({
            iconType: 'info',
            title: '提示',
            content: '确定要提交吗？',
            onOk: () => {
              SaveEvaluationCriteriaPlanScope();
            },
            onCancel() {},
          });
        });
      };

      const validateFields = () => {
        return formRef.value.validateFields();
      };

      const SaveEvaluationCriteriaPlanScope = () => {
        loading.value = true;
        apiSaveEvaluationCriteriaPlanAndScope({
          evaluationCriteriaPlanScope: { ...formState },
        })
          .then((res) => {
            if (res.code === 200) {
              useMessage().createSuccessNotification({
                message: '成功',
                description: '保存成功',
              });
              emit('saveSuccess');
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .finally(() => {
            loading.value = false;
          })
          .catch(() => {
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络错误',
            });
          });
      };

      return {
        formState,
        scopeCategoryOptions,
        registerSelectPeopleModal,
        toSelectPeopleModal,
        registerSelectDeptModal,
        openSelectDeptModal,
        toSelectDeptModal,
        onCheckDept,
        confirmSelectPeople,
        selectPeopleList,
        loading,
        selectDeptList,
        formRef,
        onClickSubmit,
        validateFields,
        SaveEvaluationCriteriaPlanScope,
        getPlanScope,
      };
    },
  });
</script>
