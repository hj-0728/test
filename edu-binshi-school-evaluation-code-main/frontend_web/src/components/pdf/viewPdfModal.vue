<template>
  <div class="pdf-view-modal" ref="pdfViewModalRef">
    <BasicModal
      @register="register"
      :canFullscreen="false"
      :defaultFullscreen="false"
      :draggable="false"
      :destroyOnClose="true"
      :closable="true"
      :centered="true"
      :maskClosable="false"
      width="90vw"
      :showOkBtn="false"
      :showCancelBtn="false"
      @cancel="onCloseModal"
    >
      <template #title>
        <Icon icon="carbon:report-data" />
        <span> 【{{ peopleName }}】评价报告 </span>
      </template>
      <Loading
        :loading="loading"
        :absolute="true"
        style="height: 100vh !important; display: flex; align-items: center"
      />
      <div class="toolbar">
        <Button
          type="primary"
          color="edit"
          :iconSize="16"
          preIcon="ph:download-simple"
          @click="downloadAssignmentReport"
        >
          下载报告
        </Button>
      </div>
      <div class="iframe-content">
        <iframe
          v-if="fileUrl !== null"
          width="100%"
          height="100%"
          style="overflow: hidden"
          id="pdf"
          :src="fileUrl"
          type="application/pdf"
          ref="iframe"
        ></iframe>
      </div>
    </BasicModal>
  </div>
</template>

<script lang="ts">
  import { BasicModal, useModalInner } from '/@/components/Modal';
  import { defineComponent, ref } from 'vue';
  import Icon from '/@/components/Icon/src/Icon.vue';
  import { apiGetFileDownloadUrl } from '/@/api/storage/storage';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { Loading } from '/@/components/Loading';
  import { Button } from '/@/components/Button';

  export default defineComponent({
    components: {
      Icon,
      BasicModal,
      Loading,
      Button,
    },
    emits: ['register', 'downloadAssignmentReport'],
    setup() {
      const iframe = ref();
      const loading = ref(true);
      const fileUrl = ref();
      const peopleName = ref('');
      const evaluationAssignmentId = ref('');
      const [register, { closeModal }] = useModalInner((data) => {
        if (data.fileId !== undefined) {
          if (data.fileId !== null) {
            getFileDownloadUrl(data.fileId);
            peopleName.value = data.peopleName;
            evaluationAssignmentId.value = data.evaluationAssignmentId;
          }
        } else {
          getFileDownloadUrlByResponse(data.response);
        }
      });
      const getFileDownloadUrl = (fileId) => {
        loading.value = true;
        apiGetFileDownloadUrl(fileId)
          .then((res) => {
            if (res.code === 200) {
              let x = new XMLHttpRequest();
              x.responseType = 'blob';
              x.open('GET', res.data, true);
              x.onload = function () {
                const blob = new Blob([x.response], {
                  type: 'application/pdf',
                });
                fileUrl.value = `${window.URL.createObjectURL(blob)}#toolbar=0`;
              };
              x.send();
            } else {
              useMessage().createErrorNotification(
                {
                  message: '错误',
                  description: res.error.message,
                },
                'pre-wrap',
              );
            }
          })
          .finally(() => {
            setTimeout(() => {
              loading.value = false;
            }, 500);
          });
      };

      const getFileDownloadUrlByResponse = (response) => {
        const blob = new Blob([response], {
          type: 'application/pdf',
        });
        fileUrl.value = `${window.URL.createObjectURL(blob)}#toolbar=0`;
        loading.value = false;
      };

      return {
        iframe,
        register,
        closeModal,
        fileUrl,
        loading,
        peopleName,
        evaluationAssignmentId,
      };
    },
    mounted() {},
    methods: {
      onCloseModal() {
        this.closeModal();
        this.fileUrl = null;
        this.peopleName = '';
        this.evaluationAssignmentId = '';
      },
      downloadAssignmentReport() {
        this.loading = true;
        this.$emit('downloadAssignmentReport', {
          evaluationAssignmentId: this.evaluationAssignmentId,
        });
      },
      closeLoading() {
        this.loading = false;
      },
    },
  });
</script>

<style scoped lang="less">
  .pdf-view-modal {
    ::v-deep(.ant-modal-body) {
      .scrollbar {
        padding: 0 !important;

        .scrollbar__view {
          div {
            height: 100vh !important;
          }
        }
      }
    }

    ::v-deep(.ant-modal-header) {
      display: none;
    }

    ::v-deep(.ant-modal-close) {
      display: none;
    }

    .close-pdf {
      width: 60px;
      position: fixed;
      bottom: 20px;
      right: 40px;
      border-radius: 30px;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #ffffff;
      opacity: 0.5;
      cursor: pointer;
      border: #adadad solid 1px;
    }

    .close-pdf:hover {
      opacity: 0.6;
    }

    .close-pdf:active {
      opacity: 0.5;
    }
  }

  .iframe-content {
    height: 68vh;
    background-color: #ccc;
  }

  .toolbar {
    width: 100%;
    height: 40px;
    display: flex;
    justify-content: end;
  }
</style>
