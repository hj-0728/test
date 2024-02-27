<template>
  <div class="app-spacer" :style="{ background: color, height: h }"></div>
</template>

<script>
const sizeArray = {
  xs: '12px',
  sm: '18px',
  md: '22px',
  lg: '28px'
}
export default {
  name: 'h-spacer',
  props: {
    color: {
      type: String,
      default: '#efefef'
    },
    size: {
      type: String,
      default: '20px'
    }
  },
  setup (props) {},
  computed: {
    h () {
      return sizeArray[this.size] || sizeArray.md
    }
  }
}
</script>

<style scoped>
.app-spacer {
  width: 100%;
}
</style>
