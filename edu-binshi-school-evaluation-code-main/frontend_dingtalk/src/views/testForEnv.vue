<template>
  <div style="padding: 20px 10px;">
    <div style="margin: 10px">数据请求的路径为：{{ baseUrl }}</div>
    <div style="margin: 10px">是否需要认证：{{ needAuth }}</div>
  </div>
</template>

<script>

export default {
  name: "test2",
  setup() {

    const baseUrl = import.meta.env.VITE_GLOB_API_URL
    const needAuth = import.meta.env.VITE_NEED_AUTH
    return {
      baseUrl,
      needAuth
    }
  }
}
</script>

<style scoped>

</style>