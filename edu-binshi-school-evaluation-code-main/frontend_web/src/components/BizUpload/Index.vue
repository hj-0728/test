<template>
  <div>
    <Loading :loading="loading" />
    <Upload
      v-if="canEdit"
      v-model:file-list="fileList"
      :multiple="true"
      :custom-request="onUploadFile"
      :before-upload="onBeforeUpload"
      :showUploadList="false"
      class="mini-upload"
    >
      <div class="ant-upload ant-upload-select ant-upload-select-picture-card">
        <div class="ant-upload" style="display: flex; align-items: center; justify-content: center">
          <div>
            <Icon icon="uil:upload" :size="20" color="rgb(9, 96, 189)" />
            <div class="ant-upload-text">上传</div>
          </div>
        </div>
      </div>
    </Upload>
    <div style="width: 100%" @click.stop="">
      <div v-for="file in DBFileList" class="file-card" :key="file.id">
        <Row style="display: flex; align-items: center; flex: 1">
          <Col :span="22" style="flex: 1; width: 0">
            <div class="file-name" @click="onClickFile(file)" :title="file.originalName">
              {{ file.originalName }}
            </div>
          </Col>
          <Col :span="1">
            <DeleteOutlined
              v-if="canEdit"
              style="color: rgb(255, 77, 79); font-size: 20px"
              @click.stop="onRemoveFile(file)"
            />
          </Col>
        </Row>
      </div>
      <div v-if="DBFileList.length <= 0 && !canEdit" class="no-file-div">未上传附件</div>
    </div>
    <ViewPdfModal @register="registerViewPdfModal" />
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue';
  import { Col, Row, Upload } from 'ant-design-vue';
  import { DeleteOutlined } from '@ant-design/icons-vue';
  import { apiUploadFile } from '/@/api/storage/storage';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { Loading } from '/@/components/Loading';
  import { Icon } from '/@/components/Icon';
  import ViewPdfModal from '/@/components/pdf/viewPdfModal.vue';
  import { useModal } from '../Modal';
  import { createImgPreviewAutoSize } from '/@/components/PreviewAutoSize/src/functional';

  export default defineComponent({
    components: {
      Upload,
      DeleteOutlined,
      Row,
      Col,
      Loading,
      Icon,
      ViewPdfModal,
    },
    props: {
      canEdit: Boolean,
      dbFileList: {
        type: Array,
        default: () => {
          return [];
        },
      },
    },
    emits: ['change'],
    setup(props) {
      const DBFileList = ref<object[] | unknown>([]);
      if (props.dbFileList) {
        // eslint-disable-next-line vue/no-setup-props-destructure
        DBFileList.value = props.dbFileList;
      }
      const [registerViewPdfModal, { openModal: openViewPdfModal }] = useModal();
      const fileList = ref([]);
      const loading = ref(false);
      return {
        fileList,
        loading,
        registerViewPdfModal,
        openViewPdfModal,
        DBFileList,
      };
    },
    methods: {
      onUploadFile(_) {
        return;
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
        });
        params.append('fileUidListStr', fileUids.join('&&&&'));
        this.loading = true;
        let title = '';
        let content = '';
        apiUploadFile(params)
          .then((r) => {
            const currentDuplicateFiles = [];
            if (r.code === 200) {
              // @ts-ignore
              const existedChecksumList = this.DBFileList.map((f) => f.checksum);
              r.data.map((item) => {
                let currentFileListObj = this.fileList.filter((o) => o.uid === item.remark)[0];
                if (existedChecksumList.includes(item.checksum)) {
                  currentDuplicateFiles.push(item.originalName);
                  currentFileListObj.status = 'error';
                } else {
                  this.$emit('change');
                  existedChecksumList.push(item.checksum);
                  currentFileListObj.name = item.originalName;
                  currentFileListObj.status = 'done';
                  currentFileListObj.url = item.url;
                  currentFileListObj.fileId = item.id;
                  currentFileListObj.checksum = item.checksum;
                  this.DBFileList.push(item);
                }
              });
              if (currentDuplicateFiles.length > 0) {
                title = '请勿上传重复文件';
                content += '<span style="color: black">重复文件：</span><br>';
                currentDuplicateFiles.map((f) => {
                  content += '<span >' + f + '</span><br>';
                });
                currentDuplicateFiles.length = 0;
              }
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
            this.loading = false;
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
            this.deleteFile(file);
          },
        });
        return false;
      },

      deleteFile(file) {
        const index = this.DBFileList?.indexOf(file);
        this.DBFileList?.splice(index, 1);
        this.fileList = this.fileList.filter((f) => f.uid != file.uid);
      },

      getDbFileIds() {
        return this.DBFileList.map((f) => f.id);
      },

      onClickFile(file) {
        if (file.isImage) {
          createImgPreviewAutoSize({
            imageList: [file.url],
            scaleStep: 10,
            maskClosable: true,
          });
        } else if (file.isPdf) {
          this.openViewPdfModal(true, { fileId: file.id });
        } else {
          window.open(file.url);
        }
      },
    },
  });
</script>

<style scoped>
  .file-name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #0960bd;
    cursor: pointer;
  }
</style>
