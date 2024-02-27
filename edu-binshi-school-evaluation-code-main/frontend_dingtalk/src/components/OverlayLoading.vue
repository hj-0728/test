<template>
  <div>
    <van-overlay :show="true" :z-index="150">
      <van-loading v-if="showOriginalContent" size="50px" style="text-align: center;margin-top: 60%;color: white" vertical >加载中...</van-loading>
      <van-loading v-if="!showOriginalContent" size="50px" style="text-align: center;margin-top: 60%;color: white" vertical >
        {{ content }}</van-loading>
    </van-overlay>
  </div>
</template>

<script>
import { Overlay } from 'vant'
import { ref} from 'vue'
export default {
  components: {
    [Overlay.name]: Overlay
  },
  props: {
    content: String
  },
  setup(props) {
    const showOriginalContent = ref(true)
    // console.log(props.content)
    if (props.content !== undefined) {
      showOriginalContent.value = false
    }
    return {
      showOriginalContent
    }
  }
}

</script>
<style lang="less" scoped>
:deep(.van-overlay){
  background-color: rgb(0 0 0 / 40%)
}
:deep(.van-loading__text){
  color:white;
}
</style>