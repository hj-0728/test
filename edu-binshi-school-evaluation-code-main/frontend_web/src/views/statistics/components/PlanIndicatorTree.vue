<template>
  <div class="indicator-tree">
    <div style="height: 50px; padding: 8px">
      <InputSearch v-model:value="searchValue" placeholder="搜索" enter-button @search="onSearch" />
    </div>
    <div style="height: calc(100% - 60px); padding-left: 4px">
      <BasicTree
        style="padding-bottom: 10px"
        ref="indicatorTreeRef"
        :treeData="indicatorTreeList"
        :clickRowToExpand="false"
        @select="onSelect"
        :selectedKeys="selectedKeys"
        :expandedKeys="expandedKeys"
        :loading="loading"
        @expand="onExpand"
        :delete-default-height="true"
        :fieldNames="{ key: 'id' }"
      >
        <template #title="node">
          <div style="width: fit-content">
            <img :src="indicatorImg" class="icon" />
            <span style="margin-left: 25px" v-if="node.name.indexOf(searchText) > -1">
              {{ node.name.substr(0, node.name.indexOf(searchText)) }}
              <span style="color: #f50">{{ searchText }}</span>
              {{ node.name.substr(node.name.indexOf(searchText) + searchText.length) }}
            </span>
            <span style="margin-left: 25px" v-else>{{ node.name }}</span>
          </div>
        </template>
      </BasicTree>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref, unref } from 'vue';
  import { BasicTree } from '/@/components/Tree';
  import { searchTree } from '/@/utils/helper/treeSearchHelp';
  import { Input } from 'ant-design-vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import indicatorImg from '/@/assets/icons/indicator.svg';
  import { apiGetPlanIndicatorTree } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlanStatistics';

  export default defineComponent({
    components: {
      BasicTree,
      InputSearch: Input.Search,
    },
    props: {
      planId: {
        type: String,
        default: null,
      },
    },
    emits: ['onSelectIndicator'],
    setup() {
      const loading = ref(false);
      const searchValue = ref('');
      const searchText = ref('');
      const indicatorTreeRef = ref();
      const indicatorTreeList = ref<object[]>([]);
      const originalIndicatorTreeList = ref<object[]>([]);
      const expandedKeys = ref<string[]>([]);
      const selectedKeys = ref([]);
      return {
        loading,
        searchValue,
        searchText,
        indicatorTreeRef,
        indicatorTreeList,
        originalIndicatorTreeList,
        expandedKeys,
        selectedKeys,
        indicatorImg,
      };
    },
    mounted() {
      this.getIndicatorTree(this.planId);
    },
    methods: {
      getIndicatorTree(planId) {
        console.log('getIndicatorTree');
        console.log(planId);
        this.loading = true;
        apiGetPlanIndicatorTree(planId)
          .then((res) => {
            if (res.code === 200) {
              this.indicatorTreeList = res.data;
              this.originalIndicatorTreeList = res.data;
              if (this.indicatorTreeList && this.indicatorTreeList.length > 0) {
                this.selectedKeys = [res.data[0].id];
                this.$nextTick(() => {
                  unref(this.indicatorTreeRef)?.expandAll(true);
                });
                this.$emit('onSelectIndicator', { indicatorId: this.indicatorTreeList[0].id });
              } else {
                this.$emit('onSelectIndicator', { indicatorId: null });
              }
            } else {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch(() => {
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络错误3',
            });
          })
          .finally(() => {
            this.loading = false;
          });
      },
      onExpand(keys, _event) {
        this.expandedKeys = keys;
      },
      onSelect(_selectedKeys, e) {
        this.$emit('onSelectIndicator', { indicatorId: e.node.id });
      },
      onSearch() {
        this.loading = true;
        const data = searchTree(this.searchValue, this.originalIndicatorTreeList);
        this.searchText = this.searchValue;
        this.indicatorTreeList = data.treeData;
        this.expandedKeys = data.expandedKeys;
        this.loading = false;
      },
    },
  });
</script>

<style scoped lang="less">
  .indicator-tree {
    height: 100%;

    ::v-deep(.vben-tree .ant-tree-node-content-wrapper .ant-tree-title) {
      // tree 横向滚动自适应
      width: fit-content;
    }

    .icon {
      width: 16px;
      height: 16px;
      position: absolute;
      top: 4px;
    }
  }
</style>
