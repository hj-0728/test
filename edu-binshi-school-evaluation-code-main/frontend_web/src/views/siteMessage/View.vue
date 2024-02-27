<template>
  <div style="width: 100%; padding-bottom: 60px">
    <div class="message-content" v-if="messageInfo">
      <Row>
        <Col :span="4">
          <div style="color: #959595">消息类型</div>
        </Col>
        <Col :span="20">
          <div>
            <Tag v-if="messageInfo.initResourceCategoryName" color="processing">
              {{
                messageInfo.initResourceCategoryName && messageInfo.content
                  ? messageInfo.initResourceCategoryName
                  : ''
              }}
            </Tag>
          </div>
        </Col>
      </Row>
      <Row>
        <Col :span="4">
          <div style="color: #959595">标题</div>
        </Col>
        <Col :span="20">
          <div style="font-weight: bold">
            <div>{{ messageInfo.title ? messageInfo.title : '' }}</div>
          </div>
        </Col>
      </Row>
      <Row>
        <Col :span="4">
          <div style="color: #959595">发送时间</div>
        </Col>
        <Col :span="20">
          <div>
            <div>{{ messageInfo.sendAt ? messageInfo.sendAt : '' }}</div>
          </div>
        </Col>
      </Row>
      <Row>
        <Col :span="4">
          <div style="color: #959595"> 内容</div>
        </Col>
        <Col :span="20">
          <div class="content">
            <div>{{ messageInfo.content }}</div>
          </div>
        </Col>
      </Row>
      <Row style="margin-top: 10px">
        <Col :span="4" />
        <Col :span="20">
          <Button
            type="primary"
            color="green"
            preIcon="ph:download-simple"
            :iconSize="16"
            @click="downloadFile(messageInfo.fileId)"
            v-if="messageInfo.fileId"
          >
            下载
          </Button>
        </Col>
      </Row>
    </div>
  </div>
</template>
<script lang="ts">
  import { defineComponent, ref, shallowRef } from 'vue';
  import { Col, Row, Tag } from 'ant-design-vue';
  import { apiGetSiteMessageInfo } from '/@/api/siteMessage/siteMessage';
  import dayjs from 'dayjs';
  import { useMessage } from '/@/hooks/web/useMessage';
  // import { apiGetFileUrlByFileId } from '/@/api/file/file';
  import { useAppStore } from '/@/store/modules/app';
  import { Button } from '/@/components/Button';
  import { apiGetFileDownloadUrl } from '/@/api/storage/storage';

  export default defineComponent({
    components: {
      Row,
      Col,
      Tag,
      Button,
    },
    props: {
      messageId: String,
    },
    setup(props) {
      const appStore = useAppStore();
      const loading = ref(false);
      const messageInfo = ref();
      const downloadLoading = ref<boolean>(false);
      const module = shallowRef(null);

      function getFilenameFromHeader(res) {
        let fileName = res.headers['content-disposition'].split('filename*=')[1].split(';')[0];
        fileName = decodeURIComponent(fileName).replace(/UTF-8''/g, '');
        return fileName;
      }

      const getMessageInfo = async () => {
        messageInfo.value = undefined;
        if (props.messageId) {
          await apiGetSiteMessageInfo(props.messageId).then((res) => {
            if (res.code === 200) {
              messageInfo.value = res.data;
              if (messageInfo.value.readAt) {
                appStore.setUpdateUnreadStatusFlag(true);
              }
              messageInfo.value.sendAt = dayjs(messageInfo.value.createdAt).format(
                'YYYY-MM-DD HH:mm',
              );
            } else {
              useMessage().notification.destroy();
              useMessage().createErrorNotification({
                message: '信息获取失败！',
                description: res.error.message,
              });
            }
          });
        }
      };
      getMessageInfo();

      return {
        messageInfo,
        downloadLoading,
        dayjs,
        getFilenameFromHeader,
        module,
        getMessageInfo,
        loading,
      };
    },
    watch: {
      messageId: {
        handler: function () {
          this.getMessageInfo();
        },
      },
    },
    methods: {
      downloadFile(fileId) {
        this.loading = true;
        apiGetFileDownloadUrl(fileId)
          .then((res) => {
            if (res.code === 200) {
              window.location.href = res.data;
              useMessage().createSuccessNotification({
                message: '操作成功',
                description: '文件下载完成',
              });
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .finally(() => {
            this.loading = false;
          });
      },
    },
  });
</script>

<style lang="less" scoped>
  .message-content {
    padding: 20px;
    width: 90%;
    margin-left: 5%;
    line-height: 30px;
  }

  ::v-deep(.content) {
    a {
      font-size: 18px !important;
      font-weight: 800 !important;
      color: #0960bd !important;
    }
  }
</style>
