<template>
  <div :style="showFileStyle">
<!--      <van-grid-item v-for="img in fileList" v-show="img.is_image"-->
<!--                     v-bind:key="img.file_id">-->
<!--        <van-image :src="img.file_url"-->
<!--                   fit="contain"-->
<!--                   height="100%"-->
<!--                   @click="ImagePreview([img.file_url])" />-->
<!--      </van-grid-item>-->
    <van-cell-group>
      <PictureDisplay v-if="fileList" :image-list="fileList" />
      <van-cell icon="label"  v-for="doc in fileList" :key="doc.file_id" v-show="!doc.is_image" >
        <template #title>
          <a :href="doc.file_url" style="font-size: 14px;color: #2F9AFB">
             <label>{{doc.file_name}}</label>
          </a>
        </template>
          <template #right-icon>
            <van-icon style="margin-top: 3px;" size="20" :name="copyLinkIcon" @click="copyLink(doc.file_url)"/>
          </template>
      </van-cell>
    </van-cell-group>
  </div>
</template>

<script>
import { Field, ImagePreview, Grid, GridItem, Toast } from "vant";
import {ref} from "vue";
import PictureDisplay from "./attachment/PictureDisplay.vue";
import {useRoute} from "vue-router";
import {copyLinkIcon} from '../resource.js'
export default {
  components: {
    PictureDisplay,
    [Field.name]: Field,
    [Grid.name]: Grid,
    [GridItem.name]: GridItem,
    [ImagePreview.name]: ImagePreview,
  },
  name: "ShowFile",
  props: {
    fileList: Array,
    showFileStyle: String
  },

  setup(props) {
    const route = useRoute()
    const imageList = ref([])
    return {
      ImagePreview,
      route,
      imageList,
      copyLinkIcon
    }
  },
  methods: {
    copyLink(fileUrl) {
      this.$copyText(fileUrl).then(() => {
        Toast({ message: '已经复制链接', type: 'success' })
      }, () => {
        Toast({ message: '无法复制链接,可能是浏览器的问题，请自行复制分享。', type: 'fail' })
      })
    }
  }
}
</script>

<style scoped lang="less">
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
:deep(.van-cell__left-icon){
  color: #1589f8;
}
</style>