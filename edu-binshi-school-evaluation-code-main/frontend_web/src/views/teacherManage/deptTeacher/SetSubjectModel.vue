<template>
  <div class="edit-evaluation-criteria-plan-modal" ref="editEvaluationCriteriaPlanModalRef">
    <BasicModal
      @register="register"
      :canFullscreen="false"
      :defaultFullscreen="false"
      :draggable="false"
      :destroyOnClose="true"
      :getContainer="() => $refs.editEvaluationCriteriaPlanModalRef"
      :closable="true"
      :centered="true"
      :maskClosable="false"
      width="60vw"
      :closeFunc="onCloseSetSubjectModel"
    >
      <template #title>
        <Icon icon="material-symbols:deployed-code-outline" />
        <span> 设置科目 </span>
      </template>
      <Loading :loading="fullScreenLoading" :absolute="false" />
      <div class="content">
        <Form
          :model="params"
          name="form"
          autocomplete="off"
          ref="formRef"
          layout="horizontal"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          :rules="formRules"
          style="margin-top: 20px"
        >
          <FormItem name="peopleName" label="教师姓名：" :colon="false">
            <Input v-model:value="peopleName" readonly />
          </FormItem>
          <FormItem name="deptName" label="班级：" :colon="false">
            <Input v-model:value="deptName" readonly />
          </FormItem>
          <FormItem name="selectedSubjectList" label="设置科目：" :colon="false">
            <Select
              ref="select"
              v-model:value="selectedSubjectList"
              style="width: 100%"
              :options="subjectParams.searchText ? subjectSearchOptions : subjectOptions"
              mode="multiple"
              @change="subjectChange"
              :fieldNames="{ label: 'name', value: 'name' }"
              placeholder="请选择科目名称"
              show-search
              :filter-option="false"
              allowClear
              @search="searchSubject"
              @focus="focusOnSelect"
              :autoClearSearchValue="true"
            />
          </FormItem>
        </Form>
      </div>
      <template #footer>
        <Button @click="onCloseSetSubjectModel" preIcon="ic:twotone-close" style="top: -1px"
          >关闭</Button
        >
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
    </BasicModal>
  </div>
</template>

