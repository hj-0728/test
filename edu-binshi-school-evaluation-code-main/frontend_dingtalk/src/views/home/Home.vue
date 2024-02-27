<template>
  <div>
    <van-swipe class="swipe" :autoplay="3000" indicator-color="white" height="200">
      <van-swipe-item>
        <img radius="8"
             :src="swipe2Image"/>
      </van-swipe-item>
    </van-swipe>

    <Space :height="15"></Space>
    <ComPeople @refresh-menu="refreshMenu"></ComPeople>
    <Space :height="13"></Space>
    <ComAbility ref="refComAbility"></ComAbility>

    <OverlayLoading v-if="loading"></OverlayLoading>

  </div>
</template>

<script>
import {ref, provide} from "vue";
import {swipe2Image} from '../../resource'
import {Swipe, SwipeItem} from 'vant';
import ComPeople from './ComPeople.vue'
import ComAbility from './ComAbility.vue'
import Space from "../../components/Space.vue";
import OverlayLoading from "../../components/OverlayLoading.vue";

export default {
  components: {
    ComPeople,
    ComAbility,
    Space,
    OverlayLoading,
    [Swipe.name]: Swipe,
    [SwipeItem.name]: SwipeItem,
  },
  setup() {
    const loading = ref(false);
    provide('loading', loading)
    return {
      swipe2Image,
      loading
    }
  },
  methods: {
    refreshMenu(){
      this.$refs.refComAbility.getMenuList();
    },
  },
}
</script>

<style scoped lang="less">
.swipe {
  .van-swipe-item {
    color: #fff;
    font-size: 20px;
    text-align: center;
    margin: 5px 0;

    img {
      width: calc(100% - 16px);
      border-radius: 8px;
      height: 195px;
    }
  }
}
</style>