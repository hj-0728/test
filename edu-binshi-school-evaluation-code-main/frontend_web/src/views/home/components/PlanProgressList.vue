<template>
  <div style="margin: 0 10px 10px 10px">
    <List :loading="loading" :data-source="planList">
      <template #loadMore>
        <div
          v-if="!loading && planListFilterCount > planList.length"
          :style="{
            textAlign: 'center',
            marginTop: '16px',
            height: '32px',
            lineHeight: '32px',
            marginBottom: '12px',
          }"
        >
          <a-button @click="onLoadMore">加载更多</a-button>
        </div>
      </template>
      <template #renderItem="{ item }">
        <ListItem>
          <template #title>{{ item.name }}</template>
          <ListItemMeta>
            <template #description>
              <div class="flex-container">
                <div class="flex-item" v-if="isInProgress">
                  评价情况：
                  <span class="red-font">{{ item.unfinishedCount }}</span>
                  /
                  <span class="green-font">{{ item.finishedCount }}</span>
                </div>
                <div class="flex-item" v-if="isInProgress">
                  完成情况：
                  <span class="red-font">{{ item.unfinishedStudentCount }}</span>
                  /
                  <span class="green-font">{{
                    item.allStudent - item.unfinishedStudentCount
                  }}</span>
                </div>
                <div class="flex-item" v-if="item.todoCount">
                  待办事项：<span class="red-font">{{ item.todoCount }}</span>
                </div>
              </div>
            </template>
            <template #title>
              <div style="margin-bottom: 10px">{{ item.name }}</div>
            </template>
            <template #avatar>
              <Icon icon="plan|svg" :size="30" />
            </template>
          </ListItemMeta>
          <div>
            <Tag v-if="isInProgress" color="green">进行中</Tag>
            <Tag v-else color="blue">待开始</Tag>
          </div>
        </ListItem>
      </template>
    </List>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { List, ListItem, ListItemMeta, Tag } from 'ant-design-vue';
  import { apiGetPlanProgressDetail } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlanStatistics';
  import avatarSvg from '/@/assets/icons/dynamic-avatar-2.svg';
  import { Icon } from '/@/components/Icon';
  export default defineComponent({
    components: {
      Icon,
      List,
      ListItem,
      ListItemMeta,
      Tag,
    },
    props: {
      isInProgress: {
        type: Boolean,
        default: null,
      },
    },
    emits: ['setPlanCount'],
    setup(props) {
      const loading = ref(false);
      const planList = ref([]);
      const planListFilterCount = ref(0);
      const params = reactive({
        searchText: '', //搜索框中的内容
        pageSize: 20, //页面显示条数
        pageIndex: 0, //当前显示的第几页
        draw: 1, //默认显示第一页
        isInProgress: props.isInProgress, //是不是在进行中
      });
      const loadMore = ref(false);
      return {
        loading,
        planList,
        avatarSvg,
        params,
        ...toRefs(params),
        planListFilterCount,
        loadMore,
      };
    },
    mounted() {
      this.getPlanProgressData();
    },
    methods: {
      getPlanProgressData() {
        this.loading = true;
        if (!this.loadMore) {
          this.planList = [];
          this.pageIndex = 0;
        }
        apiGetPlanProgressDetail(this.params)
          .then((res) => {
            if (res.code === 200 && res.data.draw === this.draw) {
              this.planList.push(...res.data.data);
              this.planListFilterCount = res.data.filterCount;
              this.$emit('setPlanCount', {
                isInProgress: this.isInProgress,
                count: res.data.totalCount,
              });
              this.draw += 1;
            }
            if (res.code !== 200) {
              useMessage().createErrorNotification({
                message: '错误',
                description: res.error.message,
              });
            }
          })
          .catch(() => {
            useMessage().createErrorNotification({
              message: '错误',
              description: '网络错误',
            });
          })
          .finally(() => {
            this.loading = false;
            this.loadMore = false;
          });
      },
      onLoadMore() {
        this.pageIndex += 1;
        this.loadMore = true;
        this.getPlanProgressData();
      },
      init() {
        this.pageIndex = 0;
        this.searchText = '';
        this.planListFilterCount = 0;
        this.planList = [];
        this.getPlanProgressData();
      },
    },
  });
</script>

<style lang="less" scoped>
  .echarts-container {
    height: fit-content;
  }

  ::v-deep(.ant-list-item-meta-title) {
    margin: 4px 0 !important;
  }

  ::v-deep(.ant-list-item-meta-avatar) {
    height: 22px;
    margin-top: 4px;
  }

  .red-font {
    color: red;
    font-weight: 500;
  }

  .green-font {
    color: #389e0d;
    font-weight: 500;
  }

  .flex-container {
    display: flex;
  }

  .flex-item {
    min-width: 165px;
  }
</style>
