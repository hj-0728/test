<template>
  <div class="dept-teacher">
    <PageWrapper :content-style="{ height: 'calc(100vh - 80px)' }">
      <div class="content">
        <iframe
          width="100%"
          height="100%"
          :src="'https://dev-bjzp.org-assistant.com/vue-fabric-editor/#/'"
        ></iframe>
      </div>
    </PageWrapper>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import { PageWrapper } from '/@/components/Page';

  export default defineComponent({
    components: {
      PageWrapper,
    },
    setup() {},
    methods: {},
  });
</script>

<style scoped lang="less">
  .dept-teacher {
    .content {
      //background-color: #fff;
      height: 100%;
    }
  }

  .select-item-wrapper {
    margin: 0 10px 0 0;
  }

  .select-period {
    width: 100%;
    display: flex;
    background: white;
    flex: 1;
    justify-content: flex-start;
  }

  .select-label {
    color: black;
    margin-right: 10px;
  }
</style>
