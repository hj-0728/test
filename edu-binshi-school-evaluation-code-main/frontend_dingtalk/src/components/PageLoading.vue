<template>
  <div>
    <van-overlay :show="true" :z-index="150">
      <van-loading size="50px" style="text-align: center;margin-top: 50%" vertical >加载中...</van-loading>
    </van-overlay>
  </div>
</template>

<script>
import { Overlay } from 'vant'
export default {
  components: {
    [Overlay.name]: Overlay
  }
}
</script>
