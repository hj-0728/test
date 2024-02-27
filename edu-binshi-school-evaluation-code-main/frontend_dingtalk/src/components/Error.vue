<template>
  <div style="background-color: white;height: 100vh">
    <div>
      <van-nav-bar fixed title="提示">
      </van-nav-bar>
    </div>
    <div class="view-wrapper_fixed_nav">
      <van-empty class="custom-image" :image="errorImage">
        <span>{{msg}}</span>
      </van-empty>
    </div>
  </div>
</template>

<script>
import { Empty } from 'vant'
import { useRouter } from 'vue-router'
import { errorImage } from '../resource.js'
export default {
  components: {
    [Empty.name]: Empty,
  },
  props: {
    msg: String
  },
  setup () {
    const router = useRouter()
    return {
      router,
      errorImage
    }
  },
  methods: {
    back () {
      this.$router.isBack = true
      this.$router.back()
    }
  }
}
</script>

<style lang="less" scoped>
.custom-image .van-empty__image {
  width: 90px;
  height: 90px;
}
:deep(.custom-image){
  padding: 90px 0;
}
:deep(.van-empty__description) {
  margin-top: 16px;
  padding: 8px 60px;
  color: #969799;
  font-size: 20px;
  line-height: 20px;
}
:deep(.van-empty__bottom){
  padding-top: 12px;
  margin-left: 8%;
  margin-right: 8%;
  word-break: break-all;
  line-height: 1.6;
}
:deep(.van-empty__image) {
  width: 60%;
  height: 100%;
}
</style>
