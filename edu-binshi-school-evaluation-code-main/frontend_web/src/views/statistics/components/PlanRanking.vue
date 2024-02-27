<template>
  <div style="margin: 0 10px 10px 10px">
    <div style="margin-bottom: 10px; text-align: right">
      <Input
        v-if="selectDeptListStr"
        v-model:value="selectDeptListStr"
        readonly
        @click="toSelectPlanDeptModal"
        style="margin-right: 6px; width: calc(100% - 70px)"
      />
      <a-button style="border-radius: 8px" type="primary" @click="toSelectPlanDeptModal">
        筛选
      </a-button>
      <select-plan-dept-scope-modal
        @register="registerSelectPlanDeptModal"
        @on-check-dept="onCheckDept"
      />
    </div>
    <List
      size="small"
      bordered
      :loading="loading"
      :data-source="rankingList"
      style="border-radius: 8px"
    >
      <template #loadMore>
        <div
          v-if="!loading && rankingListFilterCount > rankingList.length"
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
          <ListItemMeta>
            <template #title>
              {{ item.name }}
              <span style="color: rgba(0, 0, 0, 0.45); font-size: 14px; padding-left: 10px">{{
                item.deptName
              }}</span>
            </template>
            <template #avatar>
              <Image
                v-if="item.fileUrl"
                :src="item.fileUrl"
                :preview="false"
                style="width: 22px; height: 22px; border-radius: 50%"
              />
              <Image v-else :src="avatarSvg" :preview="false" style="width: 22px; height: 22px" />
            </template>
          </ListItemMeta>
          <div style="font-weight: bold; padding-right: 20px">{{
            item.stringScore ? item.stringScore : item.numericScore
          }}</div>
        </ListItem>
      </template>
    </List>
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { List, ListItem, ListItemMeta, Image, Input } from 'ant-design-vue';
  import { apiGetPlanBenchmarkRanking } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlanStatistics';
  import avatarSvg from '/@/assets/icons/dynamic-avatar-2.svg';
  import SelectPlanDeptScopeModal from '/src/views/statistics/components/SelectPlanDeptScopeModal.vue';
  import { useModal } from '/@/components/Modal';
  export default defineComponent({
    components: {
      List,
      ListItem,
      ListItemMeta,
      Image,
      SelectPlanDeptScopeModal,
      Input,
    },
    props: {
      planId: {
        type: String,
        default: null,
      },
      benchmark: {
        type: Object,
        default: null,
      },
    },
    emits: ['completeEcharts'],
    setup(props) {
      const loading = ref(false);
      const rankingList = ref([]);
      const rankingListFilterCount = ref(0);
      const params = reactive({
        searchText: '', //搜索框中的内容
        pageSize: 20, //页面显示条数
        pageIndex: 0, //当前显示的第几页
        draw: 1, //默认显示第一页
        benchmarkId: props.benchmark?.id,
        evaluationCriteriaPlanId: props.planId,
        dimensionDeptTreeIdList: [],
      });

      const selectDimensionDeptTreeIdList = ref([]);
      const selectDeptListStr = ref('');

      const [registerSelectPlanDeptModal, { openModal: openSelectPlanDeptModal }] = useModal();

      return {
        loading,
        rankingList,
        avatarSvg,
        params,
        ...toRefs(params),
        rankingListFilterCount,
        registerSelectPlanDeptModal,
        openSelectPlanDeptModal,
        selectDimensionDeptTreeIdList,
        selectDeptListStr,
      };
    },
    mounted() {
      console.log(this.benchmark);
      this.getRankingData();
    },
    methods: {
      getRankingData() {
        this.loading = true;
        this.dimensionDeptTreeIdList = this.selectDimensionDeptTreeIdList;
        apiGetPlanBenchmarkRanking(this.params)
          .then((res) => {
            if (res.code === 200 && res.data.draw === this.draw) {
              this.rankingList.push(...res.data.data);
              this.rankingListFilterCount = res.data.filterCount;
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
            this.$emit('completeEcharts');
          });
      },
      onLoadMore() {
        this.pageIndex += 1;
        this.getRankingData();
      },
      init(planId, benchmarkId) {
        this.evaluationCriteriaPlanId = planId;
        this.benchmarkId = benchmarkId;
        this.pageIndex = 0;
        this.searchText = '';
        this.rankingListFilterCount = 0;
        this.rankingList = [];
        this.getRankingData();
      },
      onCheckDept(checkDept) {
        const selectIdList = checkDept.map((dept) => dept.key);
        this.selectDimensionDeptTreeIdList = selectIdList;
        this.selectDeptListStr = checkDept.map((dept) => dept.name).join('，');
        this.init(this.planId, this.benchmarkId);
      },
      toSelectPlanDeptModal() {
        this.openSelectPlanDeptModal(true, {
          checkedDeptKeys: this.selectDimensionDeptTreeIdList,
          planId: this.evaluationCriteriaPlanId,
        });
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
</style>
