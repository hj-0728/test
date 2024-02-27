<template>
<!--  <van-cell-group title="附件" style="background: #efefef">-->
    <van-cell class="attachment-uploder" :style="disabledBorderRadius === true ? '' : 'border-radius:0 0 8px 8px' ">
        <van-uploader
            v-model="imageList"
            multiple
            :preview-size="previewSize + 'rem'"
            :after-read="afterRead"
            :before-delete="beforeDelete"
            accept="*"
            :max-count="maxCount"
            :show-upload="showUpload"
        >
        </van-uploader>
        <van-cell
          v-for="doc in fileList"
          v-bind:key="doc.file_id"
          v-show="!doc.isImage"
        >
        <template #icon>
          <van-icon style="margin: 3px 5px 0 0" name="label" size="20" color="#2F9AFB"></van-icon>
        </template>
        <template #title>
          <a :href="doc.hint.file_url" style="font-size: 14px; color: #2f9afb">
            {{ doc.hint.file_name }}
          </a>
        </template>
        <template #right-icon>
          <van-icon
            plain
            style="float: right; border: 0; margin: 6px"
            name="cross"
            @click="deleteFile(doc)"
          />
        </template>
      </van-cell>
    </van-cell>
  <OverlayLoading v-if="loadingShow"></OverlayLoading>
</template>
<script>
// 参考： https://vant-contrib.gitee.io/vant/#/zh-CN/uploader
import { Notify, Uploader, CellGroup, Cell } from "vant";
import { ref, reactive } from "vue";
import OverlayLoading from "../OverlayLoading.vue";
import {apiUploadFile} from "../../api/storage";
export default {
  components: {
    OverlayLoading,
    [Uploader.name]: Uploader,
    [Notify.name]: Notify,
    [CellGroup.name]: CellGroup,
    [Cell.name]: Cell,
  },
  props: {
    disabledBorderRadius: Boolean,
  },
  setup() {
    const fileList = ref([]);
    const imageList = ref([]);
    const resultFileList = ref([]);
    const loadingShow = ref(false);
    const showUpload = ref(true);
    const previewSize = ref((document.body.clientWidth/16 - 76/16)/3)
    const maxCount = ref(9)

    function clearAllFileList() {
      fileList.value.splice(0);
      imageList.value.splice(0);
      resultFileList.value.splice(0);
    }

    return {
      fileList,
      imageList,
      resultFileList,
      loadingShow,
      previewSize,
      clearAllFileList,
      showUpload,
      maxCount,
    };
  },
  methods: {
     afterRead(files) {
      if (files.length) {
        console.log('files', files.length)
        console.log(this.imageList.length-files.length)
        const len = this.maxCount - this.fileList.length - (this.imageList.length - files.length)
        let index = 1;
        console.log('len--', len)
        for (const file of files) {
          console.log('index---', index)
          if(index > len) {
            console.log('结束')
            this.imageList.splice(this.imageList.indexOf(file), 1)
          } else {
            file.status = "uploading";
            file.message = "上传中...";
            this.uploadFile(file);
          }
          index += 1;
        }
      } else {
        if (files.file.type === "image/jpeg") {
          files.status = "uploading";
          files.message = "上传中...";
        } else {
          this.loadingShow = true;
        }
         this.uploadFile(files);
      }
       console.log(this.imageList.length)
    },
    uploadFile(file) {
      const params = new FormData()
      params.append('files', file.file)
      apiUploadFile(params).then(r => {
        if (r.data.code === 200) {
          console.log('apiUploadFile 200')
          file.hint = r.data.data[0]
          this.resultFileList.push(file)
          if (r.data.data[0].is_image) {
            file.status = 'done'
          } else {
            console.log('apiUploadFile 300')
            this.imageList.splice(this.imageList.indexOf(file), 1)
            this.fileList.push(file)
            // setTimeout(() => { this.loadingShow = false }, 200)
          }
        } else {
          file.status = 'failed'
          Notify({ type: 'danger', message: r.data.messages.join(';') })
        }
      }).catch(e => {
        file.status = 'failed'
        console.log('upload file error:', e)
      }).finally(()=>{
        this.loadingShow = false;
      })

      this.showUpload = this.imageList.length + this.fileList.length < this.maxCount;
      // setTimeout(() => {
      //   this.loadingShow = false;
      // }, 1000);
    },
    beforeDelete(file) {
      const delIndex = ref(null);
      this.imageList.forEach(function (value, index) {
        if (value === file) {
          delIndex.value = index;
        }
      });
      console.log(delIndex)
      this.imageList.splice(delIndex.value, 1);
      this.resultFileList.forEach((value, index) => {
        if (value === file) {
          this.resultFileList.splice(index, 1);
        }
      });
      this.showUpload = this.imageList.length + this.fileList.length < this.maxCount;
    },
    deleteFile(doc) {
      console.log(11111)
      const delIndex = ref(null);
      this.fileList.forEach(function (value, index) {
        if (value === doc) {
          delIndex.value = index;
        }
      });
      this.fileList.splice(delIndex.value, 1);
      this.resultFileList.forEach((value, index) => {
        if (value === doc) {
          this.resultFileList.splice(index, 1);
        }
      });
      this.showUpload = this.imageList.length + this.fileList.length < this.maxCount;
    },

    initDBFileList(dbFileList) {
      const fileList = []
      for (const dbFile of dbFileList) {
        fileList.push({
          url: dbFile.file_url,
          isImage: dbFile.is_image,
          hint: dbFile
        })
      }
      fileList.forEach(item => {
        if (item.isImage) {
          this.imageList.push(item)
        } else {
          this.fileList.push(item)
        }
        this.resultFileList.push(item)
      })
      console.log(this.imageList)
    },


  },
};
</script>

<style lang="less" scoped>
:deep(.dynamic-item_title) {
  display: flex;
  align-items: center;
  justify-items: center;
  span {
    display: flex;
    align-items: center;
    margin: 0 10px 0 0;
    font-size: 14px;
    label {
      font-size: 14px;
      color: #1589f8;
      font-weight: bold;
    }
  }
}

:deep(.van-uploader__preview) {
    margin: 0 12px 12px 0;
  }
:deep(.van-uploader__preview:nth-child(3)) {
    margin: 0 0 12px 0;
  }
:deep(.van-uploader__preview:nth-child(6)) {
    margin: 0 0 12px 0;
  }
:deep(.van-uploader__preview:nth-child(9)) {
    margin: 0 0 12px 0;
  }
:deep(.van-uploader__upload) {
  margin: 0 0 8px 0;
}

</style>
