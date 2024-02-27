<template>
  <router-view v-if="isRouterAlive" v-slot="{ Component }">
    <transition :name="transName" >
      <component :is="Component" appear/>
    </transition>
  </router-view>
</template>

<script>
  import { useStore } from 'vuex'
  import {onMounted, ref} from 'vue';
export default {
  provide() {
    return {
      reload:this.reload
    }
  },
  setup() {
    const store = useStore()
    const isRouterAlive = ref(true)
    onMounted(() => {
      // 载入用户信息
      // store.dispatch('updateUserInfo')

      // 获取活动相关干常量
      // store.dispatch('fetchActivityConstants')
    })
    return{
      isRouterAlive
    }
  },
  computed: {
    transName() {
      return this.$store.state.App.transName;
    },
  },
  methods:{
    reload (){
       this.isRouterAlive = false
       this.$nextTick(function(){
          this.isRouterAlive = true
       })
    }
  }
};
</script>

<style lang="less">
.view-wrapper {
  width: 100%;
  display: block;
  text-align: left !important;
}
.view-wrapper_fixed_nav {
  width: 100%;
  display: block;
  text-align: left !important;
  //margin-top: 46px !important;
}
/** 页面转场动画 */
.slide-right-enter-active,
.slide-right-leave-to,
.slide-left-enter-active,
.slide-left-leave-to {
  will-change: transform !important;
  transition: all 0.3s !important;
  position: absolute !important;
  width: 100% !important;
  left: 0 !important;
}
.slide-right-enter-from {
  transform: translateX(-100%) !important;
}
.slide-right-leave-to {
  transform: translateX(100%);
}
.slide-left-enter-from {
  transform: translateX(100%) !important;
}
.slide-left-leave-to {
  transform: translateX(-100%);
}

.popu-right-enter-active,
.slide-right-leave-to,
.slide-left-enter-active,
.slide-left-leave-to {
  will-change: transform !important;
  transition: all 0.3s !important;
  position: absolute !important;
  width: 100% !important;
  left: 0 !important;
}
.slide-right-enter-from {
  transform: translateX(-100%) !important;
}
.slide-right-leave-to {
  transform: translateX(100%);
}
.slide-left-enter-from {
  transform: translateX(100%) !important;
}
.slide-left-leave-to {
  transform: translateX(-100%);
}
// 覆盖vant
.custom-cell-group-title {
  display: flex;
  align-items: center;
  .van-icon {
    margin-right: 5px;
  }
  label {
    font-size: 16px;
    color: #333;

    // font-weight: bold;
    flex: 1;
  }
  .custom-cell-title__right{
    color: #777
  }
}

//通用部分
.flex-v-center{
  display: flex;
  align-items: center;
}
.nav-page {
  margin-top: 48px;
}
.nav-search-page {
  margin-top: 48px + 54px;
}
body{
  background: #efefef
}
@supports (bottom: env(safe-area-inset-bottom)) {
  #app{
    padding-bottom: constant(safe-area-inset-bottom);
    padding-bottom: env(safe-area-inset-bottom);
  }
}
.fixed-search {
  position: absolute;
  z-index: 10;
  left: 0px;
  right: 0px;
}
.fixed-search.under-nav {
  top: 46px;
}
.page-body {
  margin-top: 50px;
  padding: 0 10px 10px 10px
}
.cell-radius {
  overflow: hidden;
  border-radius: 8px;
}
.field-icon {
  color: #0aa7ef;
  font-size: 15px;
  margin-right: 3px
}
.custom-button-icon{
  margin-right: 3px
}
.list-icon {
  margin-right: 10px;
  color: #0aa7ef;
  font-size: 18px !important;
}
.button-letter-spacing {
  letter-spacing: 5px;
}
.van-cell-group__title--inset {
  padding: 16px 16px 8px 16px !important;
}
.van-cell-group--inset {
  margin: 0 !important;
}
.cell-group-box-shadow {
  box-shadow: 0 8px 12px #ebedf0
}
.van-field__body {
  textarea{
    overflow-y: hidden;
  }
}

.container {
  padding: 0.8em;
  //margin-top: 0.5em
}
</style>
