<template>
  <div class="error-container">
    <div>
      <van-nav-bar fixed title="提示"
                   :left-arrow="leftArrow"
                   @click-left="$router.back()">
      </van-nav-bar>
    </div>
    <div class="view-wrapper_fixed_nav">
      <van-empty class="custom-image" :image="errorImage">
        <span>{{ errorMsg }}</span>
      </van-empty>
    </div>
  </div>
</template>

<script>

import {ref} from 'vue'
import {errorImage} from '../../resource'
import constant from "../../constant";
import {Empty} from 'vant'

export default {
  components: {
    [Empty.name]: Empty
  },
  setup() {
    const errorMsg = ref(constant.networkAnomaly)
    const leftArrow= ref(true)
    return {
      errorMsg,
      errorImage,
      leftArrow
    }
  },

  created() {
    const query = this.$route.query
    if (query.data) {
      this.errorMsg = decodeURIComponent(query.data)
    }
    if (query.hideLeftArrow) {
      this.leftArrow = false
    }
  }
}
</script>

<style scoped>
.error-container {
  background-color: white;
  height: 100vh
}
</style>
