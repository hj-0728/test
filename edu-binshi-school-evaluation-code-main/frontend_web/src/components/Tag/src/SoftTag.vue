<template>
  <Tag
    :style="{
      backgroundColor: backgroundColor,
      color: color,
      border: 'none',
      fontWeight: 600,
      borderRadius: '0.25rem',
      padding:' 0 10px'
    }"
    >{{ name }}
    <Icon :icon="icon" v-if="icon" :size="iconSize" />
    <slot v-bind="{}"></slot>
  </Tag>
</template>

<script lang="ts">
  import Icon from '/@/components/Icon/src/Icon.vue';
  import { defineComponent } from 'vue';
  import { Tag } from 'ant-design-vue';
  export default defineComponent({
    name: 'SoftTag',
    components: {
      Tag,
      Icon,
    },
    props: {
      name: {
        type: String,
        default: null,
      },
      backgroundColor: {
        type: String,
        default: null,
      },
      color: {
        type: String,
        default: null,
      },
      icon: {
        type: String,
        default: null,
      },
      iconSize: {
        type: Number,
        default: null,
      },
    },
    setup() {},
  });
</script>

<style scoped></style>
