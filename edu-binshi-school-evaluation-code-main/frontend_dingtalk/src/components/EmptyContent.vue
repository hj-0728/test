<template>
  <div>
    <van-empty :image="emptyImg" v-if="isShow" :description="description"/>
  </div>
</template>

<script>
import { Empty} from 'vant'
import { emptyImg } from '../resource.js'
export default {
  components: {
    [Empty.name]: Empty
  },
  props: {
    isShow: Boolean,
    description: String
  },
  setup () {
    return {
      emptyImg
    }
  }
}
</script>

<style lang="less" scoped>

:deep(.van-empty__image) {
  width: 70%;
  height: 100%;
}
</style>
