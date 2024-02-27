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
          <Icon icon="ant-design:plus-outlined" />
          {{ '添加荣誉勋章' }}
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
            name="points"
            label="描述："
            :colon="false"
            :rules="[{ required: true, message: '请输入荣誉描述' }]"
          >
            <TextArea v-model:value="selectedGoalName" placeholder="请输入荣誉描述" />
          </FormItem>
          <FormItem name="dateRange" label="分值：" :colon="false">
            <Input v-model:value="points" />
          </FormItem>
          <FormItem label="勋章图片：" name="fileList" :colon="false">
            <UploadDragger
              v-model:file-list="fileList"
              :showUploadList="false"
              :multiple="true"
              :before-upload="onBeforeUpload"
              :remove="removeFile"
              :custom-request="uploadFile"
              style="width: 100%; padding-top: 10px; padding-bottom: 10px"
            >
              <CloudUploadOutlined style="font-size: 50px" />
              <p class="ant-upload-text">{{ uploadTitle }}</p>
              <p class="ant-upload-hint"> {{ uploadDescription }}</p>
            </UploadDragger>
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
    </BasicModal>
  </div>
</template>
<script lang="ts">
  import { defineComponent, reactive, Ref, ref, toRefs } from 'vue';
  import BasicModal from '/@/components/Modal/src/BasicModal.vue';
  import { Icon } from '/@/components/Icon';
  import { Form, Input, Upload } from 'ant-design-vue';
  import { Button } from '/@/components/Button';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { useModal, useModalInner } from '/@/components/Modal';
  import { ErrorNotificationEnum } from '/@/enums/notificationEnum';
  import { apiGetTeamDetail } from '/@/api/team/team';
  import { Loading } from '/@/components/Loading';
  import dayjs from 'dayjs';
  import utc from 'dayjs/plugin/utc';
  import weekday from 'dayjs/plugin/weekday';
  import localeData from 'dayjs/plugin/localeData';
  import { apiUploadFile } from '/@/api/storage/storage';
  import { CloudUploadOutlined } from '@ant-design/icons-vue';
  export default defineComponent({
    components: {
      Loading,
      Button,
      Icon,
      BasicModal,
      Form,
      FormItem: Form.Item,
      TextArea: Input.TextArea,
      UploadDragger: Upload.Dragger,
      Input: Input,
      CloudUploadOutlined,
    },
    setup() {
      dayjs.extend(utc);
      dayjs.extend(weekday);
      dayjs.extend(localeData);
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
        dateRange: ['', ''],
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
      const endOpen = ref<boolean>(false);
      const handleStartOpenChange = (open: boolean) => {
        const [planStartAt, planFinishAt] = formState.dateRange;
        if (!open) {
          endOpen.value = true;
          if (!planFinishAt && planStartAt) {
            formState.dateRange[1] = dayjs(planStartAt).add(1, 'hour');
          }

          if (
            dayjs(planFinishAt).format('YYYY-MM-DD HH:00') <=
              dayjs(planStartAt).format('YYYY-MM-DD HH:00') &&
            planStartAt
          ) {
            formState.dateRange[1] = dayjs(planStartAt).add(1, 'hour');
          }
        }

        if (dayjs(planFinishAt).isBefore(dayjs(planStartAt))) {
          formState.dateRange[1] = '';
        }
      };

      const handleEndOpenChange = (open: boolean) => {
        endOpen.value = open;
      };
      const points = ref(10);

      const uploadTitle = ref('点击或拖拽文件至此区域即可上传');
      const uploadDescription = ref('支持单个或批量上传。');

      const fileIcon = ref({
        jpg: 'ant-design:file-image-outlined',
        png: 'ant-design:file-image-outlined',
        pdf: 'vscode-icons:file-type-pdf2',
        docx: 'vscode-icons:file-type-word',
        xlsx: 'vscode-icons:file-type-excel',
        xls: 'vscode-icons:file-type-excel',
        pptx: 'vscode-icons:file-type-powerpoint',
      });
      const defaultIcon = ref('ant-design:file-outlined');

      const fileList = ref([]);
      const imgUrl = ref('');
      const visible = ref<boolean>(false);
      const setVisible = (value) => {
        visible.value = value;
      };
      const viewFile = (file) => {
        if (['jpg', 'png'].includes(file.type)) {
          visible.value = !visible.value;
          imgUrl.value = file.url;
        } else {
          downloadFile(file.url);
        }
      };

      const downloadFile = (url) => {
        // 创建一个隐藏的链接元素用于下载
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      };
      return {
        viewFile,
        imgUrl,
        setVisible,
        visible,
        defaultIcon,
        fileList,
        uploadTitle,
        uploadDescription,
        fileIcon,
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
        dayjs,
        handleStartOpenChange,
        handleEndOpenChange,
        endOpen,
        points,
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
        this.closeModal();
      },
      onClickSubmit() {
        useMessage().createConfirm({
          iconType: 'info',
          title: '提示',
          content: '确定要提交吗？',
          onOk: () => {
            this.saveTeam();
          },
          onCancel: () => {},
        });
      },
      saveTeam() {
        this.fullScreenLoading = true;
        this.$emit('saveSuccess');
        this.clearParams();
        this.onCloseModal();
        this.fullScreenLoading = false;
        this.clearParams();
      },
      getFileExtension(fileName) {
        // 匹配最后一个点（.）后的字符，不包含点本身
        const match = fileName.match(/\.([^./\\]+)$/);

        if (match) {
          return match[1];
        } else {
          return ''; // 如果没有匹配到后缀，返回空字符串
        }
      },
      onBeforeUpload(file, files) {
        if (files.indexOf(file) !== files.length - 1) {
          return;
        }
        const fileUids = [];
        const params = new FormData();
        files.map((pf) => {
          fileUids.push(pf.uid);
          params.append('files', pf);
          pf.spinning = true;
          Object.defineProperty(pf, 'type', {
            value: this.getFileExtension(pf.name),
            writable: true,
          });
          this.fileList.push(pf);
        });
        params.append('fileUidListStr', fileUids.join('&&&&'));
        // this.loading = true;
        let title = '';
        let content = '';
        apiUploadFile(params)
          .then((res) => {
            if (res.code === 200) {
              res.data.map((item) => {
                this.$emit('change');
                item.name = item.originalName;
                item.status = 'done';
                item.fileId = item.id;

                this.fileList = this.fileList.map((fileItem) => {
                  if (fileItem.uid === item.uid) {
                    fileItem.url = item.url;
                    fileItem.checksum = item.checksum;
                    fileItem.spinning = false;
                    fileItem.id = item.id;
                  }
                  return fileItem;
                });
              });
            }
          })
          .catch((e) => {
            console.error('文件上传失败：', e);
            content += '<span style="color: black">上传失败文件：</span><br>';
            files.map((f) => {
              this.fileList = this.fileList.filter((f2) => f2.uid != f.uid);
              content += '<span >' + f.name + '</span><br>';
            });
          })
          .finally(() => {
            if (content) {
              if (title === '') {
                title = '上传失败';
              }
              useMessage().createErrorModal({
                title: title,
                content: content,
                closable: true,
                maskClosable: true,
                showOkBtn: true,
                showCancelBtn: false,
              });
            }
            this.fullScreenLoading = false;
            this.fileList.forEach((item) => {
              if (item.status === 'error') {
                this.fileList = this.fileList.filter((f) => f.uid != item.uid);
              }
            });
          });
      },
      onRemoveFile(file) {
        useMessage().createConfirm({
          title: '确定要删除此附件吗？',
          iconType: 'warning',
          onOk: () => {
            this.$emit('change');
            this.removeFile(file);
          },
        });
        return false;
      },
      removeFile(file) {
        this.fileList = this.fileList.filter((f) => f.uid != file.uid);
      },
      uploadFile() {
        return;
      },
    },
  });
</script>