<script lang="ts">
  import { defineComponent, nextTick, reactive, ref, toRefs } from 'vue';
  import { Loading } from '/@/components/Loading';
  import { Icon } from '/@/components/Icon';
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { Form, Input, Select } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import dayjs from 'dayjs';
  import utc from 'dayjs/plugin/utc';
  import {
    apiGetK12TeacherSubjectDetail,
    apiGetSubjectList,
    apiSaveK12TeacherSubject,
  } from '/@/api/k12TeacherSubject/k12TeacherSubject';
  import { useTabs } from '/@/hooks/web/useTabs';

  export default defineComponent({
    components: {
      Loading,
      Icon,
      BasicModal,
      Form,
      FormItem: Form.Item,
      Button,
      Select,
      Input,
    },
    emits: ['refreshTable'],
    setup() {
      dayjs.extend(utc);
      const subjectList = ref<Object[]>([]);
      const subjectOptions = ref<Object[]>([]);
      const subjectSearchOptions = ref<Object[]>([]);
      const formRef = ref();
      const fullScreenLoading = ref(false);
      const subjectLoading = ref(false);
      const peopleId = ref('');
      const peopleName = ref('');
      const deptName = ref('');
      const dimensionDeptTreeId = ref('');
      const k12TeacherSubject = ref<any>({});
      const selectedSubjectList = ref<string[]>([]);
      const duplicateTeacherSubject = ref<string[]>([]);
      const params = reactive({
        selectedSubjectList: selectedSubjectList.value,
        name: '',
        dateRange: null,
        status: null,
      });
      const [register, { closeModal }] = useModalInner((data) => {
        duplicateTeacherSubject.value = [];
        peopleId.value = data.peopleId;
        dimensionDeptTreeId.value = data.dimensionDeptTreeId;
        peopleName.value = data.peopleName;
        deptName.value = data.deptName;
        subjectList.value = [];
        subjectOptions.value = [];
        getK12TeacherSubjectDetail();
      });

      const getK12TeacherSubjectDetail = () => {
        fullScreenLoading.value = true;
        apiGetK12TeacherSubjectDetail(peopleId.value, dimensionDeptTreeId.value)
          .then((res) => {
            if (res.code === 200) {
              const selectedSubjectList: string[] = [];
              res.data.forEach((item) => {
                selectedSubjectList.push(item.subjectName);
              });
              getSubjectList(selectedSubjectList);
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
              description: '网络异常',
            });
          })
          .finally(() => {
            fullScreenLoading.value = false;
          });
      };
      const subjectParams = ref({
        pageIndex: 0,
        pageSize: 10,
        searchText: '',
        draw: 1,
      });

      const getSubjectList = (selectedSubjectList: string[] = []) => {
        subjectLoading.value = true;
        apiGetSubjectList()
          .then((res) => {
            if (res.code === 200) {
              subjectList.value.push(...res.data);
              subjectOptions.value.push(...res.data);
              if (selectedSubjectList) {
                nextTick(() => {
                  params.selectedSubjectList = selectedSubjectList;
                });
              }
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
              description: '网络异常',
            });
          })
          .finally(() => {
            subjectLoading.value = false;
          });
      };
      const validateSelectedSubjectList = async (_rule, _value) => {
        if (!params.selectedSubjectList) {
          return Promise.reject('请选择科目');
        }

        return Promise.resolve();
      };
      const { refreshPage } = useTabs();
      const formRules = {
        selectedSubjectList: [
          {
            trigger: ['blur', 'change'],
            message: '请选择科目',
            whitespace: false,
            validator: validateSelectedSubjectList,
          },
        ],
      };
      return {
        subjectList,
        formRef,
        fullScreenLoading,
        subjectParams,
        register,
        closeModal,
        refreshPage,
        params,
        ...toRefs(params),
        formRules,
        subjectLoading,
        subjectOptions,
        getSubjectList,
        peopleName,
        deptName,
        peopleId,
        dimensionDeptTreeId,
        k12TeacherSubject,
        duplicateTeacherSubject,
        subjectSearchOptions,
      };
    },
    methods: {
      subjectChange() {
        console.log('subjectChange');
        const newSubjectOptions: Object[] = [];
        const originalSubjectNameList: string[] = [];
        this.subjectList.forEach((item) => {
          originalSubjectNameList.push(item['name']);
        });
        this.selectedSubjectList.forEach((item) => {
          if (originalSubjectNameList.indexOf(item) < 0) {
            newSubjectOptions.push({
              id: item,
              name: item,
            });
          }
        });
        newSubjectOptions.push(...this.subjectList);
        this.subjectOptions = newSubjectOptions;
        this.subjectParams.searchText = '';
      },
      searchSubject(searchValue) {
        this.subjectParams.searchText = searchValue;
        let subjectSearchOptions: Object[] = [];
        subjectSearchOptions = this.subjectOptions.filter((item) =>
          // @ts-ignore
          item.name.includes(this.subjectParams.searchText),
        );
        if (subjectSearchOptions.length === 0 && this.subjectParams.searchText) {
          subjectSearchOptions.push({
            id: this.subjectParams.searchText,
            name: this.subjectParams.searchText,
          });
        }
        this.subjectSearchOptions = subjectSearchOptions;
      },
      onClickSubmit() {
        this.duplicateTeacherSubject = this.duplicateTeacherSubject.filter((item) =>
          this.selectedSubjectList.includes(item),
        );
        if (this.duplicateTeacherSubject.length > 0) {
          useMessage().createErrorNotification({
            message: '错误',
            description: '数据已发生改变，请刷新页面重试',
          });
        } else {
          this.formRef.validateFields().then(() => {
            useMessage().createConfirm({
              iconType: 'info',
              title: '提示',
              content: '确定要提交吗？',
              onOk: () => {
                this.saveK12TeacherSubject();
              },
              onCancel() {},
            });
          });
        }
      },
      focusOnSelect() {
        this.subjectParams.searchText = '';
        this.searchSubject('');
      },
      saveK12TeacherSubject() {
        const params = {
          peopleId: this.peopleId,
          dimensionDeptTreeId: this.dimensionDeptTreeId,
          subjectNameList: this.selectedSubjectList,
        };
        this.handleSaveK12TeacherSubject(params);
      },

      handleSaveK12TeacherSubject(params) {
        this.fullScreenLoading = true;
        apiSaveK12TeacherSubject(params)
          .then((res) => {
            if (res.code === 200) {
              if (res.data) {
                this.handleCallbackSaveTeacherSubject(res.data);
              } else {
                useMessage().createSuccessNotification({
                  message: '保存成功',
                });
                this.closeModal();
                this.$emit('refreshTable');
              }
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
          })
          .finally(() => {
            this.fullScreenLoading = false;
          });
      },
      handleCallbackSaveTeacherSubject(data) {
        let message = '';
        data.existedTeacherSubject.map((et, idx) => {
          this.duplicateTeacherSubject.push(et.subjectName);
          const subjectTeacher = `<text style="color: #00acc1">【${et.subjectName}】</text>科目已由<text style="color: #e7b0b0">【${et.peopleName}】</text>老师任教`;
          if (idx === 0) {
            message += `${subjectTeacher}`;
          } else {
            message += `<br/>${subjectTeacher}`;
          }
        });
        message += '<br/>确定要替换吗？';
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: message,
          onOk: () => {
            this.handleSaveK12TeacherSubject(data);
          },
        });
      },
      onCloseSetSubjectModel() {
        this.closeModal();
        this.subjectParams.searchText = '';
        this.$emit('refreshTable');
        return true;
      },
    },
  });
</script>

<style scoped lang="less">
  .edit-evaluation-criteria-plan-modal {
    ::v-deep(.ant-modal) {
      max-width: calc(100vw) !important;

      .scroll-container .scrollbar__wrap {
        margin-bottom: 0 !important;
      }

      .scrollbar__view {
        //height: calc(100% - 50px);
        height: 60vh;
        overflow: hidden;
      }

      .ant-modal-body {
        height: 100%;
        //background-color: #f0f2f5;
        .scrollbar {
          padding: 0 !important;
          overflow: hidden;
        }
      }

      .content {
        //height: 100%;
        height: 60vh;
        //background-color: #00acc1;
        overflow-y: auto;
        padding: 16px;
      }
    }
  }
</style>
