<template>
  <div>
    <span style="padding: 0 10px"
      ><ProfileOutlined /> <label class="select-label">评价计划</label>
    </span>
    <Select
      ref="select"
      style="width: 380px"
      v-model:value="evaluationCriteriaPlanId"
      :options="searchText ? evaluationCriteriaPlanSearchList : evaluationCriteriaPlanList"
      :searchValue="searchText"
      @change="evaluationCriteriaPlanChange"
      :fieldNames="{ label: 'name', value: 'id' }"
      :maxTagCount="1"
      :maxTagTextLength="5"
      :placeholder="placeholder"
      show-search
      :filter-option="false"
      @search="searchPlan"
      :autoClearSearchValue="false"
    />
  </div>
</template>

<script lang="ts">
  import { defineComponent, reactive, ref, toRefs } from 'vue';
  import { Select } from 'ant-design-vue';
  import { ProfileOutlined } from '@ant-design/icons-vue';
  import { apiGetEvaluationPlanList } from '/@/api/evaluationCriteriaPlan/evaluationCriteriaPlan';
  import { useMessage } from '/@/hooks/web/useMessage';
  import { usePeriodStore } from '/@/store/modules/period';
  import { useRoute } from 'vue-router';

  export default defineComponent({
    components: {
      ProfileOutlined,
      Select,
    },
    emits: ['selectPlanId', 'selectPlanCallback'],
    setup() {
      const evaluationCriteriaPlanLoading = ref(false);
      const evaluationCriteriaPlanList = ref<object[]>([]);
      const evaluationCriteriaPlanSearchList = ref<object[]>([]);
      const evaluationCriteriaPlanFilterTotal = ref(0);
      const route = useRoute();
      const evaluationCriteriaPlanId = ref<String | null>(null);
      const planParams = reactive({
        searchText: '', //搜索框中的内容
        pageSize: 1000, //页面显示条数
        pageIndex: 0, //当前显示的第几页
        draw: 1, //默认显示第一页
        statusList: ['PUBLISHED', 'ARCHIVED'], //状态筛选列表
        finished: true, //已完成的
        isCurrentPeriod: true, // 是否只获取当前选择的周期的计划
      });
      const placeholder = ref('选择评价标准进行过滤');

      const debounceTimer = ref();
      return {
        evaluationCriteriaPlanLoading,
        evaluationCriteriaPlanList,
        evaluationCriteriaPlanFilterTotal,
        evaluationCriteriaPlanId,
        placeholder,
        debounceTimer,
        evaluationCriteriaPlanSearchList,
        planParams,
        ...toRefs(planParams),
        route,
      };
    },
    computed: {
      periodId() {
        return usePeriodStore().getPeriodId;
      },
    },
    watch: {
      periodId(newVal, oldVal) {
        if (newVal !== oldVal && oldVal) {
          this.initPlan();
        }
      },
    },
    mounted() {
      this.getEvaluationCriteriaPlan(true);
    },
    methods: {
      getEvaluationCriteriaPlan(isJudgeParams) {
        this.evaluationCriteriaPlanLoading = true;
        apiGetEvaluationPlanList(this.planParams)
          .then((res) => {
            if (res.code === 200 && this.draw === res.data.draw) {
              this.evaluationCriteriaPlanFilterTotal = res.data.filterCount;
              this.evaluationCriteriaPlanList.push(...res.data.data);
              if (isJudgeParams && this.route.params.id) {
                this.evaluationCriteriaPlanId = this.route.params.id;
              }
              if (res.data.filterCount === 0) {
                this.placeholder = '暂无数据';
                if (!this.evaluationCriteriaPlanId) {
                  this.$emit('selectPlanId', null);
                  this.$emit('selectPlanCallback', null);
                }
              } else {
                if (!this.evaluationCriteriaPlanId) {
                  this.evaluationCriteriaPlanId = this.evaluationCriteriaPlanList[0].id;
                  this.$emit('selectPlanId', this.evaluationCriteriaPlanList[0].id);
                  this.$emit('selectPlanCallback', this.evaluationCriteriaPlanList[0]);
                }
                this.pageIndex += 1;
              }
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
            this.evaluationCriteriaPlanLoading = false;
          });
      },
      evaluationCriteriaPlanChange(_value, option) {
        if (this.evaluationCriteriaPlanId) {
          this.$emit('selectPlanId', this.evaluationCriteriaPlanId);
          this.$emit('selectPlanCallback', option);
        }
      },
      searchPlan(searchText) {
        this.searchText = searchText;
        this.evaluationCriteriaPlanSearchList = this.evaluationCriteriaPlanList.filter((item) =>
          // @ts-ignore
          item.name.includes(this.searchText),
        );
      },
      initPlan() {
        this.pageIndex = 0;
        this.searchText = '';
        this.evaluationCriteriaPlanList = [];
        this.evaluationCriteriaPlanSearchList = [];
        this.evaluationCriteriaPlanFilterTotal = 0;
        this.evaluationCriteriaPlanId = null;
        this.getEvaluationCriteriaPlan(false);
      },
    },
  });
</script>
