<template>
  <div>
    <van-grid :column-num="1" v-if="imageList.length===1" :border="false" style="padding:0 10px">
      <van-grid-item v-show="image.is_image"
                     v-for="image in imageList"
                     v-bind:key="image.file_id" style="height: 100%;" class="single-grid-item">
        <van-image :src="image.file_thumbnail_url"
                   class="single-image"
                   @click="ImagePreview([image.file_url])"/>
      </van-grid-item>
    </van-grid>

    <van-grid :column-num="2" square v-else-if="imageList.length===4||imageList.length===2" :border="false"
              style="padding: 4px 32% 4px 10px">
      <!--          <van-grid-item v-for="(a) in data.file_info_list" v-bind:key="a.file_id">-->
      <!--            <van-image :src="a.file_url" @click="ImagePreview([a.file_url])" />-->
      <!--          </van-grid-item>-->
      <van-grid-item style="width:95%;height: 95%" v-for="(image,index) in imageList" v-bind:key="image.file_id"
                     v-show="image.is_image">
        <van-image :src="image.file_thumbnail_url"
                   fit="cover"
                   height="100%"
                   @click="ImagePreview({images:imageUrlList,startPosition:index,loop:false})"/>
      </van-grid-item>
    </van-grid>

    <van-grid :column-num="3" square v-else :border="false">
      <!--          <van-grid-item v-for="(a) in data.file_info_list" v-bind:key="a.file_id">-->
      <!--            <van-image :src="a.file_url" @click="ImagePreview([a.file_url])" />-->
      <!--          </van-grid-item>-->
      <van-grid-item v-for="(image,index) in imageList.slice(0,9)" v-bind:key="image.file_id" v-show="image.is_image">
        <div style="width:95%;height: 95%;position:absolute;">

          <van-image :src="image.file_thumbnail_url"
                     fit="cover"
                     width="100%"
                     height="100%"
                     @click="openImagePreview(index)"

          >
            <div class="mask" v-if="imageList.length>9&&index===8">
              <p class="remainder">+{{ imageList.length - 9 }}</p>
            </div>
          </van-image>
        </div>
      </van-grid-item>
    </van-grid>
    <van-image-preview v-model:show="show" :images="imageUrlList" :start-position="imageIndex" :loop="false">
    </van-image-preview>
    <div :class="slideClass" id="slide-div" v-show="show&&imageList.length>9">
      <div class="slide-ball">
        <van-icon v-if="!isSlide" name="arrow-up" size="30px" style="margin-top: 5px" color="white"
                  @click="slideToggle"/>
        <van-icon v-else name="arrow-down" size="30px" style="margin-top: 10px" color="white" @click="slideToggle"/>
      </div>
      <div class="slide-abbreviation-div">
        <div v-for="(image,index) in imageList" v-bind:key="image" class="slide-abbreviation-img">
          <van-image :src="image.file_thumbnail_url"
                     fit="cover"
                     width="100%"
                     height="100%"
                     @click="imageIndex=index"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {ref} from "vue";
import {ImagePreview, Grid, GridItem, Loading, Notify, Swipe, SwipeItem} from 'vant'

export default {
  props: ['imageList'],
  components: {
    [Image.name]: Image,
    [ImagePreview.name]: ImagePreview,
    [Grid.name]: Grid,
    [GridItem.name]: GridItem,
    [Swipe.name]: Swipe,
    [SwipeItem.name]: SwipeItem,
    [Notify.name]: Notify,
    [Loading.name]: Loading,
    [ImagePreview.Component.name]: ImagePreview.Component
  },
  setup(props) {
    const imageList = props.imageList.filter(item => item.is_image === true)
    const imageUrlList = ref([])
    // 缩略图
    const minImageUrlList = ref([])
    const show = ref(false)
    const isShowAll = ref(false)
    const isSlide = ref(false)
    const slideClass = ref('slide-div closed')
    const imageIndex = ref(0)
    imageList.forEach(item => {
      imageUrlList.value.push(item.file_url)
      minImageUrlList.value.push(item.file_thumbnail_url)
    })
    console.log(imageList)
    return {
      imageList,
      imageUrlList,
      ImagePreview,
      show,
      imageIndex,
      minImageUrlList,
      isShowAll,
      isSlide,
      slideClass
    }
  },
  methods: {
    load(index) {
      console.log(index)
    },
    openImagePreview(index) {
      this.show = true
      this.imageIndex = index
    },
    slideToggle() {
      if (!this.isSlide) {
        // document.getElementById('slide-div').classList.remove('closed')
        this.slideClass = 'slide-div open'
      } else {
        // document.getElementById('slide-div').classList.remove('open')
        this.slideClass = 'slide-div closed'
      }
      this.isSlide = !this.isSlide
    },


  }
}
</script>

<style scoped>
.mask {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-items: center;
  text-align: center;
}

.remainder {
  margin: 0 auto;
  color: white;
  font-size: 35px;
  font-weight: bold;
}

.slide-div {
  width: 100%;
  max-height: 35px;
  position: fixed;
  z-index: 9999;

  background-color: rgba(0, 0, 0, 1);
  bottom: 0;
  left: 0;
  border-radius: 20px 20px 0 0;
  /*overflow-y: hidden;*/
  /* 最大高度 */
  /*  Webkit内核浏览器：Safari and Chrome*/
  -webkit-transition-property: all;
  -webkit-transition-duration: .5s;
  -webkit-transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
  /*  Mozilla内核浏览器：firefox3.5+*/
  -moz-transition-property: all;
  -moz-transition-duration: .5s;
  -moz-transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
  /*  Opera*/
  -o-transition-property: all;
  -o-transition-duration: .5s;
  -o-transition-timing-function: cubic-bezier(0, 1, 0.5, 1);
  /*  IE9*/
  -ms-transition-property: all;
  -ms-transition-duration: .5s;
  -ms-transition-timing-function: cubic-bezier(0, 1, 0.5, 1)
}

.slide-ball {
  width: 50px;
  height: 50px;
  background-color: rgba(0, 0, 0);
  position: fixed;
  border-radius: 50%;
  left: 50%;
  transform: translate(-50%, -30%);
  align-items: center;
  justify-items: center;
  text-align: center;
  overflow: scroll;
  float: left;
}

.slide-div.closed {
  max-height: 35px;
}

.slide-div.open {
  max-height: 35%;
}

.slide-abbreviation-div {
  width: 100%;
  float: left;
  margin: 10% 0;
  white-space: nowrap;
  overflow-x: auto;
  overflow-y: hidden;
}

.slide-abbreviation-img {
  width: 100px;
  height: 100px;
  margin: 10px;
  display: inline-block;
  color: white;
}

.slide-abbreviation-img:focus {
  border: 5px solid #FFFFFF;
}

:deep(.van-grid-item__content) {
  padding: 2px;

}

:deep(.single-image>.van-image__img) {
  width: auto;
  height: 100%;
  /*background: yellow;*/

}

:deep(.single-image>.van-image__img) {
  width: 100%;
  height: auto;
  max-height: 220px;
  object-fit: cover;
}

:deep(.single-grid-item>.van-grid-item__content) {
  align-items: initial;
  /*display: block;*/
}

</style>